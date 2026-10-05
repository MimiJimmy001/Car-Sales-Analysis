# 项目可视化与可解释性指南

本页用思维导图、流程、指标树、结论地图和现有图表解释汽车销售复盘项目。需要注意的是，本项目数据由 `generate_data.py` 按固定随机种子生成，数字用于演示方法，不代表真实企业。

## 图 1：项目能力思维导图

```mermaid
flowchart TD
    ROOT((汽车销售复盘))
    ROOT --> DATA[模拟数据]
    ROOT --> SQL[SQL 分析]
    ROOT --> PY[Python 可视化]
    ROOT --> EXCEL[Excel BI]
    ROOT --> INSIGHT[经营结论]

    DATA --> D1[cars 车型]
    DATA --> D2[salespersons 销售员]
    DATA --> D3[sales 80,000 条记录]

    SQL --> S1[建表]
    SQL --> S2[20 组分析查询]
    SQL --> S3[经营指标]

    PY --> P1[Pandas 清洗]
    PY --> P2[Matplotlib 图表]
    PY --> P3[固定随机种子]

    EXCEL --> E1[KPI 指标卡]
    EXCEL --> E2[联动图表]
    EXCEL --> E3[交互式看板]

    INSIGHT --> I1[品牌与品类结构]
    INSIGHT --> I2[季节性与月度趋势]
    INSIGHT --> I3[客户画像]
    INSIGHT --> I4[支付方式与团队效能]
```

## 图 2：数据生成与分析流程

```mermaid
flowchart LR
    GEN[generate_data.py] --> CARS[cars.csv]
    GEN --> STAFF[salespersons.csv]
    GEN --> SALES[sales.csv]
    CARS --> SQL[analysis.sql]
    STAFF --> SQL
    SALES --> SQL
    SALES --> VIZ[visualize.py]
    SALES --> XLSX[excel_dashboard.py]
    SQL --> METRIC[SQL 指标结果]
    VIZ --> PNG[6 张分析图]
    XLSX --> DASH[Excel BI 看板]
```

数据、图表和 Excel 都可以从生成脚本重新构建，当前仓库不包含真实汽车经销商数据。

## 图 3：分析问题与指标树

```mermaid
flowchart TD
    ROOT[经营复盘问题]
    ROOT --> Q1[卖什么]
    ROOT --> Q2[什么时候卖]
    ROOT --> Q3[卖给谁]
    ROOT --> Q4[怎么卖]
    ROOT --> Q5[谁来卖]

    Q1 --> M1[品牌 / 品类销售额]
    Q1 --> M2[车型均价]
    Q2 --> M3[月度趋势]
    Q2 --> M4[同比 / 环比 / 季节性]
    Q3 --> M5[年龄 × 性别]
    Q3 --> M6[客单价分布]
    Q4 --> M7[全款 / 贷款 / 分期]
    Q4 --> M8[折扣率和贷款渗透率]
    Q5 --> M9[区域排名]
    Q5 --> M10[销售员业绩]
```

## 图 4：支付方式与客户结构解释

```mermaid
flowchart LR
    CUSTOMER[客户记录] --> SEGMENT[年龄与性别分层]
    CUSTOMER --> PAYMENT[支付方式]
    CUSTOMER --> AMOUNT[成交金额]
    PAYMENT --> LOAN[贷款渗透率]
    PAYMENT --> CASH[全款占比]
    PAYMENT --> INSTALLMENT[分期占比]
    SEGMENT --> PROFILE[客户画像]
    AMOUNT --> AOV[各年龄段客单价]
    LOAN --> ACTION[金融方案策略]
    PROFILE --> ACTION
    AOV --> ACTION
```

## 图 5：结论、证据与限制地图

```mermaid
flowchart TD
    ROOT((结论与限制))
    ROOT --> C1[品牌格局]
    ROOT --> C2[品类结构]
    ROOT --> C3[季节规律]
    ROOT --> C4[客户与支付]

    C1 --> E1[大众销量与豪华品牌均价]
    C2 --> E2[SUV 销售额约为轿车 1.4 倍]
    C3 --> E3[年末冲高 / 春节回落 / 波动超 ±50%]
    C4 --> E4[贷款约 49.7% / 全款约 30.3%]

    E1 --> LIMIT[数据为模拟生成，不能外推真实市场]
    E2 --> LIMIT
    E3 --> LIMIT
    E4 --> LIMIT
```

## 既有分析图表

### 品牌营收

![品牌营收](../output/01_brand_revenue.png)

解释：比较不同品牌的销售额、销量和价格带，识别走量与高价值路线。

### 月度趋势

![月度趋势](../output/02_monthly_trend.png)

解释：观察季节性、年末冲量和春节回落等时间规律。

### 客户画像

![客户画像](../output/04_customer_profile.png)

解释：展示年龄、性别和客单价结构，用于解释不同客户群体的购车行为。

### 品类与支付

![品类支付](../output/05_category_payment.png)

解释：结合品类、支付方式和折扣信息，分析产品结构与金融渗透率。

## 视觉阅读顺序

1. 图 1 看项目模块和模拟数据边界。
2. 图 2 看数据生成到 SQL、图表和 Excel 的完整链路。
3. 图 3 看五个经营问题和对应指标。
4. 图 4 看客户、支付和金融策略之间的解释关系。
5. 图 5 与四张图表用于说明结论、证据和不可外推的限制。