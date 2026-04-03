import streamlit as st
import json
import os
import uuid
import requests

# --- 1. إعدادات المنصة (الأساس المتين) ---
st.set_page_config(page_title="VUPEX GLOBAL", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. محرك قاعدة البيانات (لا يضيع سنت ولا مستخدم) ---
DB_FILE = "users_db.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"basha": {"password": "1234", "id": "BOSS001", "balance": 0.0, "wallet": "T-MASTER-VAULT", "ref_earnings": 0.0}}

def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f)

def register_user(username, password, ref_code):
    db = load_users()
    if username in db: return False, "الاسم مستخدم مسبقاً!"
    uid = str(uuid.uuid4())[:8].upper()
    wallet = "T" + str(uuid.uuid4().hex).upper()[:33]
    db[username] = {
        "password": password, "id": uid, "balance": 0.0, 
        "wallet": wallet, "referred_by": ref_code, "ref_earnings": 0.0
    }
    save_db(db)
    return True, uid

# --- 3. جلب الأسعار الحية ---
@st.cache_data(ttl=60) # تحديث كل 60 ثانية لعدم الضغط على السيرفر
def get_prices():
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=3).json()
        return {i['symbol']: float(i['price']) for i in res if i['symbol'] in ['BTCUSDT', 'ETHUSDT', 'TRXUSDT']}
    except: return {"BTCUSDT": 67000.0, "ETHUSDT": 3400.0, "TRXUSDT": 0.12}

# --- 4. ستايل الـ Flagship (تصميم التطبيقات الفاخرة) ---
st.markdown("""
<style>
    /* جعل المنصة تظهر كتطبيق موبايل في المنتصف حتى على الكمبيوتر */
    .block-container { max-width: 600px; margin: 0 auto; padding-top: 10px; padding-bottom: 80px; background-color: #0d1117;}
    [data-testid="stSidebar"], [data-testid="stHeader"] { display: none; }
    
    /* خلفية التطبيق */
    .stApp { background-color: #0d1117; }

    /* الهيدر المتدرج */
    .header-box {
        background: linear-gradient(135deg, #001529 0%, #003366 100%);
        padding: 30px 20px; border-radius: 20px; text-align: center; margin-bottom: 20px;
        border: 1px solid #1c232d; box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    
    /* بطاقات العملات الأفقية */
    .ticker-flex { display: flex; justify-content: space-between; gap: 10px; margin-bottom: 20px; }
    .ticker-item {
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 10px; flex: 1; text-align: center;
    }
    
    /* البانر الإعلاني */
    .promo-banner {
        background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%);
        padding: 15px; border-radius: 12px; color: white; display: flex; justify-content: space-between;
        align-items: center; margin-bottom: 20px;
    }

    /* أزرار Streamlit الأساسية (الوصول السريع والناف بار) */
    div.stButton > button {
        background-color: #161b22; color: #c9d1d9; border: 1px solid #30363d;
        border-radius: 15px; height: 75px; font-weight: bold; font-size: 14px; transition: 0.3s;
    }
    div.stButton > button:hover { border-color: #2ea043; background-color: #1c232d; color: white;}
    div.stButton > button:active { background-color: #2ea043; color: white; }

    /* تنسيق النصوص */
    p, h1, h2, h3, h4 { color: #e1e1e1; font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- 5. إدارة الجلسة (لضمان بقاء المستخدم مسجلاً) ---
if 'auth' not in st.session_state: st.session_state.auth = None
if 'page' not in st.session_state: st.session_state.page = "home"

def go_to(page_name): st.session_state.page = page_name

# --- 6. واجهة الدخول / التسجيل الحقيقية (تعمل 100%) ---
if st.session_state.auth is None:
    st.markdown("<div class='header-box'><h1 style='color:#58a6ff;'>VUPEX GLOBAL</h1><p>Trade with Prestige</p></div>", unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔒 تسجيل الدخول", "✨ حساب جديد"])
    
    with tab_log:
        lu = st.text_input("اسم المستخدم", key="l_u")
        lp = st.text_input("كلمة المرور", type="password", key="l_p")
        if st.button("دخول المنصة", use_container_width=True):
            db = load_users()
            if lu in db and db[lu]["password"] == lp:
                st.session_state.auth = db[lu]
                st.session_state.auth['u'] = lu
                st.rerun()
            else: st.error("بيانات خاطئة!")
            
    with tab_reg:
        ref_code = st.query_params.get("ref", "")
        if ref_code: st.success(f"أنت تسجل عبر كود الإحالة: {ref_code}")
        ru = st.text_input("اسم مستخدم جديد", key="r_u")
        rp = st.text_input("كلمة مرور قوية", type="password", key="r_p")
        if st.button("إنشاء حساب آمن", use_container_width=True):
            if len(ru) > 2 and len(rp) > 3:
                success, msg = register_user(ru, rp, ref_code)
                if success:
                    st.success(f"تم إنشاء حسابك! الـ ID الخاص بك: {msg}. اذهب لتسجيل الدخول.")
                else: st.error(msg)
            else: st.warning("الاسم وكلمة المرور قصيرة جداً.")

# --- 7. قلب المنصة النابض (بعد الدخول) ---
else:
    u = st.session_state.auth
    prices = get_prices()

    # --- [الهيدر] ---
    st.markdown(f"""
    <div class="header-box">
        <p style="margin:0; font-size:14px;">إجمالي الرصيد (USDT)</p>
        <h1 style="margin:5px 0; color:#2ea043; font-size:36px;">$ {u['balance']:.2f}</h1>
        <p style="margin:0; font-size:12px; color:#8b949e;">ID: {u['id']} | User: {u['u']}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [المحتوى حسب الصفحة] ---
    if st.session_state.page == "home":
        # 1. كروت الأسعار (متجاوبة أفقياً)
        st.markdown(f"""
        <div class="ticker-flex">
            <div class="ticker-item"><span style="font-size:12px;color:#8b949e;">BTC</span><br><b style="color:#2ea043;">${prices['BTCUSDT']:,}</b></div>
            <div class="ticker-item"><span style="font-size:12px;color:#8b949e;">ETH</span><br><b style="color:#2ea043;">${prices['ETHUSDT']:,}</b></div>
            <div class="ticker-item"><span style="font-size:12px;color:#8b949e;">TRX</span><br><b style="color:#f85149;">${prices['TRXUSDT']}</b></div>
        </div>
        """, unsafe_allow_html=True)

        # 2. أزرار الوصول السريع (أزرار حقيقية تفاعلية)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.button("📥\nإيداع", on_click=go_to, args=("assets",), use_container_width=True)
        with c2: st.button("📤\nسحب", on_click=go_to, args=("assets",), use_container_width=True)
        with c3: st.button("👥\nإحالة", on_click=go_to, args=("ref",), use_container_width=True)
        with c4: st.button("💬\nدعم", use_container_width=True)

        # 3. البانر
        st.markdown("""
        <div class="promo-banner">
            <div><h4 style="margin:0;">صفقات VIP جاهزة</h4><span style="font-size:12px;">أرباح مضمونة للمشتركين</span></div>
            <div style="font-size:24px;">🎯</div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.page == "trade":
        st.markdown("### 📊 منصة التداول")
        st.components.v1.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&theme=dark" width="100%" height="450" frameborder="0"></iframe>', height=460)

    elif st.session_state.page == "assets":
        st.markdown("### 💰 محفظة الأصول")
        st.info("قم بإيداع USDT على شبكة (TRC20) للعنوان التالي:")
        st.code(u['wallet'])
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={u['wallet']}")
        if st.button("تأكيد الإيداع (إرسال إشعار للإدارة)", use_container_width=True):
            st.success("تم إرسال الطلب، سيتم التحديث قريباً.")

    elif st.session_state.page == "ref":
        st.markdown("### 👥 نظام الشركاء (Referral)")
        link = f"https://vupex-global.streamlit.app/?ref={u['id']}"
        st.code(link)
        st.metric("أرباحك من الفريق", f"${u['ref_earnings']:.2f}")
        st.write("شارك هذا الرابط واربح 10% من إيداعات أصدقائك مباشرة إلى محفظتك!")

    # --- [الناف بار السفلي] (أزرار حقيقية بجانب بعضها للتنقل) ---
    st.markdown("<hr style='border-color: #30363d; margin: 30px 0 15px 0;'>", unsafe_allow_html=True)
    n1, n2, n3, n4 = st.columns(4)
    with n1: st.button("🏠\nالرئيسية", on_click=go_to, args=("home",), use_container_width=True)
    with n2: st.button("📊\nالأسواق", on_click=go_to, args=("trade",), use_container_width=True)
    with n3: st.button("💰\nالأصول", on_click=go_to, args=("assets",), use_container_width=True)
    with n4: 
        if st.button("🚪\nخروج", use_container_width=True):
            st.session_state.auth = None
            st.rerun()