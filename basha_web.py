import streamlit as st
import requests

# 1. إعدادات الموقع (تظهر في تبويب المتصفح)
st.set_page_config(page_title="Vupex Global", page_icon="📈", layout="centered")

# 2. وظيفة جلب الأسعار من Binance
def get_crypto_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data = requests.get(url).json()
        return f"{float(data['price']):,.2f} $"
    except:
        return "Offline"

# 3. إدارة الجلسة (Session State) ليبقى المستخدم مسجلاً دخوله
if 'page' not in st.session_state:
    st.session_state.page = "login"

# --- [ صفحة تسجيل الدخول ] ---
if st.session_state.page == "login":
    st.title("🔐 Vupex Secure Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    
    if st.button("Access Account", use_container_width=True):
        if user == "basha" and pwd == "1234":
            st.session_state.page = "admin" # الادمن يروح لصفحته
            st.rerun()
        elif user == "user" and pwd == "0000":
            st.session_state.page = "home" # المستخدم العادي يروح للرئيسية
            st.rerun()
        else:
            st.error("بيانات الدخول خاطئة!")

# --- [ صفحة المستخدم الرئيسية ] ---
elif st.session_state.page == "home":
    st.title("👋 Welcome back!")
    st.metric("Your Balance", "41.57 $", delta="+5.2%")
    
    st.subheader("Live Market")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"BTC/USDT\n\n**{get_crypto_price('BTC')}**")
    with col2:
        st.info(f"ETH/USDT\n\n**{get_crypto_price('ETH')}**")
    
    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()

# --- [ صفحة الادمن - غرفة التحكم ] ---
elif st.session_state.page == "admin":
    st.title("😎 Admin Dashboard")
    st.warning("You are in Control Mode")
    
    st.write("### Quick Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", "152")
    col2.metric("Total Deposits", "5,400 $")
    col3.metric("System Status", "Active")
    
    st.divider()
    st.write("### Control Actions")
    if st.button("Freeze All Withdrawals"):
        st.error("All withdrawals are now FROZEN")
    
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()
