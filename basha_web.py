import streamlit as st
import requests

# إعدادات الفخامة
st.set_page_config(page_title="Vupex Pro", page_icon="💰", layout="wide")

# وظيفة جلب الأسعار
def get_price(symbol):
    try:
        res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
        return float(res['price'])
    except: return 0

# تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Vupex Global Login")
    with st.container():
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Sign In"):
            if u == "basha" and p == "1234":
                st.session_state.logged_in = True
                st.rerun()
else:
    # القائمة الجانبية (Sidebar)
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Deposit", "Admin Control"])
    
    if menu == "Dashboard":
        st.title("💳 Your Wallet")
        st.metric("Total Balance", "$ 4,157.20", "+2.5%")
        
        st.subheader("Live Crypto Market")
        c1, c2, c3 = st.columns(3)
        with c1: st.success(f"BTC: ${get_price('BTC'):,.2f}")
        with c2: st.warning(f"ETH: ${get_price('ETH'):,.2f}")
        with c3: st.error(f"SOL: ${get_price('SOL'):,.2f}")
        
    elif menu == "Deposit":
        st.title("📥 Deposit Funds")
        st.write("Send USDT (TRC20) to the address below:")
        st.code("T9yD3s5wE4f6G7h8J9k0L1m2N3b4V5c6") # مثال لعنوان محفظة
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=T9yD3s5wE4f6G7h8J9k0L1m2N3b4V5c6")
        st.info("After sending, upload the screenshot for approval.")
        st.file_uploader("Upload Receipt")

    elif menu == "Admin Control":
        st.title("😎 Boss Mode")
        st.write("Manage users and requests")
        st.table({"User": ["User1", "User2"], "Status": ["Pending", "Active"], "Balance": ["$50", "$1200"]})
