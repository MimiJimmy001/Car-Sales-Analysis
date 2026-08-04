"""
汽车销售复盘分析 - Python 可视化脚本
读取 data/*.csv，生成多维度分析图表
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, facecolor="white")
    print(f"  -> {name}")


# 加载数据
df_sales = pd.read_csv(f"{DATA_DIR}/sales.csv")
df_cars = pd.read_csv(f"{DATA_DIR}/cars.csv")
df_sp = pd.read_csv(f"{DATA_DIR}/salespersons.csv")

df_sales["sale_date"] = pd.to_datetime(df_sales["sale_date"])
df_sales["sale_month"] = df_sales["sale_date"].dt.strftime("%Y-%m")
df_sales["sale_year"] = df_sales["sale_date"].dt.year

df = df_sales.merge(df_cars, on="car_id").merge(df_sp, on="salesperson_id")

# ============================================================
# 图1: 品牌销售额排名 (柱状+均价折线)
# ============================================================
brand_gmv = df.groupby("brand").agg(
    total=("sale_amount_wan", "sum"),
    avg=("sale_amount_wan", "mean"),
    count=("sale_id", "count")
).sort_values("total", ascending=True)

fig, ax1 = plt.subplots(figsize=(12, 6))
colors = ["#C0504D" if i >= len(brand_gmv) - 3 else "#7EA8C4"
          for i in range(len(brand_gmv))]
ax1.barh(brand_gmv.index, brand_gmv["total"] / 10000, color=colors)
ax1.set_title("Brand Revenue Ranking & Avg Price", fontsize=16, fontweight="bold")
ax1.set_xlabel("Revenue (亿)")
for i, (v, c) in enumerate(zip(brand_gmv["total"] / 10000, brand_gmv["count"])):
    ax1.text(v + 0.02, i, f"{v:.1f}亿 ({c:,}台)", va="center", fontsize=8)

ax2 = ax1.twiny()
ax2.plot(brand_gmv["avg"], brand_gmv.index, "D-", color="#2B5B84", markersize=6)
ax2.set_xlabel("Avg Price (万)", color="#2B5B84")
ax2.tick_params(colors="#2B5B84")
save(fig, "01_brand_revenue.png")
plt.close()

# ============================================================
# 图2: 月度销售趋势 + 环比增长率
# ============================================================
monthly = df.groupby("sale_month").agg(
    revenue=("sale_amount_wan", "sum"),
    count=("sale_id", "count"),
    avg=("sale_amount_wan", "mean")
).reset_index().sort_values("sale_month")

monthly["mom_pct"] = monthly["revenue"].pct_change() * 100

fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.fill_between(range(len(monthly)), monthly["revenue"] / 10000,
                 alpha=0.35, color="#2B5B84")
ax1.plot(range(len(monthly)), monthly["revenue"] / 10000,
         color="#2B5B84", linewidth=2, marker="o", markersize=4)
ax1.set_title("Monthly Sales Trend (2023-2025)", fontsize=14, fontweight="bold")
ax1.set_ylabel("Revenue (亿)")
ax1.set_xticks(range(0, len(monthly), 3))
ax1.set_xticklabels(monthly["sale_month"].iloc[::3], rotation=45, ha="right", fontsize=7)

ax2 = ax1.twinx()
valid = monthly["mom_pct"].notna()
colors_mom = ["#C0504D" if v >= 0 else "#4D8066" for v in monthly.loc[valid, "mom_pct"]]
ax2.bar(monthly.index[valid], monthly.loc[valid, "mom_pct"],
        color=colors_mom, alpha=0.5, width=0.6)
ax2.axhline(y=0, color="gray", linewidth=0.5, linestyle="--")
ax2.set_ylabel("MoM Growth (%)")
save(fig, "02_monthly_trend.png")
plt.close()

# ============================================================
# 图3: 区域销售分布 + 各区域客单价
# ============================================================
region_data = df.groupby("region").agg(
    revenue=("sale_amount_wan", "sum"),
    avg=("sale_amount_wan", "mean"),
    count=("sale_id", "count")
).sort_values("revenue", ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

wedges, texts, autotexts = ax1.pie(
    region_data["revenue"], labels=region_data.index,
    autopct="%1.1f%%", startangle=90,
    colors=["#2B5B84", "#4D8066", "#7EA8C4", "#C0504D", "#B8CDE0", "#F4A300", "#8C6E4A"],
    textprops={"fontsize": 9}
)
ax1.set_title("Revenue by Region", fontsize=13, fontweight="bold")

ax2.barh(region_data.index[::-1], region_data["avg"].iloc[::-1],
         color=["#2B5B84" if v > region_data["avg"].mean() else "#7EA8C4"
                for v in region_data["avg"].iloc[::-1]])
ax2.set_title("Avg Price by Region (万)", fontsize=13, fontweight="bold")
for i, (v, c) in enumerate(zip(region_data["avg"].iloc[::-1], region_data["count"].iloc[::-1])):
    ax2.text(v + 0.1, i, f"{v:.1f}万\n({c:,}台)", va="center", fontsize=7)
save(fig, "03_region_analysis.png")
plt.close()

# ============================================================
# 图4: 客户画像 - 年龄与性别交叉分析
# ============================================================
customer = df.groupby(["customer_age_group", "customer_gender"]).agg(
    count=("sale_id", "count"),
    avg_spend=("sale_amount_wan", "mean")
).reset_index()

pivot_count = customer.pivot(index="customer_age_group", columns="customer_gender", values="count").fillna(0)
age_order = ["18-25", "26-35", "36-45", "46-55", "55+"]
pivot_count = pivot_count.reindex(age_order)
pivot_avg = customer.pivot(index="customer_age_group", columns="customer_gender", values="avg_spend").fillna(0)
pivot_avg = pivot_avg.reindex(age_order)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
x = range(len(pivot_count))
w = 0.35
ax1.bar([i - w / 2 for i in x], pivot_count["男"], w, label="Male", color="#2B5B84")
ax1.bar([i + w / 2 for i in x], pivot_count["女"], w, label="Female", color="#C0504D")
ax1.set_title("Customer Count by Age & Gender", fontsize=12, fontweight="bold")
ax1.set_xticks(x)
ax1.set_xticklabels(pivot_count.index)
ax1.legend(fontsize=8)
ax1.set_ylabel("Customer Count")

ax2.bar([i - w / 2 for i in x], pivot_avg["男"], w, label="Male", color="#2B5B84")
ax2.bar([i + w / 2 for i in x], pivot_avg["女"], w, label="Female", color="#C0504D")
ax2.set_title("Avg Spend by Age & Gender (万)", fontsize=12, fontweight="bold")
ax2.set_xticks(x)
ax2.set_xticklabels(pivot_count.index)
ax2.legend(fontsize=8)
ax2.set_ylabel("Avg Spend (万)")
save(fig, "04_customer_profile.png")
plt.close()

# ============================================================
# 图5: 车型类别对比 + 支付方式
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

cat_data = df.groupby("category").agg(
    revenue=("sale_amount_wan", "sum"),
    avg=("sale_amount_wan", "mean"),
    discount=("discount_pct", "mean")
).sort_values("revenue")

ax1.barh(cat_data.index, cat_data["revenue"] / 10000,
         color=["#2B5B84", "#4D8066", "#C0504D"])
ax1.set_title("Revenue by Category (SUV/Sedan/NEV)", fontsize=12, fontweight="bold")
ax1.set_xlabel("Revenue (亿)")
for i, (v, a) in enumerate(zip(cat_data["revenue"] / 10000, cat_data["avg"])):
    ax1.text(v + 0.02, i, f"{v:.1f}亿 | 均价{a:.1f}万", va="center", fontsize=8)

pay = df["payment_type"].value_counts()
ax2.pie(pay.values, labels=pay.index, autopct="%1.1f%%", startangle=90,
        colors=["#2B5B84", "#C0504D", "#7EA8C4"], textprops={"fontsize": 10})
ax2.set_title("Payment Method Distribution", fontsize=12, fontweight="bold")
save(fig, "05_category_payment.png")
plt.close()

# ============================================================
# 图6: 年度对比
# ============================================================
yearly = df.groupby("sale_year").agg(
    revenue=("sale_amount_wan", "sum"),
    count=("sale_id", "count"),
    avg=("sale_amount_wan", "mean"),
    discount=("discount_pct", "mean")
).reset_index()

fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.bar(yearly["sale_year"].astype(int), yearly["revenue"] / 10000,
        color=["#7EA8C4", "#4D8066", "#2B5B84"], width=0.5)
ax1.set_title("Annual Revenue Comparison", fontsize=14, fontweight="bold")
ax1.set_ylabel("Revenue (亿)")
ax1.set_xlabel("Year")
max_h = (yearly["revenue"] / 10000).max()
ax1.set_ylim(0, max_h * 1.3)
for x, (v, c) in enumerate(zip(yearly["revenue"] / 10000, yearly["count"])):
    ax1.text(x, v + 0.3, f"{v:.1f}亿", ha="center", fontsize=10, fontweight="bold")
    ax1.text(x, v - 0.5, f"{c:,}台", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(yearly["sale_year"].astype(int), yearly["avg"], "D-",
         color="#C0504D", linewidth=2, markersize=8)
ax2.set_ylabel("Avg Price (万)", color="#C0504D")
ax2.tick_params(colors="#C0504D")
save(fig, "06_annual_comparison.png")
plt.close()

# ============================================================
# 业务洞察报告
# ============================================================
print("\n" + "=" * 60)
print("业务洞察报告")
print("=" * 60)

# 洞察1: 客户画像
age_26_35 = customer[customer["customer_age_group"] == "26-35"]["count"].sum()
total_customers = customer["count"].sum()
age_26_35_pct = age_26_35 / total_customers * 100
suv_revenue = cat_data.loc["SUV", "revenue"] if "SUV" in cat_data.index else 0
total_revenue = cat_data["revenue"].sum()

print(f"""
【洞察一】26-35岁客群是核心增长引擎
  该年龄段占比 {age_26_35_pct:.1f}%，贡献约 {age_26_35/total_customers*100:.1f}% 的客户量
  建议：针对该客群加大 SUV 车型促销力度，匹配其家庭出行需求
""")

# 洞察2: 区域分析
sc_avg = region_data.loc["华南区", "avg"] if "华南区" in region_data.index else 0
avg_all = region_data["avg"].mean()
print(f"""【洞察二】华南区域客单价偏低，存在升级空间
  华南区客单价 {sc_avg:.1f}万，低于全国均值 {avg_all:.1f}万
  建议：优化华南区高端车型（C级/中大型SUV）的推荐策略与试驾活动
""")

# 洞察3: 季节性
dec_data = monthly[monthly["sale_month"].str.endswith("-12")]
dec_avg = dec_data["revenue"].mean() if len(dec_data) > 0 else 0
other_avg = monthly[~monthly["sale_month"].str.endswith("-12")]["revenue"].mean()

print(f"""【洞察三】年底旺季效应显著，需提前储备库存
  12月均销售额 {dec_avg/10000:.1f}亿，较其他月均值 {other_avg/10000:.1f}亿 高出约 {(dec_avg/other_avg-1)*100:.0f}%
  建议：每年10月启动旺季备货，增加热销车型库存，避免断供
""")

# 输出统计摘要
print(f"""【统计摘要】
  总销售额: {total_revenue/10000:.1f} 亿
  总订单数: {total_customers:,}
  平均折扣: {df['discount_pct'].mean():.1f}%
  贷款比例: {df['is_loan'].mean()*100:.1f}%
""")

print("\n可视化完成! 图表已保存至 output/ 目录:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    if f.endswith(".png"):
        print(f"  - {f}")
