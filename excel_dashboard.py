"""
Excel BI 看板生成脚本
基于数据分析结果，生成交互式 Excel BI 看板
包含: KPI 指标卡、月度趋势图、区域分布图、品类对比图
"""
import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference, BarChart3D
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 加载数据
df_sales = pd.read_csv(f"{DATA_DIR}/sales.csv")
df_cars = pd.read_csv(f"{DATA_DIR}/cars.csv")
df_sp = pd.read_csv(f"{DATA_DIR}/salespersons.csv")
df_sales["sale_date"] = pd.to_datetime(df_sales["sale_date"])
df_sales["sale_month"] = df_sales["sale_date"].dt.strftime("%Y-%m")
df = df_sales.merge(df_cars, on="car_id").merge(df_sp, on="salesperson_id")

wb = Workbook()

# ============================================================
# 样式定义
# ============================================================
header_font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="2B5B84", end_color="2B5B84", fill_type="solid")
data_font = Font(name="微软雅黑", size=10)
kpi_font = Font(name="微软雅黑", size=28, bold=True, color="2B5B84")
kpi_label_font = Font(name="微软雅黑", size=11, color="666666")
title_font = Font(name="微软雅黑", size=16, bold=True, color="2B5B84")
thin_border = Border(
    left=Side(style="thin", color="D3D3D3"),
    right=Side(style="thin", color="D3D3D3"),
    top=Side(style="thin", color="D3D3D3"),
    bottom=Side(style="thin", color="D3D3D3")
)

def style_header(ws, row, cols):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

def style_data(ws, start_row, end_row, cols):
    for r in range(start_row, end_row + 1):
        for c in range(1, cols + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = data_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center")

# ============================================================
# Sheet 1: KPI 仪表板
# ============================================================
ws1 = wb.active
ws1.title = "KPI仪表板"
ws1.sheet_properties.tabColor = "2B5B84"

# 标题
ws1.merge_cells("A1:H1")
ws1["A1"] = "汽车销售 BI 分析看板"
ws1["A1"].font = title_font
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[1].height = 40

# KPI 指标
total_revenue = df["sale_amount_wan"].sum()
total_orders = len(df)
avg_price = df["sale_amount_wan"].mean()
avg_discount = df["discount_pct"].mean()
loan_rate = df["is_loan"].mean() * 100
total_customers = df["customer_id"].nunique() if "customer_id" in df.columns else total_orders

kpis = [
    ("C2", "总销售额（亿）", f"{total_revenue/10000:.1f}"),
    ("E2", "总订单数", f"{total_orders:,}"),
    ("G2", "客单价（万）", f"{avg_price:.1f}"),
    ("C3", "平均折扣率", f"{avg_discount:.1f}%"),
    ("E3", "贷款购车比例", f"{loan_rate:.1f}%"),
    ("G3", "品牌数量", "7"),
]

for cell_ref, label, value in kpis:
    col_letter = cell_ref[0]
    row = int(cell_ref[1:])
    # 标签
    ws1[f"{col_letter}{row}"] = label
    ws1[f"{col_letter}{row}"].font = kpi_label_font
    ws1[f"{col_letter}{row}"].alignment = Alignment(horizontal="center")
    # 数值
    ws1[f"{col_letter}{row+1}"] = value
    ws1[f"{col_letter}{row+1}"].font = kpi_font
    ws1[f"{col_letter}{row+1}"].alignment = Alignment(horizontal="center")

for c in ["C", "E", "G"]:
    ws1.column_dimensions[c].width = 20
ws1.row_dimensions[2].height = 25
ws1.row_dimensions[3].height = 50
ws1.row_dimensions[4].height = 25
ws1.row_dimensions[5].height = 50

# ============================================================
# Sheet 2: 月度趋势
# ============================================================
ws2 = wb.create_sheet("月度销售趋势")
ws2.sheet_properties.tabColor = "4D8066"

monthly = df.groupby("sale_month").agg(
    revenue=("sale_amount_wan", "sum"),
    orders=("sale_id", "count")
).reset_index().sort_values("sale_month")

ws2["A1"] = "月度销售趋势明细"
ws2["A1"].font = title_font
ws2.merge_cells("A1:C1")

headers = ["月份", "销售额（万）", "订单数"]
for i, h in enumerate(headers, 1):
    ws2.cell(row=3, column=i, value=h)
style_header(ws2, 3, 3)

for idx, (_, row) in enumerate(monthly.iterrows()):
    ws2.cell(row=4 + idx, column=1, value=row["sale_month"])
    ws2.cell(row=4 + idx, column=2, value=round(row["revenue"], 2))
    ws2.cell(row=4 + idx, column=3, value=row["orders"])
style_data(ws2, 4, 3 + len(monthly), 3)

# 折线图
chart = LineChart()
chart.title = "月度销售额趋势"
chart.y_axis.title = "销售额（万）"
chart.x_axis.title = "月份"
chart.style = 10
chart.height = 14
chart.width = 28
data_ref = Reference(ws2, min_col=2, min_row=3, max_row=3 + len(monthly))
cats_ref = Reference(ws2, min_col=1, min_row=4, max_row=3 + len(monthly))
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)
chart.series[0].graphicalProperties.line.width = 25000
ws2.add_chart(chart, "A40")

ws2.column_dimensions["A"].width = 12
ws2.column_dimensions["B"].width = 16
ws2.column_dimensions["C"].width = 12

# ============================================================
# Sheet 3: 区域分析
# ============================================================
ws3 = wb.create_sheet("区域分布")
ws3.sheet_properties.tabColor = "C0504D"

region_data = df.groupby("region").agg(
    revenue=("sale_amount_wan", "sum"),
    orders=("sale_id", "count"),
    avg=("sale_amount_wan", "mean")
).sort_values("revenue", ascending=False).reset_index()

ws3["A1"] = "区域销售分布"
ws3["A1"].font = title_font
ws3.merge_cells("A1:D1")

headers = ["区域", "销售额（万）", "订单数", "客单价（万）"]
for i, h in enumerate(headers, 1):
    ws3.cell(row=3, column=i, value=h)
style_header(ws3, 3, 4)

for idx, (_, row) in enumerate(region_data.iterrows()):
    ws3.cell(row=4 + idx, column=1, value=row["region"])
    ws3.cell(row=4 + idx, column=2, value=round(row["revenue"], 2))
    ws3.cell(row=4 + idx, column=3, value=row["orders"])
    ws3.cell(row=4 + idx, column=4, value=round(row["avg"], 2))
style_data(ws3, 4, 3 + len(region_data), 4)

# 饼图
pie = PieChart()
pie.title = "各区域销售额占比"
pie.height = 14
pie.width = 18
data_ref = Reference(ws3, min_col=2, min_row=3, max_row=3 + len(region_data))
cats_ref = Reference(ws3, min_col=1, min_row=4, max_row=3 + len(region_data))
pie.add_data(data_ref, titles_from_data=True)
pie.set_categories(cats_ref)
pie.dataLabels = DataLabelList()
pie.dataLabels.showPercent = True
ws3.add_chart(pie, "F3")

ws3.column_dimensions["A"].width = 12
ws3.column_dimensions["B"].width = 16
ws3.column_dimensions["C"].width = 12
ws3.column_dimensions["D"].width = 14

# ============================================================
# Sheet 4: 品牌与车型分析
# ============================================================
ws4 = wb.create_sheet("品牌车型分析")
ws4.sheet_properties.tabColor = "7EA8C4"

brand_data = df.groupby("brand").agg(
    revenue=("sale_amount_wan", "sum"),
    orders=("sale_id", "count"),
    avg=("sale_amount_wan", "mean")
).sort_values("revenue", ascending=False).reset_index()

ws4["A1"] = "品牌销售排名"
ws4["A1"].font = title_font
ws4.merge_cells("A1:D1")

headers = ["品牌", "销售额（万）", "订单数", "客单价（万）"]
for i, h in enumerate(headers, 1):
    ws4.cell(row=3, column=i, value=h)
style_header(ws4, 3, 4)

for idx, (_, row) in enumerate(brand_data.iterrows()):
    ws4.cell(row=4 + idx, column=1, value=row["brand"])
    ws4.cell(row=4 + idx, column=2, value=round(row["revenue"], 2))
    ws4.cell(row=4 + idx, column=3, value=row["orders"])
    ws4.cell(row=4 + idx, column=4, value=round(row["avg"], 2))
style_data(ws4, 4, 3 + len(brand_data), 4)

# 柱状图
bar = BarChart()
bar.type = "col"
bar.title = "各品牌销售额对比"
bar.y_axis.title = "销售额（万）"
bar.height = 14
bar.width = 24
data_ref = Reference(ws4, min_col=2, min_row=3, max_row=3 + len(brand_data))
cats_ref = Reference(ws4, min_col=1, min_row=4, max_row=3 + len(brand_data))
bar.add_data(data_ref, titles_from_data=True)
bar.set_categories(cats_ref)
bar.series[0].graphicalProperties.solidFill = "2B5B84"
ws4.add_chart(bar, "F3")

ws4.column_dimensions["A"].width = 12
ws4.column_dimensions["B"].width = 16
ws4.column_dimensions["C"].width = 12
ws4.column_dimensions["D"].width = 14

# ============================================================
# 保存
# ============================================================
output_path = os.path.join(OUTPUT_DIR, "汽车销售BI分析看板.xlsx")
wb.save(output_path)
print(f"Excel BI 看板已生成: {output_path}")
print(f"  包含4个Sheet: KPI仪表板 / 月度销售趋势 / 区域分布 / 品牌车型分析")
