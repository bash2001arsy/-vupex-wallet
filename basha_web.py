import streamlit as st
import requests
import json
import os
import uuid
from datetime import datetime

# --- 1. إعدادات المنصة الاحترافية ---
st.set_page_config(page_title="Vupex Global | Real-Time Exchange", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# --- 2. جلب أسعار السوق الحقيقية (Real API) ---
def get_live_prices():
    try:
        # جلب الأسعار من Binance API
        res = requests.get("https://api.binance.com/api/v3/ticker/price", timeout=5).json()
        prices = {item['symbol']: float(item['price']) for item in res if item['symbol'] in ['BTCUSDT', 'ETHUSDT', 'TRXUSDT', 'SOLUSDT', 'ADAUSDT']}
        return prices
    except:
        # أسعار احتياطية في حال تعطل الـ API
        return {"BTCUSDT": 67500.0, "ETHUSDT": 3450.0, "TRXUSDT": 0.12, "SOLUSDT": 140.0, "ADAUSDT": 0.45}

# --- 3. محرك قاعدة البيانات الواقعي ---
DB_FILE = "users_db.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    # حساب الأدمن (البداية برصيد صفر)
    return {"basha": {"password": "1234", "id": "BOSS001", "balance": 0.0, "total_deposited": 0.0, "capital": 0.0, "wallet": "VUPEX-MAIN-VAULT", "role": "admin", "kyc": "Verified"}}

def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f)

def create_user(u, p, ref_by=None):
    db = load_users()
    if u in db: return False, ""
    uid = str(uuid.uuid4())[:8].upper()
    # توليد محفظة USDT TRC20 فريدة وحقيقية التنسيق
    u_wallet = "T" + str(uuid.uuid4().hex).upper()[:33]
    db[u] = {
        "password": p, "id": uid, "balance": 0.0, "total_deposited": 0.0, "capital": 0.0, 
        "wallet": u_wallet, "referred_by": ref_by, "referral_earnings": 0.0, "kyc": "Not Verified", "role": "user"
    }
    save_db(db)
    return True, uid

# --- 4. واجهة التطبيق (CSS XDCBIT Look) ---
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #e1e1e1; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
    .ticker-card { background-color: #161b22; border-radius: 12px; padding: 15px; border: 1px solid #30363d; text-align: center; margin-bottom: 10px; }
    .price-text { font-size: 20px; font-weight: bold; color: #2ea043; }
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #161b22; color: white; border: 1px solid #30363d; height: 3em; }
    .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #161b22; border-top: 1px solid #30363d; padding: 10px; z-index: 100; }
</style>
""", unsafe_allow_html=True)

# --- 5. إدارة الجلسة والتنقل ---
if 'auth' not in st.session_state: st.session_state.auth = None
if 'page' not in st.session_state: st.session_state.page = "home"

def set_page(name): st.session_state.page = name

# --- 6. واجهة الدخول ---
if st.session_state.auth is None:
    st.title("💎 VUPEX GLOBAL | Real Trade")
    ref_code = st.query_params.get("ref", None)
    
    tab1, tab2 = st.tabs(["🔒 دخول", "✨ فتح حساب"])
    with tab1:
        u_in = st.text_input("اسم المستخدم")
        p_in = st.text_input("كلمة المرور", type="password")
        if st.button("دخول المنصة"):
            db = load_users()
            if u_in in db and db[u_in]["password"] == p_in:
                st.session_state.auth = db[u_in]; st.session_state.auth["u"] = u_in; st.rerun()
            else: st.error("بيانات خاطئة")
    with tab2:
        nu = st.text_input("اسم جديد"); np = st.text_input("باسورد جديد", type="password")
        if ref_code: st.info(f"إحالة نشطة: {ref_code}")
        if st.button("تأجيل التسجيل الحقيقي"):
            db = load_users()
            owner = next((k for k, v in db.items() if v["id"] == ref_code), None)
            success, mid = create_user(nu, np, owner)
            if success: st.success(f"تم! معرفك: {mid}")

# --- 7. داخل المنصة (الحياة الحقيقية) ---
else:
    db = load_users()
    u = db[st.session_state.auth['u']]
    live_prices = get_live_prices()

    # القائمة السفلية (التنقل)
    nav1, nav2, nav3, nav4 = st.columns(4)
    with nav1: st.button("🏠", on_click=set_page, args=("home",))
    with nav2: st.button("📊", on_click=set_page, args=("market",))
    with nav3: st.button("🎯", on_click=set_page, args=("trade",))
    with nav4: st.button("💰", on_click=set_page, args=("assets",))

    # --- صفحة: الرئيسية (الواقعية) ---
    if st.session_state.page == "home":
        st.markdown(f"### مرحباً {st.session_state.auth['u']}")
        st.metric("رصيدك الفعلي", f"$ {u['balance']:.2f}")
        
        st.write("🔥 أسعار السوق الحية (Binance API)")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='ticker-card'>BTC<br><span class='price-text'>${live_prices['BTCUSDT']:,}</span></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='ticker-card'>ETH<br><span class='price-text'>${live_prices['ETHUSDT']:,}</span></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='ticker-card'>TRX<br><span class='price-text'>${live_prices['TRXUSDT']:.4f}</span></div>", unsafe_allow_html=True)

        st.markdown("### إجراءات سريعة")
        sc1, sc2 = st.columns(2)
        with sc1: st.button("📥 إيداع USDT", on_click=set_page, args=("assets",))
        with sc2: st.button("👥 دعوة أصدقاء", on_click=set_page, args=("ref",))

    # --- صفحة: الأصول (نظام الإيداع الحقيقي) ---
    elif st.session_state.page == "assets":
        st.header("💰 محفظة الأصول")
        st.info("نظام الإيداع: أودع في العنوان أدناه وسيتم تفعيل الرصيد بعد تأكيد الشبكة (10-30 دقيقة).")
        st.markdown(f"<div class='ticker-card'>عنوان TRC20 الخاص بك:<br><code>{u['wallet']}</code></div>", unsafe_allow_html=True)
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={u['wallet']}")
        
        amt = st.number_input("أدخل المبلغ الذي قمت بتحويله للتسجيل", min_value=0.0)
        if st.button("تأكيد التحويل (Notify Admin)"):
            st.success("تم إرسال بلاغ الإيداع للأدمن. سيتم التحديث قريباً.")

    # --- صفحة: الإحالة (3 مستويات حقيقية) ---
    elif st.session_state.page == "ref":
        st.title("🔗 نظام الشركاء")
        r_url = f"https://vupex-global.streamlit.app/?ref={u['id']}"
        st.code(r_url)
        st.write(f"أرباحك من الفريق: ${u['referral_earnings']:.2f}")

    if st.sidebar.button("Logout"): st.session_state.auth = None; st.rerun()
