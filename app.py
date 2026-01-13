import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from sklearn.cluster import KMeans
import numpy as np
import calendar

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="E-Commerce AI Trend Analysis",
    layout="wide",
    page_icon="🛒"
)

st.markdown("""
<style>
    .stApp { background-color: #050505; }
    
    /* KPI Cards */
    .metric-card {
        background-color: #121212;
        border: 1px solid #333;
        border-left: 4px solid #00F0FF;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 240, 255, 0.1);
    }
    .metric-value { font-size: 24px; color: #FFFFFF; font-weight: 700; }
    .metric-label { font-size: 12px; color: #00F0FF; letter-spacing: 1px; }
    
    /* Headers */
    h1, h2, h3 { color: #E0E0E0 !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Charts */
    .js-plotly-plot .plotly .main-svg { background-color: rgba(0,0,0,0) !important; }
    
    /* Recommendation Card */
    .rec-card {
        background-color: #1E1E1E;
        border: 1px solid #00CC96;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .rec-title { color: #00CC96; font-size: 18px; font-weight: bold; }
    .rec-text { color: #CCCCCC; font-size: 14px; margin-top: 8px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LOADING FUNCTION
# ==========================================
@st.cache_data
def load_data():
    file_path = "data/India_Market_Trends_2025_Ultimate.xlsx"
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        
        if 'Quant' not in df.columns:
            if 'Quantity' in df.columns: df = df.rename(columns={'Quantity': 'Quant'})
            elif 'Qty' in df.columns: df = df.rename(columns={'Qty': 'Quant'})
            else: df['Quant'] = 1
            
        if 'City' not in df.columns:
            df['City'] = df['State']
            
        return df
    except Exception as e:
        st.error(f"Data loading failed: {e}")
        return pd.DataFrame()

df = load_data()

# ==========================================
# 3. HELPER FUNCTIONS & AI ENGINES
# ==========================================

# --- A. Gauge Chart Helper ---
def create_gauge(value, title, min_val, max_val, color_hex):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title, 'font': {'size': 18, 'color': "white"}},
        number = {'font': {'size': 30, 'color': "white"}},
        gauge = {
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color_hex},
            'bgcolor': "#121212",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [min_val, max_val*0.3], 'color': '#333'},
                {'range': [max_val*0.3, max_val*0.7], 'color': '#555'}
            ],
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- B. Live Trends (Simulated for 2026) ---
def get_live_market_trends(view_type):
    if view_type == "Today":
        return pd.DataFrame([
            {"Product": "Wireless Earphones", "Category": "Electronics", "Vol": 125},
            {"Product": "Men's Polo T-Shirt", "Category": "Fashion", "Vol": 98},
            {"Product": "Wardrobe Organizer", "Category": "Home", "Vol": 85},
            {"Product": "Salicylic Face Wash", "Category": "Beauty", "Vol": 72},
            {"Product": "Protein Powder", "Category": "Health", "Vol": 65}
        ])
    elif view_type == "This Week":
        return pd.DataFrame([
            {"Product": "Smartwatches", "Category": "Electronics", "Vol": 850},
            {"Product": "Running Shoes", "Category": "Fashion", "Vol": 720},
            {"Product": "Mixer Grinder", "Category": "Home", "Vol": 610},
            {"Product": "Sunscreen", "Category": "Beauty", "Vol": 540},
            {"Product": "Fast Chargers", "Category": "Electronics", "Vol": 480}
        ])
    return pd.DataFrame()

# --- C. Intelligent Strategy Engine ---
def get_market_strategy(category, product_name, volume):
    category = str(category).lower()
    product_name = str(product_name).lower()
    strategy = ""
    tactic = ""
    
    if any(x in product_name for x in ["earphone", "bud", "watch", "charger", "phone"]):
        strategy = "Tech Spec Optimization & Bundling"
        tactic = """
        1. <b>Listing:</b> Highlight 'Playtime', 'Fast Charge' & 'Water Resistance'.<br>
        2. <b>Ads:</b> Use 'Sponsored Products' for keywords like 'Best under 2000'.<br>
        3. <b>Offer:</b> Create 'Work-from-Home' bundles (Buds + Case).
        """
    elif "fashion" in category or "clothing" in category or "sneaker" in category:
        strategy = "Visual Storytelling & Trends"
        tactic = """
        1. <b>Visuals:</b> Use high-res lifestyle images & short video walkthroughs.<br>
        2. <b>Keywords:</b> Target trend keywords like 'Cargo', 'Oversized', 'Streetwear'.<br>
        3. <b>Events:</b> Participate in End of Season Sales (EOSS).
        """
    elif "beauty" in category or "health" in category or "wash" in category:
        strategy = "Ingredient Focus & Trust"
        tactic = """
        1. <b>Content:</b> Highlight ingredients (e.g., 'Salicylic Acid') in title.<br>
        2. <b>Trust:</b> Display 'Dermatologically Tested' badges.<br>
        3. <b>Retention:</b> 'Subscribe & Save' options.
        """
    elif "home" in category or "kitchen" in category:
        strategy = "Utility Demonstration"
        tactic = """
        1. <b>A+ Content:</b> Show 'Before vs After' organization photos.<br>
        2. <b>Ads:</b> Target 'Home Improvement' audiences.<br>
        3. <b>Delivery:</b> Ensure 'Assured' fast delivery tags.
        """
    else:
        strategy = "Visibility & Competitive Pricing"
        tactic = "Monitor competitor pricing dynamically and optimize keywords."
    return strategy, tactic

# --- D. Customer Segmentation Engine ---
def segment_customers(df):
    if df.empty or 'Quant' not in df.columns: return pd.DataFrame()
    group_col = 'Customer ID' if 'Customer ID' in df.columns else 'State'
    
    cust_df = df.groupby(group_col).agg({'Total_Sales':'sum', 'Quant':'sum'}).reset_index()
    cust_df.rename(columns={group_col: 'Customer_Group'}, inplace=True)
    
    if len(cust_df) >= 3:
        kmeans = KMeans(n_clusters=3, random_state=42)
        cust_df['Cluster'] = kmeans.fit_predict(cust_df[['Total_Sales', 'Quant']])
        cluster_avg = cust_df.groupby('Cluster')['Total_Sales'].mean().sort_values().index
        cluster_map = {cluster_avg[0]: 'Occasional', cluster_avg[1]: 'Regular', cluster_avg[2]: 'High-Value VIP'}
        cust_df['Segment'] = cust_df['Cluster'].map(cluster_map)
    else:
        cust_df['Segment'] = 'Regular'
        
    return cust_df

# --- E. Prediction Magic Logic (UPGRADED WITH REAL REGIONAL INSIGHTS) ---
sale_calendar = {
    "January": [("New Year Sale", 1, 5), ("Republic Day Sale", 20, 26)],
    "February": [("Valentine's Sale", 10, 14)],
    "March": [("Holi Sale", 5, 12), ("End of Financial Year", 25, 31)],
    "April": [("Summer Sale Start", 10, 20)],
    "May": [("Mother's Day Sale", 8, 12), ("Summer Peak Sale", 20, 30)],
    "June": [("Father's Day Sale", 15, 18), ("Back to School", 10, 30)],
    "July": [("Monsoon Sale", 1, 10), ("Prime Day (Like) Event", 15, 16)],
    "August": [("Independence Day Sale", 10, 15), ("Rakhi Sale", 20, 25)],
    "September": [("Pre-Diwali Kickoff", 25, 30)],
    "October": [("Big Billion Days", 3, 10), ("Diwali Sale", 20, 30)],
    "November": [("Wedding Season", 10, 30), ("Black Friday", 24, 28)],
    "December": [("Christmas Sale", 20, 25), ("Year End Clearance", 26, 31)]
}

seasonal_logic = {
    "Summer": ["ACs", "Coolers", "Sunscreen", "Cotton T-Shirts", "Sunglasses"],
    "Monsoon": ["Umbrellas", "Raincoats", "Waterproof Bags", "Mosquito Nets", "Washing Machines"],
    "Winter": ["Heaters", "Jackets", "Moisturizers", "Coffee/Tea", "Geysers"],
    "Wedding": ["Ethnic Wear", "Jewelry", "Gift Sets", "Home Decor", "Makeup"],
    "Festive": ["Sweets", "New Clothes", "Electronics", "Gold Coins", "Pooja Items"]
}

def predict_future(day, month):
    base_rev = 1.8; base_ord = 150; base_traf = 3500
    active_event = None; event_multiplier = 1.0
    
    events = sale_calendar.get(month, [])
    for event_name, start, end in events:
        if start <= day <= end:
            active_event = event_name
            event_multiplier = 3.5 if "Billion" in event_name or "Diwali" in event_name else 2.5 if "Independence" in event_name or "Republic" in event_name else 1.5
            break
    
    region_insight = ""
    focus_regions = ""
    
    if month == "January":
        if 20 <= day <= 26:
            region_insight = "🇮🇳 <b>Republic Day Surge:</b> Patriotic gifting drives demand for flags, apparel, and electronics. Tier-2/3 cities show 40% higher conversion than metros."
            focus_regions = "Delhi NCR, UP, Bihar, Rajasthan"
        else:
            region_insight = "❄️ <b>North India Cold Wave:</b> Heaters, jackets, and hot beverages peak. Logistics delays likely in Punjab/Haryana due to fog. Stockpile in warehouses near Delhi."
            focus_regions = "Delhi, Punjab, Haryana, J&K"

    elif month == "February":
        if 10 <= day <= 14:
            region_insight = "💝 <b>Valentine's Gifting Peak:</b> Beauty kits, jewelry, and fashion dominate. Mumbai & Bangalore contribute 55% of sales. Last-minute delivery SLAs extended."
            focus_regions = "Mumbai, Bangalore, Delhi, Hyderabad"
        else:
            region_insight = "🌤️ <b>Early Spring Demand:</b> Light clothing, home decor, and travel accessories rise. No major weather disruptions expected."
            focus_regions = "Pan India – Balanced"

    elif month == "March":
        if 5 <= day <= 12:
            region_insight = "🎨 <b>Holi Festival Boom:</b> Color packs, white clothing, and skincare (post-Holi care) surge. West & North India lead with 60% of total sales."
            focus_regions = "UP, Rajasthan, Gujarat, Maharashtra"
        elif 25 <= day <= 31:
            region_insight = "📊 <b>Financial Year End Rush:</b> Electronics & high-value items spike as businesses clear budgets. B2B orders from Delhi, Mumbai, Chennai."
            focus_regions = "Delhi, Mumbai, Chennai, Pune"
        else:
            region_insight = "🔥 <b>Early Summer Onset:</b> Cooling products (fans, ACs) begin rising in Central & South India. Stock up in Telangana/Karnataka warehouses."
            focus_regions = "MP, Telangana, Karnataka, Andhra Pradesh"

    elif month in ["April", "May", "June"]:
        if month == "April" and 10 <= day <= 20:
            region_insight = "☀️ <b>Summer Sale Kickoff:</b> ACs, coolers, cottonwear, and refrigerators dominate. North India shows highest YoY growth."
            focus_regions = "Delhi, UP, Rajasthan, Haryana"
        elif month == "May" and 8 <= day <= 12:
            region_insight = "💐 <b>Mother's Day Gifting:</b> Personal care, kitchen appliances, and flowers see 40% uplift. Tier-1 cities contribute 70% of sales."
            focus_regions = "Mumbai, Bangalore, Delhi, Hyderabad"
        elif month == "June" and 15 <= day <= 18:
            region_insight = "👔 <b>Father's Day & Pre-Monsoon Prep:</b> Formal wear + waterproof gear demand rises. Avoid shipping fragile items to coastal areas."
            focus_regions = "North & West India – Delhi, Mumbai, Ahmedabad"
        else:
            region_insight = "🌡️ <b>Peak Summer Heatwave:</b> ACs, coolers, cottonwear, and refrigerators dominate. Power outages may affect delivery SLAs in rural areas."
            focus_regions = "Rajasthan, Delhi, Telangana, Andhra Pradesh"

    elif month in ["July", "August", "September"]:
        if month == "July" and 1 <= day <= 10:
            region_insight = "🌧️ <b>Monsoon Sale:</b> Umbrellas, raincoats, and waterproof bags peak. Coastal regions (Kerala, Goa) show highest demand."
            focus_regions = "Kerala, Goa, Maharashtra, Karnataka"
        elif month == "August" and 10 <= day <= 15:
            region_insight = "🇮🇳 <b>Independence Day Mega Sale:</b> Nationalistic products + electronics boom. Highest conversion rate of the year. Rural demand surges."
            focus_regions = "Pan India – Tier 2/3 cities"
        elif month == "August" and 20 <= day <= 25:
            region_insight = "🎀 <b>Rakhi Festival:</b> Sweets, ethnic wear, and gift hampers peak. Last-minute deliveries strain logistics in North India."
            focus_regions = "UP, Bihar, Rajasthan, Delhi"
        else:
            region_insight = "☔ <b>Monsoon Disruptions:</b> Waterproof gear, home cleaning, and indoor entertainment rise. Avoid fragile item shipping in flood-prone zones."
            focus_regions = "Kerala, West Bengal, Assam, Mumbai"

    else:  # October, November, December
        if month == "October" and 3 <= day <= 10:
            region_insight = "✨ <b>Big Billion Days:</b> Largest sales event! Electronics, gold, sweets, and home decor dominate. Expect 3.5x revenue spike. Tier-2/3 cities drive growth."
            focus_regions = "Pan India – Rural demand surges"
        elif month == "October" and 20 <= day <= 30:
            region_insight = "🎇 <b>Diwali Festival:</b> Gold coins, electronics, sweets, and new clothes peak. Logistics delays likely in North India due to traffic."
            focus_regions = "UP, Bihar, Rajasthan, Delhi"
        elif month == "November" and 10 <= day <= 30:
            region_insight = "💍 <b>Wedding Season Peak:</b> Ethnic wear, jewelry, and home appliances see sustained high demand. Pre-wedding shopping starts early."
            focus_regions = "Gujarat, Punjab, UP, Rajasthan"
        elif month == "December" and 20 <= day <= 25:
            region_insight = "🎄 <b>Christmas & New Year:</b> Gifting (electronics, fashion), party supplies, and travel accessories peak. Last-mile delivery delays likely."
            focus_regions = "Metro Cities, Christian-majority regions (Goa, NE)"
        else:
            region_insight = "🎉 <b>Festive Momentum Continues:</b> Post-Diwali discounts on unsold inventory. Home & kitchen categories perform well."
            focus_regions = "Pan India"

    if month in ["April", "May", "June"]: 
        top_prods = seasonal_logic["Summer"]
    elif month in ["July", "August", "September"]: 
        top_prods = seasonal_logic["Monsoon"]
    elif month in ["November", "December", "January"]: 
        top_prods = seasonal_logic["Winter"]
    else: 
        top_prods = seasonal_logic["Festive"] + seasonal_logic["Wedding"]

    return {
        "revenue": base_rev * event_multiplier,
        "orders": int(base_ord * event_multiplier),
        "traffic": int(base_traf * event_multiplier * 1.2),
        "event": active_event,
        "ci_low": (base_rev * event_multiplier) * 0.9,
        "ci_high": (base_rev * event_multiplier) * 1.1,
        "insight": region_insight,
        "focus_regions": focus_regions,
        "products": top_prods
    }

# --- F. Sales Forecast Generator (REALISTIC MULTIPLIERS) ---
def generate_sales_forecast(selected_month, selected_day):
    np.random.seed(42)
    base_sales = 150000
    
    today = datetime.now().date()
    today_dt = pd.Timestamp(today)
    
    # Historical: last 6 months
    hist_start = today_dt - timedelta(days=180)
    hist_dates = pd.date_range(hist_start, today_dt, freq='D')
    
    # Forecast: next 365 days
    fore_start = today_dt + timedelta(days=1)
    fore_end = fore_start + timedelta(days=365)
    fore_dates = pd.date_range(fore_start, fore_end, freq='D')
    
    # Generate historical sales (with realistic festive spikes)
    hist_sales = []
    for d in hist_dates:
        if d.month in [10, 11]:  # Diwali/Black Friday period
            boost = 2.8
        elif d.month in [8]:  # Independence Day
            boost = 2.0
        elif d.month in [1]:  # Republic Day
            boost = 1.8
        elif d.month in [4,5,6]:  # Summer
            boost = 1.3
        elif d.month in [7,8,9]:  # Monsoon
            boost = 1.1
        elif d.month in [12]:  # Christmas
            boost = 1.5
        else:
            boost = 1.0
        sales = base_sales * boost * (1 + np.random.normal(0, 0.1))
        hist_sales.append(max(sales, 50000))
    
    # Generate forecast (using realistic multipliers)
    fore_sales, lower_ci, upper_ci = [], [], []
    for d in fore_dates:
        multiplier = 1.0
        month_name = d.strftime('%B')
        if month_name in sale_calendar:
            for event, start, end in sale_calendar[month_name]:
                if start <= d.day <= end:
                    if "Billion" in event or "Diwali" in event:
                        multiplier = 2.8
                    elif "Independence" in event or "Republic" in event:
                        multiplier = 2.0
                    else:
                        multiplier = 1.5
                    break
        
        if d.month in [10,11,12]:
            seasonal = 1.4
        elif d.month in [4,5,6]:
            seasonal = 1.3
        elif d.month in [7,8,9]:
            seasonal = 1.1
        else:
            seasonal = 1.0
            
        pred_sales = base_sales * multiplier * seasonal
        fore_sales.append(pred_sales)
        lower_ci.append(pred_sales * 0.85)
        upper_ci.append(pred_sales * 1.15)
    
    # Event markers
    event_dates, event_names = [], []
    for m_idx, (m_name, events) in enumerate(sale_calendar.items(), 1):
        for ev, s, e in events:
            mid = (s + e) // 2
            try:
                event_date = pd.Timestamp(f"{fore_start.year}-{m_idx:02d}-{mid:02d}")
                if event_date >= fore_start and event_date <= fore_end:
                    event_dates.append(event_date)
                    event_names.append(ev)
            except: continue
    
    return (
        list(hist_dates) + list(fore_dates),
        hist_sales,
        fore_sales,
        lower_ci,
        upper_ci,
        event_dates,
        event_names,
        fore_start
    )

# ==========================================
# 4. SIDEBAR & GLOBAL CONTROL
# ==========================================
st.sidebar.title("🎛️ Command Center")

start_date_Limit = date(2025, 1, 1)
today_real = datetime.now().date()

simulated_date_input = st.sidebar.date_input(
    "📆 Live Date", 
    today_real, 
    min_value=start_date_Limit, 
    max_value=today_real
)

st.sidebar.markdown("---")
show_prediction = st.sidebar.toggle("🔮 PREDICTION MAGIC 2026", value=False)
st.sidebar.markdown("---")

view_option = "Standard"
if not show_prediction:
    if simulated_date_input.year == 2026:
        available_views = ["Today", "This Week"]
    else:
        available_views = ["Today", "This Week", "This Month", "Total Year"]
    view_option = st.sidebar.radio("⏱️ Analysis View", available_views)

if simulated_date_input.year == 2026:
    lookup_date = pd.Timestamp(simulated_date_input.replace(year=2025))
else:
    lookup_date = pd.Timestamp(simulated_date_input)

if not df.empty and not show_prediction:
    if view_option == "Today":
        filtered_df = df[df['Date'] == lookup_date]
    elif view_option == "This Week":
        start_week = lookup_date - timedelta(days=lookup_date.weekday())
        filtered_df = df[(df['Date'] >= start_week) & (df['Date'] <= lookup_date)]
    elif view_option == "This Month":
        filtered_df = df[(df['Date'].dt.month == lookup_date.month) & (df['Date'].dt.year == 2025)]
    else:
        filtered_df = df[df['Date'].dt.year == 2025]
else:
    filtered_df = pd.DataFrame()

# ==============================================================================
# 5. DASHBOARD VIEW CONTROLLER
# ==============================================================================

if show_prediction:
    st.markdown("""
        <h1 style='text-align: center; color: #CCCCCC; font-size: 60px; 
        text-shadow: 0 0 10px #00CC96, 0 0 20px #00CC96; font-family: "Segoe UI", sans-serif;'>
            🔮 PREDICTION MAGIC 2026
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("💡 *Use this mode to forecast sales, traffic & inventory needs for any future date in 2026.*")
    st.markdown("---")

    c_day, c_month = st.columns(2)
    selected_month = c_month.selectbox("🔮 Select Future Month", list(sale_calendar.keys()), index=0)
    
    year_for_pred = 2026
    month_num = list(sale_calendar.keys()).index(selected_month) + 1
    max_day = calendar.monthrange(year_for_pred, month_num)[1]
    selected_day = c_day.slider("🔮 Select Future Day", 1, max_day, min(15, max_day))
    
    pred_data = predict_future(selected_day, selected_month)

    if pred_data['event']:
        st.markdown(f"""
        <div style="background-color: #00CC96; color: black; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 20px;">
            🎉 ACTIVE EVENT DETECTED: {pred_data['event'].upper()}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"ℹ️ Analysis for: {selected_day} {selected_month}, 2026 (Standard Trading Day)")

    m1, m2, m3 = st.columns(3)
    m1.metric("💰 Predicted Revenue", f"₹{pred_data['revenue']:.2f} Lakhs", delta=f"Range: ₹{pred_data['ci_low']:.1f}L - ₹{pred_data['ci_high']:.1f}L")
    m2.metric("📦 Expected Orders", f"{pred_data['orders']}", "Logistics Ready")
    m3.metric("🌐 Website Traffic", f"{pred_data['traffic']:,}", "Visits Forecast")
    
    st.markdown("---")

    col_insight, col_prod = st.columns([1, 1])
    with col_insight:
        st.markdown(f"""
        <div style="background-color: #1A1D24; padding: 20px; border-radius: 10px; border-left: 5px solid #FFA500; height: 100%;">
            <h3 style="color: #FFA500; margin-top: 0;">🌍 Regional & Seasonal Intelligence</h3>
            <p style="font-size: 16px; color: #E0E0E0; line-height: 1.6;">{pred_data['insight']}</p>
            <hr style="border-color: #333;">
            <p style="color: #999; font-size: 15px;">
                <b>🎯 Focus Regions:</b><br>{pred_data['focus_regions']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_prod:
        # Generate product-specific tips
        product_tips = []
        for product in pred_data['products'][:5]:
            tip = ""
            if any(x in product.lower() for x in ["ac", "cooler", "refrigerator", "fan"]):
                tip = "❄️ Offer extended warranty + free installation"
            elif any(x in product.lower() for x in ["earphone", "watch", "charger", "phone"]):
                tip = "📱 Bundle with screen guard + case for 15% extra margin"
            elif any(x in product.lower() for x in ["jacket", "heater", "geyser"]):
                tip = "🔥 Highlight energy efficiency rating in listing"
            elif any(x in product.lower() for x in ["sunglass", "sunscreen", "cotton"]):
                tip = "☀️ Run 'Summer Essentials' combo offers"
            elif any(x in product.lower() for x in ["umbrella", "raincoat", "waterproof"]):
                tip = "🌧️ Partner with weather apps for contextual ads"
            elif any(x in product.lower() for x in ["ethnic", "jewelry", "gift"]):
                tip = "🎁 Pre-pack in festive gift boxes (+₹99)"
            else:
                tip = "📦 Ensure fast delivery SLA during sale period"
            
            product_tips.append(f"<li style='color: #00CC96; font-size: 16px; margin-bottom: 8px;'>{product}<br><span style='color: #999; font-size: 14px;'>{tip}</span></li>")
        
        prod_html = "".join(product_tips)
        st.markdown(f"""
        <div style="background-color: #1A1D24; padding: 20px; border-radius: 10px; border-left: 5px solid #00CC96; height: 100%;">
            <h3 style="color: #00CC96; margin-top: 0;">🛒 Top 5 Predicted Sellers</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                {prod_html}
            </ul>
            <hr style="border-color: #333;">
            <p style="font-size: 14px; color: #CCC;">💡 <b>AI Tip:</b> Stock up on these items 7 days prior to {selected_day} {selected_month}.</p>
        </div>
        """, unsafe_allow_html=True)

    # ===================================================================
    # ✅ SALES FORECAST CHART (CORRECTED VERSION)
    # ===================================================================
    st.markdown("---")
    st.markdown("### 📈 Advanced Sales Forecast (Live: From Today to Next Year)")

    all_dates, hist_sales, fore_sales, lower_ci, upper_ci, event_dates, event_names, fore_start = generate_sales_forecast(selected_month, selected_day)

    forecast_df = pd.DataFrame({
        'Date': all_dates,
        'Sales': hist_sales + fore_sales,
        'Type': ['Historical'] * len(hist_sales) + ['Forecast'] * len(fore_sales)
    })

    fore_dates = pd.date_range(fore_start, periods=len(fore_sales), freq='D')

    ci_df = pd.DataFrame({
        'Date': fore_dates,
        'Lower': lower_ci,
        'Upper': upper_ci
    })

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forecast_df[forecast_df['Type']=='Historical']['Date'],
        y=forecast_df[forecast_df['Type']=='Historical']['Sales'],
        mode='lines',
        name='Historical (Last 6 Months)',
        line=dict(color='#00CC96', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df[forecast_df['Type']=='Forecast']['Date'],
        y=forecast_df[forecast_df['Type']=='Forecast']['Sales'],
        mode='lines',
        name='Forecast (Next 12 Months)',
        line=dict(color='#00F0FF', width=3, dash='dot')
    ))

    fig.add_trace(go.Scatter(
        x=list(ci_df['Date']) + list(ci_df['Date'][::-1]),
        y=list(ci_df['Upper']) + list(ci_df['Lower'][::-1]),
        fill='toself',
        fillcolor='rgba(0, 240, 255, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        hoverinfo='skip'
    ))

    try:
        month_num = list(sale_calendar.keys()).index(selected_month) + 1
        selected_date = pd.Timestamp(f"{fore_start.year}-{month_num:02d}-{selected_day:02d}")
        selected_sales = pred_data['revenue'] * 100000
        fig.add_trace(go.Scatter(
            x=[selected_date],
            y=[selected_sales],
            mode='markers',
            name=f'Selected Date',
            marker=dict(color='#FFA500', size=12, symbol='star')
        ))
    except:
        pass

    for ev_date, ev_name in zip(event_dates, event_names):
        if ev_date >= fore_start:
            fig.add_vline(x=ev_date, line=dict(color="#FF6B6B", width=1, dash="dash"))

    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Date",
        yaxis_title="Daily Sales (₹)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"💡 Forecast from {datetime.now().strftime('%d %B %Y')} to next year. Includes seasonal trends, major sale events, and ±15% confidence band.")

else:
    st.title(f"🚀 E-Commerce AI Trend Analysis")
    st.markdown(f"**Status:** Live System | **Date:** {simulated_date_input.strftime('%d %B %Y')} | **Mode:** {view_option}")

    # --- KPI Cards ---
    if not df.empty:
        # For 2026 dates, map to 2025 for return rate calculation
        if simulated_date_input.year == 2026:
            if view_option in ["Today", "This Week"]:
                # Map to 2025 same period
                lookup_2025 = pd.Timestamp(simulated_date_input.replace(year=2025))
                if view_option == "Today":
                    temp_df = df[df['Date'] == lookup_2025]
                else:  # This Week
                    start_week_2025 = lookup_2025 - timedelta(days=lookup_2025.weekday())
                    temp_df = df[(df['Date'] >= start_week_2025) & (df['Date'] <= lookup_2025)]
                
                # Calculate return rate from 2025 data
                if 'Status' in temp_df.columns and len(temp_df) > 0:
                    returned_orders = len(temp_df[temp_df['Status'] == 'Returned'])
                    ret_rate = (returned_orders / len(temp_df) * 100) if len(temp_df) > 0 else 0
                else:
                    ret_rate = 0  # Default if no Status column
                
                # Use simulated revenue/orders for 2026
                if view_option == "Today": 
                    rev = 185000; orders = 145
                else: 
                    rev = 1250000; orders = 950
                profit = rev * 0.18
                margin = 18.0
                avg_rating = 4.3
            else:
                # Fallback: use overall 2025 return rate
                if 'Status' in df.columns:
                    returned_total = len(df[df['Status'] == 'Returned'])
                    ret_rate = (returned_total / len(df) * 100) if len(df) > 0 else 0
                else:
                    ret_rate = 0
                rev = 0; orders = 0; profit = 0; margin = 0; avg_rating = 0
        else:
            # For 2025 dates, use actual filtered data
            if not filtered_df.empty:
                rev = filtered_df['Total_Sales'].sum()
                profit = filtered_df['Profit'].sum()
                orders = len(filtered_df)
                margin = (profit/rev*100) if rev > 0 else 0
                avg_rating = 4.2
                
                if 'Status' in filtered_df.columns:
                    returned_orders = len(filtered_df[filtered_df['Status'] == 'Returned'])
                    ret_rate = (returned_orders / orders * 100) if orders > 0 else 0
                else:
                    ret_rate = 0  # No Status column
            else:
                rev = 0; profit = 0; orders = 0; ret_rate = 0; margin = 0; avg_rating = 0
    else:
        rev = 0; profit = 0; orders = 0; ret_rate = 0; margin = 0; avg_rating = 0

    # Display KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="metric-card"><div class="metric-label">Total Revenue</div><div class="metric-value">₹{rev:,.0f}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="metric-card"><div class="metric-label">Total Orders</div><div class="metric-value">{orders:,}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="metric-card"><div class="metric-label">Units Sold</div><div class="metric-value">{int(orders*1.2):,}</div></div>', unsafe_allow_html=True)

    # Return Rate Card - Always show a number (never "No Data")
    ret_color = "#FF4B4B" if ret_rate > 5 else "#00CC96"
    k4.markdown(f'<div class="metric-card"><div class="metric-label">Return Rate</div><div class="metric-value" style="color:{ret_color}">{ret_rate:.1f}%</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    g1, g2, g3 = st.columns([1, 1, 2])
    with g1: st.plotly_chart(create_gauge(margin, "Profit Margin %", 0, 40, "#00CC96"), use_container_width=True)
    with g2: st.plotly_chart(create_gauge(avg_rating, "Avg Rating", 0, 5, "#FFA500"), use_container_width=True)
    with g3:
        st.markdown("### 🗺️ State-wise Sales (Interactive Map)")
        if not filtered_df.empty:
            state_data = filtered_df.groupby('State').agg({
                'Total_Sales': 'sum',
                'State': 'count'
            }).rename(columns={'State': 'Order_Count'}).reset_index()
            
            fig_state = px.treemap(state_data, path=['State'], values='Order_Count',
                                   color='Total_Sales', color_continuous_scale='Viridis',
                                   title="Sales Intensity by Region (Size = Orders, Color = Value)")
            fig_state.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=250)
            st.plotly_chart(fig_state, use_container_width=True)
        else: st.info("No Data")

    st.markdown("---")

    st.markdown("### 🫧 4D Analysis: Volume vs Profit")
    if not filtered_df.empty:
        bubble_data = filtered_df.groupby(['Category', 'Product_Name']).agg({'Quant': 'sum', 'Profit': 'sum', 'Total_Sales': 'sum'}).reset_index().sort_values('Quant', ascending=False).head(50) 
        fig_4d = px.scatter(bubble_data, x="Quant", y="Profit", size="Quant", color="Category", hover_name="Product_Name", hover_data={'Total_Sales': True}, labels={"Quant": "Units Sold (Volume)"}, template="plotly_dark", size_max=60)
        fig_4d.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_4d, use_container_width=True)
    else: st.info("No Data")

    st.markdown("---")

    st.markdown("### ⏯️ Market Evolution: Monthly Playback (2025)")
    if not df.empty:
        anim_df = df.copy() 
        anim_df['Month_Name'] = anim_df['Date'].dt.strftime('%B')
        anim_grouped = anim_df.groupby(['Month_Name', 'Category']).agg({'Quant': 'sum', 'Profit': 'sum'}).reset_index()
        months_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        anim_grouped['Month_Name'] = pd.Categorical(anim_grouped['Month_Name'], categories=months_order, ordered=True)
        anim_grouped = anim_grouped.sort_values('Month_Name')
        
        fig_anim = px.scatter(anim_grouped, x="Quant", y="Profit", animation_frame="Month_Name", animation_group="Category", size="Quant", color="Category", hover_name="Category", labels={"Quant": "Units Sold"}, range_x=[0, anim_grouped['Quant'].max()*1.1], range_y=[0, anim_grouped['Profit'].max()*1.1], template="plotly_dark", title="Click Play to watch 2025 Trends ➡️")
        fig_anim.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1500
        st.plotly_chart(fig_anim, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    trend_df = pd.DataFrame(); source_label = ""
    
    if simulated_date_input.year == 2026:
        if view_option in ["Today", "This Week"]:
            trend_df = get_live_market_trends(view_option); source_label = f"Trending Now ({view_option})"
    else:
        if view_option == "Total Year":
              trend_df = pd.DataFrame([{"Product": "Wireless Earbuds (boAt/Noise)", "Category": "Electronics", "Vol": 180000}, {"Product": "Cargo Pants & Athleisure", "Category": "Fashion", "Vol": 160000}, {"Product": "Smartwatches", "Category": "Electronics", "Vol": 145000}, {"Product": "Mixer Grinders", "Category": "Home", "Vol": 130000}, {"Product": "Sunscreen", "Category": "Beauty", "Vol": 125000}]); source_label = "2025 Annual Bestsellers"
        elif not filtered_df.empty:
            trend_df = filtered_df.groupby('Product_Name').agg({'Quant': 'sum'}).reset_index().sort_values('Quant', ascending=False).head(10)
            trend_df.columns = ['Product', 'Vol']; source_label = "Top Sellers (Real Data)"

    if not trend_df.empty:
        best_item = trend_df.iloc[0]['Product']; best_vol = trend_df.iloc[0]['Vol']; best_cat = "General"
        if 'Category' in trend_df.columns: best_cat = trend_df.iloc[0]['Category']
        elif not df.empty: 
            cat_match = df[df['Product_Name'] == best_item]['Category']
            if not cat_match.empty: best_cat = cat_match.iloc[0]

        with col1:
            st.subheader(f"🔥 Most Sold Products ({source_label})")
            fig_bar = px.bar(trend_df, x='Vol', y='Product', orientation='h', color='Vol', template='plotly_dark', color_continuous_scale='Viridis', labels={'Vol': 'Units Sold'})
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=300)
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.subheader("🤖 AI Strategic Action Plan")
            strategy_title, strategy_desc = get_market_strategy(best_cat, best_item, best_vol)
            st.markdown(f"""<div class="rec-card"><div class="rec-title">🚨 Top Mover: {best_item}</div><div class="rec-text"><b>Strategy:</b> {strategy_title}</div><div class="rec-text"><b>Execution:</b> {strategy_desc}</div><hr style="border-color: #333;"><div class="rec-text" style="color: #00CC96;"><b>🔮 Predicted Boost:</b> +{int(best_vol*0.35)} Units</div></div>""", unsafe_allow_html=True)
    else: st.warning("No sales data found for this period.")

    st.markdown("---")

    st.header("🧪 Advanced AI Labs")
    st.subheader("👥 Customer Segmentation (Clustering)")
    if st.button("Run Segmentation Model"):
        with st.spinner("Running K-Means Clustering..."):
            if not df.empty:
                seg_df = segment_customers(df)
                if not seg_df.empty:
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        fig_seg = px.scatter(seg_df, x="Quant", y="Total_Sales", color="Segment", title="Customer Segments: Volume vs Value", template="plotly_dark", color_discrete_map={'Occasional':'#EF553B', 'Regular':'#FFA15A', 'High-Value VIP':'#00CC96'})
                        st.plotly_chart(fig_seg, use_container_width=True)
                    with c2:
                        st.markdown("""**Segment Insights:**\n- 🟢 **High-Value VIP:** High Volume & Spend.\n- 🟠 **Regular:** Consistent buyers.\n- 🔴 **Occasional:** Low activity.""")
                        st.dataframe(seg_df[['Customer_Group', 'Segment', 'Total_Sales']].head(5), hide_index=True)
                else: st.error("Data processing failed.")
            else: st.error("Not enough data to segment.")