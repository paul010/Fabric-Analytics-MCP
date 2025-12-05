import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# 1. 生成模拟数据
def generate_data():
    brands = ['Huawei', 'Xiaomi', 'OPPO', 'vivo', 'Apple', 'Honor', 'Others']
    # 模拟2024年至今的月度数据
    dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
    
    data = []
    
    base_sales = {
        'Huawei': 300, 'Xiaomi': 250, 'OPPO': 200, 
        'vivo': 190, 'Apple': 280, 'Honor': 220, 'Others': 100
    }
    
    for date in dates:
        month_factor = 1.0
        # 年底和年初销售旺季
        if date.month in [1, 2, 11, 12]:
            month_factor = 1.2
        # 618
        elif date.month == 6:
            month_factor = 1.3
            
        for brand in brands:
            # 添加一些随机波动
            random_factor = np.random.normal(1, 0.05)
            sales = int(base_sales[brand] * month_factor * random_factor * 10000) # 销量（台）
            revenue = sales * np.random.randint(2000, 5000) # 估算营收
            
            data.append({
                'Date': date,
                'Brand': brand,
                'Sales_Volume': sales,
                'Revenue': revenue
            })
            
    return pd.DataFrame(data)

df = generate_data()

# 2. 数据汇总
# 2.1 品牌总销量和总营收
brand_summary = df.groupby('Brand').agg({
    'Sales_Volume': 'sum',
    'Revenue': 'sum'
}).reset_index().sort_values('Sales_Volume', ascending=False)

# 2.2 月度趋势
monthly_trend = df.groupby('Date').agg({
    'Sales_Volume': 'sum',
    'Revenue': 'sum'
}).reset_index()

# 2.3 品牌月度趋势
brand_monthly = df.pivot(index='Date', columns='Brand', values='Sales_Volume')

# 3. 创建仪表盘
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'xy'}],
           [{'type': 'xy', 'colspan': 2}, None]],
    subplot_titles=('2024年市场份额 (销量)', '各品牌总营收 (亿元)', '月度销量趋势 (分品牌)'),
    vertical_spacing=0.15
)

# 图表 1: 市场份额饼图
fig.add_trace(
    go.Pie(
        labels=brand_summary['Brand'],
        values=brand_summary['Sales_Volume'],
        name="市场份额",
        hole=.4,
        marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#7f7f7f'])
    ),
    row=1, col=1
)

# 图表 2: 营收柱状图
fig.add_trace(
    go.Bar(
        x=brand_summary['Brand'],
        y=brand_summary['Revenue'] / 100000000, # 转换为亿元
        name="总营收 (亿元)",
        marker_color='#17becf'
    ),
    row=1, col=2
)

# 图表 3: 月度趋势堆叠面积图
for brand in brand_summary['Brand']: # 按销量排序添加
    fig.add_trace(
        go.Scatter(
            x=brand_monthly.index,
            y=brand_monthly[brand],
            name=brand,
            stackgroup='one',
            mode='lines'
        ),
        row=2, col=1
    )

# 更新布局
fig.update_layout(
    title_text="中国智能手机市场分析仪表盘 (2024模拟数据)",
    height=800,
    showlegend=True,
    template="plotly_white"
)

# 导出
output_file = "china_phone_dashboard.html"
fig.write_html(output_file)
print(f"Dashboard generated: {output_file}")
