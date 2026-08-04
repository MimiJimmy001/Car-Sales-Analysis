-- ============================================================
-- 汽车销售复盘分析 - SQL 脚本 (MySQL)
-- 数据集: cars / sales / salespersons 三表，8万条销售记录
-- ============================================================

-- 1. 建表与数据导入
CREATE TABLE cars (
    car_id INT PRIMARY KEY,
    brand VARCHAR(20),
    model VARCHAR(20),
    category VARCHAR(10),
    level VARCHAR(10),
    guide_price_wan DECIMAL(10,2)
);

CREATE TABLE salespersons (
    salesperson_id INT PRIMARY KEY,
    name VARCHAR(10),
    region VARCHAR(10),
    city VARCHAR(20)
);

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    car_id INT,
    salesperson_id INT,
    sale_date DATE,
    sale_amount_wan DECIMAL(10,2),
    customer_gender VARCHAR(2),
    customer_age_group VARCHAR(10),
    payment_type VARCHAR(5),
    discount_pct DECIMAL(5,1),
    is_loan TINYINT,
    FOREIGN KEY (car_id) REFERENCES cars(car_id),
    FOREIGN KEY (salesperson_id) REFERENCES salespersons(salesperson_id)
);

-- (导入 data/*.csv 后运行以下分析)

-- ============================================================
-- 2. 品牌维度：各品牌销售额、销量与均价
-- ============================================================
SELECT 
    c.brand,
    COUNT(s.sale_id) AS sales_count,
    ROUND(SUM(s.sale_amount_wan), 2) AS total_revenue_wan,
    ROUND(AVG(s.sale_amount_wan), 2) AS avg_price_wan,
    ROUND(AVG(s.discount_pct), 1) AS avg_discount_pct,
    ROUND(SUM(s.is_loan) / COUNT(*) * 100, 1) AS loan_rate_pct
FROM sales s
JOIN cars c ON s.car_id = c.car_id
GROUP BY c.brand
ORDER BY total_revenue_wan DESC;

-- ============================================================
-- 3. 月度趋势：GMV、销量与客单价的月度变化
-- ============================================================
SELECT 
    DATE_FORMAT(sale_date, '%Y-%m') AS sale_month,
    COUNT(*) AS order_count,
    ROUND(SUM(sale_amount_wan), 2) AS monthly_revenue_wan,
    ROUND(AVG(sale_amount_wan), 2) AS avg_price_wan,
    ROUND(AVG(discount_pct), 1) AS avg_discount_pct
FROM sales
GROUP BY sale_month
ORDER BY sale_month;

-- ============================================================
-- 4. 区域维度：各区域销售额分布
-- ============================================================
SELECT 
    sp.region,
    COUNT(s.sale_id) AS order_count,
    ROUND(SUM(s.sale_amount_wan), 2) AS total_revenue_wan,
    ROUND(AVG(s.sale_amount_wan), 2) AS avg_price_wan,
    ROUND(AVG(s.discount_pct), 1) AS avg_discount_pct
FROM sales s
JOIN salespersons sp ON s.salesperson_id = sp.salesperson_id
GROUP BY sp.region
ORDER BY total_revenue_wan DESC;

-- ============================================================
-- 5. 车型类别维度：轿车 vs SUV vs 新能源
-- ============================================================
SELECT 
    c.category,
    COUNT(s.sale_id) AS order_count,
    ROUND(SUM(s.sale_amount_wan), 2) AS total_revenue,
    ROUND(AVG(s.sale_amount_wan), 2) AS avg_price
FROM sales s
JOIN cars c ON s.car_id = c.car_id
GROUP BY c.category
ORDER BY order_count DESC;

-- ============================================================
-- 6. 客户画像：性别与年龄段交叉分析
-- ============================================================
SELECT 
    customer_gender,
    customer_age_group,
    COUNT(*) AS customer_count,
    ROUND(AVG(sale_amount_wan), 2) AS avg_purchase_wan,
    ROUND(SUM(sale_amount_wan), 2) AS total_revenue_wan
FROM sales
GROUP BY customer_gender, customer_age_group
ORDER BY customer_age_group, customer_gender;

-- ============================================================
-- 7. 支付方式分析
-- ============================================================
SELECT 
    payment_type,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales), 1) AS pct,
    ROUND(AVG(sale_amount_wan), 2) AS avg_amount_wan
FROM sales
GROUP BY payment_type
ORDER BY count DESC;

-- ============================================================
-- 8. 销售人员 Top 10
-- ============================================================
SELECT 
    sp.name,
    sp.region,
    sp.city,
    COUNT(s.sale_id) AS sales_count,
    ROUND(SUM(s.sale_amount_wan), 2) AS total_revenue_wan,
    ROUND(AVG(s.discount_pct), 1) AS avg_discount_pct
FROM sales s
JOIN salespersons sp ON s.salesperson_id = sp.salesperson_id
GROUP BY sp.salesperson_id, sp.name, sp.region, sp.city
ORDER BY total_revenue_wan DESC
LIMIT 10;

-- ============================================================
-- 9. 年度对比分析 (2023 vs 2024 vs 2025)
-- ============================================================
SELECT 
    YEAR(sale_date) AS year,
    COUNT(*) AS order_count,
    ROUND(SUM(sale_amount_wan), 2) AS annual_revenue_wan,
    ROUND(AVG(sale_amount_wan), 2) AS avg_price_wan
FROM sales
GROUP BY year
ORDER BY year;

-- ============================================================
-- 10. 折扣策略效果: 折扣力度与销量的关系
-- ============================================================
SELECT 
    CASE 
        WHEN discount_pct < 3 THEN '0-3%'
        WHEN discount_pct < 6 THEN '3-6%'
        WHEN discount_pct < 9 THEN '6-9%'
        WHEN discount_pct < 12 THEN '9-12%'
        ELSE '12%+'
    END AS discount_range,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales), 1) AS pct
FROM sales
GROUP BY discount_range
ORDER BY discount_range;
