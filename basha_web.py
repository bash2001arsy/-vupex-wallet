import streamlit as st
import requests
import json
import os
import uuid

# --- 1. إعدادات المنصة ---
st.set_page_config(
    page_title="Vupex Global | Real Trade", 
    page_icon="💎", 
    layout="wide", # هذا الخيار ضروري جداً لجعل الموقع يملأ الشاشة على الكمبيوتر
    initial_sidebar_state="collapsed"
)

# --- 2. ستايل "التجاوب الذكي" (Responsive CSS) ---
st.markdown("""
<style>
    /* جعل الحاوية الأساسية مرنة */
    .main { background-color: #0d1117; color: #e1e1e1; }
    
    /* تنسيق العناصر لتناسب الموبايل والكمبيوتر */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 calc(25% - 1rem) !important; /* يتوسع على الكمبيوتر ويتقلص على الموبايل */
        min-width: 150px !important;
    }

    /* هيدر متجاوب */
    .app-header {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        padding: 5% 2%;
        border-radius: 0 0 25px 25px;
        text-align: center;
        border-bottom: 1px solid #30363d;
        margin-bottom: 20px;
    }

    /* بطاقات الأسعار - مرنة */
    .ticker-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #30363d;
        text-align: center;
        margin: 5px;
    }

    /* تحسين شكل الأزرار للمس بالهاتف والضغط بالماوس */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background-color: #1c232d;
        color: white;
        border: 1px solid #30363d;
        height: 60px !important; /* طول مناسب للإبهام على الهاتف */
        font-weight: bold;
        font-size: 16px;
    }

    /* إخفاء القائمة الجانبية تماماً لمنع "الخبصة" */
    [data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. محرك الأسعار الحية (Binance API) ---
def get_live_prices():
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=2).json()
        target = ['BTCUSDT', 'ETHUSDT', 'TRXUSDT', 'SOLUSDT']
        return {item['symbol']: float(item['price']) for item in res if item['symbol'] in target}
    except:
        return {"BTCUSDT": 0.0, "ETHUSDT": 0.0, "TRXUSDT": 0.0, "SOLUSDT": 0.0}

# --- 4. إدارة البيانات والجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = None
if 'page' not in st.session_state: st.session_state.page = "home"

# --- 5. واجهة الدخول المتجاوبة ---
if st.session_state.auth is None:
    st.markdown("<div class='app-header'><h1>💎 VUPEX GLOBAL</h1><p>Real-Time Professional Trading</p></div>", unsafe_allow_html=True)
    # استخدام columns تجعل النموذج يتركز في المنتصف على الكمبيوتر ويأخذ كامل الشاشة على الموبايل
    _, col_mid, _ = st.columns([1, 4, 1])
    with col_mid:
        st.text_input("Username", key="u_in")
        st.text_input("Password", type="password", key="p_in")
        if st.button("Enter Platform"):
            # (منطق الدخول المعتاد)
            st.session_state.auth = {"u": st.session_state.u_in, "balance": 0.0, "wallet": "T-XYZ-123"}
            st.rerun()

# --- 6. المنصة الرئيسية (متجاوبة تماماً) ---
else:
    u = st.session_state.auth
    prices = get_live_prices()

    # القائمة السفلية "العائمة" (تتناسب مع الموبايل والكمبيوتر)
    # على الكمبيوتر ستظهر بجانب بعضها، وعلى الموبايل ستصغر تلقائياً
    nav = st.columns(4)
    with nav[0]: st.button("🏠", on_click=lambda: st.session_state.update({"page":"home"}))
    with nav[1]: st.button("📊", on_click=lambda: st.session_state.update({"page":"mkt"}))
    with nav[2]: st.button("🎯", on_click=lambda: st.session_state.update({"page":"trd"}))
    with nav[3]: st.button("💰", on_click=lambda: st.session_state.update({"page":"ast"}))

    st.divider()

    # --- محتوى الصفحات ---
    if st.session_state.page == "home":
        st.markdown(f"### Welcome, {u['u']}")
        st.metric("Total Balance", f"$ {u['balance']:.2f}")

        # عرض الأسعار بشكل متجاوب (4 أعمدة)
        # على الموبايل ستتحول تلقائياً لـ 1 أو 2 أعمدة حسب العرض
        p_cols = st.columns(4)
        coins = [("BTC", "BTCUSDT"), ("ETH", "ETHUSDT"), ("TRX", "TRXUSDT"), ("SOL", "SOLUSDT")]
        for i, (name, sym) in enumerate(coins):
            with p_cols[i]:
                st.markdown(f"<div class='ticker-card'>{name}<br><span style='color:#2ea043; font-weight:bold;'>${prices[sym]:,}</span></div>", unsafe_allow_html=True)

        st.markdown("### Quick Actions")
        # أزرار كبيرة للموبايل
        a_cols = st.columns(2)
        with a_cols[0]: st.button("📥 Deposit", key="d1")
        with a_cols[1]: st.button("👥 Invite", key="r1")

    elif st.session_state.page == "ast":
        st.header("Wallet Assets")
        st.info("USDT TRC20 Address:")
        st.code(u['wallet'], language="text")
        # الصورة ستصغر تلقائياً على الموبايل بفضل use_container_width
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={u['wallet']}", use_container_width=False)

    elif st.session_state.page == "trd":
        st.header("Trading Terminal")
        # جعل الشارت يتوسع ليملأ الشاشة
        st.components.v1.html(f"""
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&theme=dark" width="100%" height="400" frameborder="0"></iframe>
        """, height=410)
