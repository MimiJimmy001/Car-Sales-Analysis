"""
某品牌汽车经销商脱敏销售数据生成
输出: cars.csv, sales.csv, salespersons.csv
数据量: 车辆46款, 销售人员103人, 销售记录80,000条, 时间跨度2023-2025
"""
import csv
import random
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

random.seed(42)

# ============================================================
# 车辆信息表（脱敏）
# ============================================================
brands_models = {
    "大众": [("朗逸", "轿车", "A级"), ("速腾", "轿车", "A+级"), ("迈腾", "轿车", "B级"), ("途观L", "SUV", "中型"), ("途昂", "SUV", "中大型"), ("帕萨特", "轿车", "B级"), ("ID.4", "SUV", "新能源"), ("揽境", "SUV", "大型")],
    "丰田": [("卡罗拉", "轿车", "A级"), ("凯美瑞", "轿车", "B级"), ("RAV4", "SUV", "紧凑型"), ("汉兰达", "SUV", "中型"), ("亚洲龙", "轿车", "B+级"), ("威兰达", "SUV", "紧凑型"), ("bZ4X", "SUV", "新能源")],
    "本田": [("思域", "轿车", "A级"), ("雅阁", "轿车", "B级"), ("CR-V", "SUV", "紧凑型"), ("缤智", "SUV", "小型"), ("冠道", "SUV", "中型"), ("型格", "轿车", "A级"), ("e:NS1", "SUV", "新能源")],
    "比亚迪": [("秦PLUS", "轿车", "新能源"), ("宋PLUS", "SUV", "新能源"), ("汉", "轿车", "新能源"), ("唐", "SUV", "新能源"), ("海豚", "轿车", "新能源"), ("元PLUS", "SUV", "新能源"), ("海豹", "轿车", "新能源")],
    "宝马": [("3系", "轿车", "B级"), ("5系", "轿车", "C级"), ("X3", "SUV", "中型"), ("X5", "SUV", "中大型"), ("iX3", "SUV", "新能源"), ("X1", "SUV", "紧凑型")],
    "奔驰": [("C级", "轿车", "B级"), ("E级", "轿车", "C级"), ("GLC", "SUV", "中型"), ("GLE", "SUV", "中大型"), ("A级", "轿车", "A级"), ("EQE", "轿车", "新能源")],
    "日产": [("轩逸", "轿车", "A级"), ("天籁", "轿车", "B级"), ("逍客", "SUV", "紧凑型"), ("奇骏", "SUV", "紧凑型"), ("劲客", "SUV", "小型")],
}

price_config = {
    "新能源": (12, 35), "A级": (8, 16), "A+级": (12, 20), "B级": (16, 28),
    "B+级": (20, 32), "C级": (30, 55), "小型": (8, 14), "紧凑型": (14, 22),
    "中型": (22, 45), "中大型": (35, 70), "大型": (28, 50),
}

cars = []
car_id = 0
for brand, models in brands_models.items():
    for model, category, level in models:
        car_id += 1
        p_min, p_max = price_config.get(level, (10, 20))
        price = round(random.uniform(p_min, p_max), 2)
        cars.append([car_id, brand, model, category, level, price])

with open(f"{DATA_DIR}/cars.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["car_id", "brand", "model", "category", "level", "guide_price_wan"])
    w.writerows(cars)
print(f"cars.csv: {len(cars)} 款车型")

# ============================================================
# 销售人员表
# ============================================================
regions = ["华东区", "华南区", "华北区", "华中区", "西南区", "西北区", "东北区"]
region_cities = {
    "华东区": ["上海", "杭州", "南京", "苏州", "宁波", "合肥"],
    "华南区": ["广州", "深圳", "东莞", "佛山", "厦门", "福州"],
    "华北区": ["北京", "天津", "石家庄", "太原", "济南", "青岛"],
    "华中区": ["武汉", "长沙", "郑州", "南昌"],
    "西南区": ["成都", "重庆", "昆明", "贵阳"],
    "西北区": ["西安", "兰州", "乌鲁木齐", "银川"],
    "东北区": ["沈阳", "大连", "长春", "哈尔滨"],
}
surnames = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
names_pool = "伟强明磊洋涛军鹏勇峰斌杰超辉亮建华刚文武博"

salespersons = []
sp_id = 0
for region in regions:
    for city in region_cities[region]:
        for _ in range(random.randint(2, 4)):
            sp_id += 1
            name = random.choice(surnames) + random.choice(names_pool) + random.choice(names_pool)
            salespersons.append([sp_id, name, region, city])

with open(f"{DATA_DIR}/salespersons.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["salesperson_id", "name", "region", "city"])
    w.writerows(salespersons)
print(f"salespersons.csv: {len(salespersons)} 人")

# ============================================================
# 销售记录表 (80000条, 2023.01 - 2025.12)
# ============================================================
num_cars = len(cars)
num_sp = len(salespersons)
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = (end_date - start_date).days

customer_genders = ["男"] * 65 + ["女"] * 35  # 偏男性
age_groups = ["18-25"] * 10 + ["26-35"] * 35 + ["36-45"] * 30 + ["46-55"] * 15 + ["55+"] * 10
payment_types = ["全款"] * 30 + ["贷款"] * 50 + ["分期"] * 20

# 季节性: 年底和春季是旺季
month_weights = [1.0, 0.6, 1.2, 1.1, 1.0, 0.9, 0.8, 0.8, 1.1, 1.0, 1.1, 1.5]

with open(f"{DATA_DIR}/sales.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["sale_id", "car_id", "salesperson_id", "sale_date", "sale_amount_wan",
                 "customer_gender", "customer_age_group", "payment_type", "discount_pct", "is_loan"])
    for i in range(1, 80001):
        cid = random.randint(1, num_cars)
        sp = random.randint(1, num_sp)
        # 按月份权重生成日期
        while True:
            rand_day = start_date + timedelta(days=random.randint(0, date_range))
            wgt = month_weights[rand_day.month - 1]
            if random.random() < wgt / max(month_weights):
                break
        car = cars[cid - 1]
        base = car[5]
        discount = round(random.uniform(0, 12) if random.random() < 0.7 else random.uniform(8, 18), 1)
        amount = round(base * (1 - discount / 100), 2)
        payment = random.choice(payment_types)
        is_loan = 1 if payment in ("贷款", "分期") else 0
        w.writerow([i, cid, sp, rand_day.strftime("%Y-%m-%d"), amount,
                     random.choice(customer_genders), random.choice(age_groups),
                     payment, discount, is_loan])

print(f"sales.csv: 80,000 条销售记录 (2023-2025)")
print("\n数据集生成完成!")
