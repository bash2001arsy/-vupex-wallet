import streamlit as st
import requests
import json
import os
import uuid

# --- 1. إعدادات المنصة ---
st.set_page_config(page_title="Vupex App", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. ستايل "الأزرار السفلية" (Bottom Nav Style) ---
st.markdown("""
<style>
    /* تصفير الهوامش */
    .main { background-color: #0d1117; padding-bottom: 100px !important; }
    
    /* ستايل المستطيل السفلي (الأزرار) */
    .nav-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 500px;
        background: rgba(22, 27, 34, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid #30363d;
        border-radius: 20px;
        display: flex;
        justify-content: space-around;
        padding: 10px;
        z-index: 9999;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* تنسيق كل زر داخل المستطيل */
    .nav-item {
        text-align: center;
        color: #8b949e;
        font-size: 10px;
        flex: 1;
        cursor: pointer;
    }
    .nav-item i { font-size: 20px; display: block; margin-bottom: 2px; }
    .nav-item.active { color: #2ea043; }

    /* إخفاء القائمة الجانبية وأزرار Streamlit الافتراضية */
    [data-testid="stSidebar"] { display: none; }
    header {visibility: hidden;}
    
    /* تنسيق الكروت لتكون متجاوبة */
    .stMetric { background-color: #161b22 !important; border: 1px solid #30363d !important; border-radius: 15px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. إدارة الجلسة والتنقل ---
if 'auth' not in st.session_state: st.session_state.auth = None
if 'page' not in st.session_state: st.session_state.page = "home"

def set_page(pg):
    st.session_state.page = pg

# --- 4. واجهة الدخول ---
if st.session_state.auth is None:
    st.markdown("<h2 style='text-align:center;'>💎 VUPEX LOGIN</h2>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            st.session_state.auth = {"u": u, "balance": 0.0}
            st.rerun()

# --- 5. المنصة (بعد الدخول) ---
else:
    # --- [A] الهيكل العلوي (Header) ---
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px;">
            <div style="font-size: 20px; font-weight: bold; color: #58a6ff;">VUPEX</div>
            <div style="background: #161b22; padding: 5px 15px; border-radius: 20px; font-size: 12px; border: 1px solid #30363d;">
                ID: {str(uuid.uuid4())[:8].upper()} 👤
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- [B] محتوى الصفحات ---
    if st.session_state.page == "home":
        st.markdown("### الرئيسية")
        st.metric("Total Balance", f"$ {st.session_state.auth['balance']:.2f}")
        
        # كروت الأسعار (متجاوبة)
        c1, c2 = st.columns(2)
        with c1: st.markdown("<div style='background:#161b22; padding:15px; border-radius:10px; border:1px solid #30363d;'>BTC/USDT<br><b style='color:#2ea043;'>$67,230.12</b></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div style='background:#161b22; padding:15px; border-radius:10px; border:1px solid #30363d;'>ETH/USDT<br><b style='color:#2ea043;'>$3,412.50</b></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        # أزرار الوصول السريع (مربعات مثل الصورة)
        b1, b2, b3, b4 = st.columns(4)
        with b1: st.button("📥\nإيداع", on_click=set_page, args=("assets",))
        with b2: st.button("📤\nسحب", on_click=set_page, args=("assets",))
        with b3: st.button("🔄\nصرف", on_click=set_page, args=("home",))
        with b4: st.button("💬\nدعم", on_click=set_page, args=("home",))

    elif st.session_state.page == "trade":
        st.header("الأسواق والصفقات")
        st.components.v1.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&theme=dark" width="100%" height="400" frameborder="0"></iframe>', height=400)

    elif st.session_state.page == "assets":
        st.header("الأصول")
        st.write("إيداع USDT (TRC20)")
        st.code("T-Example-Wallet-Address-123456")

    # --- [C] القائمة السفلية (المستطيل العائم) ---
    # ملاحظة: استخدمنا أزرار Streamlit حقيقية داخل الـ Container لضمان بقاء الجلسة
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) # فراغ عشان الأزرار ما تغطي المحتوى
    
    # نستخدم Columns داخل الـ Fixed Container
    # بفضل الـ CSS فوق، هذه الأزرار رح تطلع مرتبة جوا المستطيل
    footer = st.container()
    with footer:
        cols = st.columns(4)
        with cols[0]: st.button("🏠", help="الرئيسية", on_click=set_page, args=("home",), key="nav_h")
        with cols[1]: st.button("📊", help="الأسواق", on_click=set_page, args=("trade",), key="nav_m")
        with cols[2]: st.button("🎯", help="الصفقات", on_click=set_page, args=("trade",), key="nav_t")
        with cols[3]: st.button("💰", help="الأصول", on_click=set_page, args=("assets",), key="nav_a")
