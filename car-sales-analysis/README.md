# 汽车销售复盘分析（Car Sales BI Analysis）

基于 8 万条脱敏汽车销售记录的全流程数据分析项目：从数据建模、SQL 业务分析、Python 可视化到 Excel BI 看板，覆盖"数据 → 洞察 → 展示"完整链路。

## 项目亮点

- **全流程闭环**：数据生成建模 → MySQL SQL 分析 → Python 多维可视化 → Excel 交互式 BI 看板
- **双工具交叉验证**：同一套业务问题分别用 SQL 和 Pandas 实现，结果互相印证
- **业务导向分析**：品牌/车型结构、月度趋势、区域对比、客户画像、支付方式、同比环比等 20 个分析主题
- **可复现**：数据为程序生成的脱敏模拟数据（固定随机种子 42），无隐私风险，克隆即可运行

## 数据集

| 表 | 规模 | 说明 |
|---|---|---|
| `cars` | 46 款车型 | 7 大品牌，覆盖轿车 / SUV / 新能源，含指导价 |
| `salespersons` | 103 人 | 按区域、城市分布 |
| `sales` | 80,000 条 | 2023–2025 年销售记录，含成交金额、客户性别 / 年龄段、支付方式、折扣率、是否贷款 |

> 数据由 `generate_data.py` 生成的脱敏模拟数据，不包含任何真实客户或商业信息。

## 项目结构

```
car-sales-analysis/
├── generate_data.py      # 数据生成脚本（脱敏建模，种子固定可复现）
├── analysis.sql          # MySQL 分析脚本（建表 + 20 个业务分析查询）
├── visualize.py          # Python 可视化（6 张分析图表）
├── excel_dashboard.py    # Excel BI 看板生成（KPI 指标卡 + 交互图表）
├── data/                 # 三张数据表 CSV
└── output/               # 分析图表 + 汽车销售BI分析看板.xlsx
```

## 分析主题

**SQL 分析（analysis.sql）**：品牌与车型销售排行、月度 / 年度趋势、区域与城市对比、销售人员业绩、客户年龄与性别画像、支付方式与贷款渗透率、折扣力度分析、同比环比增长等。

**Python 可视化（visualize.py）**：

| 图表 | 内容 |
|---|---|
| 01_brand_revenue | 品牌销售额排名 + 均价折线 |
| 02_monthly_trend | 月度销量与销售额趋势 |
| 03_region_analysis | 区域销售对比 |
| 04_customer_profile | 客户画像（年龄段 × 性别） |
| 05_category_payment | 品类结构与支付方式分布 |
| 06_annual_comparison | 年度同比对比 |

**Excel BI 看板（excel_dashboard.py）**：KPI 指标卡、月度趋势图、区域分布图、品类对比图，使用 openpyxl 原生图表，打开即可交互。

## 快速开始

### 环境依赖

```bash
pip install pandas matplotlib openpyxl
# SQL 部分需要 MySQL 8.0+
```

### 运行

```bash
# 1. 重新生成数据（可选，data/ 已自带）
python generate_data.py

# 2. SQL 分析：将 data/*.csv 导入 MySQL 后执行 analysis.sql

# 3. 生成可视化图表（输出到 output/）
python visualize.py

# 4. 生成 Excel BI 看板
python excel_dashboard.py
```

## 技术栈

Python · Pandas · Matplotlib · openpyxl · MySQL

##  License

MIT
