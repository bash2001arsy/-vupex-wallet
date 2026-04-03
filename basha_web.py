import streamlit as st
import json, os, uuid, requests, hashlib

# ------------------ إعداد الصفحة ------------------
st.set_page_config(page_title="VUPEX GLOBAL", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

DB_FILE = "users_db.json"

# ------------------ الأمان ------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

# ------------------ قاعدة البيانات ------------------
def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def register_user(username, password, ref_code):
    db = load_users()
    if username in db:
        return False, "الاسم مستخدم مسبقاً"

    uid = str(uuid.uuid4())[:8].upper()
    wallet = "T" + uuid.uuid4().hex.upper()[:33]

    db[username] = {
        "password": hash_password(password),
        "id": uid,
        "balance": 0.0,
        "wallet": wallet,
        "referred_by": ref_code,
        "ref_earnings": 0.0
    }
    save_db(db)
    return True, uid

# ------------------ جلب الأسعار ------------------
@st.cache_data(ttl=60)
def get_prices():
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=3).json()
        return {i['symbol']: float(i['price']) for i in res if i['symbol'] in ['BTCUSDT','ETHUSDT','TRXUSDT']}
    except:
        return {"BTCUSDT":67000,"ETHUSDT":3400,"TRXUSDT":0.12}

# ------------------ ستايل احترافي ------------------
st.markdown("""
<style>
.block-container { max-width:600px; margin:auto; padding-top:10px; padding-bottom:80px;}
[data-testid="stSidebar"], [data-testid="stHeader"] {display:none;}
.stApp {background:#0d1117;}
.header-box {
 background:linear-gradient(135deg,#001529,#003366);
 padding:30px;border-radius:20px;text-align:center;margin-bottom:20px;
 border:1px solid #1c232d;
}
.ticker-flex {display:flex;gap:10px;margin-bottom:20px;}
.ticker-item {background:#161b22;border:1px solid #30363d;border-radius:12px;padding:10px;flex:1;text-align:center;}
div.stButton > button {
 background:#161b22;color:#c9d1d9;border:1px solid #30363d;
 border-radius:15px;height:70px;font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Session ------------------
if "auth" not in st.session_state:
    st.session_state.auth = None
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page

# ------------------ صفحة تسجيل الدخول ------------------
if st.session_state.auth is None:
    st.markdown("<div class='header-box'><h1 style='color:#58a6ff;'>VUPEX GLOBAL</h1></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["تسجيل الدخول","إنشاء حساب"])

    with tab1:
        lu = st.text_input("اسم المستخدم")
        lp = st.text_input("كلمة المرور", type="password")

        if st.button("دخول"):
            db = load_users()
            if lu in db and verify_password(lp, db[lu]["password"]):
                st.session_state.auth = lu
                st.rerun()
            else:
                st.error("بيانات خاطئة")

    with tab2:
        ru = st.text_input("اسم مستخدم جديد")
        rp = st.text_input("كلمة مرور", type="password")
        ref = st.query_params.get("ref","")

        if st.button("تسجيل"):
            ok,msg = register_user(ru,rp,ref)
            if ok: st.success("تم إنشاء الحساب")
            else: st.error(msg)

# ------------------ داخل الحساب ------------------
else:
    db = load_users()
    u = db[st.session_state.auth]
    prices = get_prices()

    st.markdown(f"""
    <div class="header-box">
        <h1 style="color:#2ea043;">$ {u['balance']:.2f}</h1>
        <p>ID: {u['id']} | {st.session_state.auth}</p>
    </div>
    """, unsafe_allow_html=True)

    # -------- الصفحة الرئيسية --------
    if st.session_state.page=="home":
        st.markdown(f"""
        <div class="ticker-flex">
        <div class="ticker-item">BTC<br>${prices['BTCUSDT']:,}</div>
        <div class="ticker-item">ETH<br>${prices['ETHUSDT']:,}</div>
        <div class="ticker-item">TRX<br>${prices['TRXUSDT']}</div>
        </div>
        """, unsafe_allow_html=True)

        c1,c2,c3,c4 = st.columns(4)
        with c1: st.button("إيداع", on_click=go,args=("assets",), use_container_width=True)
        with c2: st.button("تداول", on_click=go,args=("trade",), use_container_width=True)
        with c3: st.button("إحالة", on_click=go,args=("ref",), use_container_width=True)
        with c4:
            if st.button("خروج", use_container_width=True):
                st.session_state.auth=None
                st.rerun()

    # -------- التداول --------
    if st.session_state.page=="trade":
        st.components.v1.html(
            '<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&theme=dark" width="100%" height="450"></iframe>',
            height=460)

    # -------- الأصول --------
    if st.session_state.page=="assets":
        st.info("ايداع USDT TRC20 على العنوان:")
        st.code(u['wallet'])
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={u['wallet']}")

    # -------- الإحالة --------
    if st.session_state.page=="ref":
        link=f"https://vupex-global.streamlit.app/?ref={u['id']}"
        st.code(link)
        st.metric("ارباحك", f"${u['ref_earnings']:.2f}")

    # -------- ناف بار سفلي --------
    st.markdown("---")
    n1,n2,n3 = st.columns(3)
    with n1: st.button("الرئيسية", on_click=go,args=("home",),use_container_width=True)
    with n2: st.button("الأسواق", on_click=go,args=("trade",),use_container_width=True)
    with n3: st.button("الأصول", on_click=go,args=("assets",),use_container_width=True)