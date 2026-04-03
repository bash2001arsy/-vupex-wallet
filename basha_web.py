import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime

# --- 1. إعدادات المنصة الأساسية ---
st.set_page_config(page_title="Vupex Exchange | Alpha", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. محرك قاعدة البيانات للنظام الجديد ---
DB_FILE = "users_db.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"basha": {"password": "1234", "id": "BOSS001", "balance": 100000.0, "total_deposited": 10000.0, "wallet": "T-MASTER", "role": "admin"}}

# --- 3. قنبلة الـ CSS: تحويل الويب إلى تطبيق موبايل (Native Look) ---
# هذا الجزء هو المسؤول عن محاكاة شكل الصورة (XDCBIT)
st.markdown("""
<style>
    /* 1. تصفير الهيكل الافتراضي وجعله مظلماً */
    .main { background-color: #101419; color: #e1e1e1; font-family: 'Segoe UI', sans-serif; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    [data-testid="stSidebar"] { display: none; } /* إلغاء القائمة الجانبية */
    
    /* 2. تنسيق الهيدر العلوي (الأزرق الفضائي) */
    .app-header {
        background: linear-gradient(180deg, #101419 0%, #1c232d 100%);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        text-align: center;
        margin-bottom: 10px;
        position: relative;
    }
    .app-header h1 { color: #58a6ff; font-size: 24px; margin: 0; }
    .app-header p { color: #8b949e; font-size: 14px; margin: 5px 0 0 0; }
    .user-avatar { position: absolute; top: 15px; left: 15px; width: 35px; height: 35px; background: #30363d; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #8b949e;}
    .support-icon { position: absolute; top: 15px; right: 15px; color: #8b949e; font-size: 20px;}

    /* 3. شريط الأخبار المتحرك */
    .news-ticker {
        background-color: #1c232d;
        color: #d29922;
        padding: 8px 15px;
        font-size: 13px;
        border-radius: 10px;
        margin: 0 10px 15px 10px;
        border: 1px solid #30363d;
        display: flex; align-items: center; gap: 10px;
    }

    /* 4. بطاقات الأسعار الحية (Live Cards) */
    .ticker-container {
        display: flex;
        gap: 10px;
        padding: 0 10px;
        overflow-x: auto;
        margin-bottom: 20px;
    }
    .ticker-card {
        background-color: #1c232d;
        border-radius: 12px;
        padding: 15px;
        min-width: 140px;
        border: 1px solid #30363d;
        text-align: left;
    }
    .ticker-card .coin-pair { font-size: 13px; color: #8b949e; margin-bottom: 3px; }
    .ticker-card .price { font-size: 18px; font-weight: bold; }
    .ticker-card .change.up { color: #2ea043; font-size: 12px; }
    .ticker-card .change.down { color: #f85149; font-size: 12px; }
    .sparkline { height: 30px; margin-top: 5px; background: url('https://upload.wikimedia.org/wikipedia/commons/e/ed/Sparkline_Green.png') no-repeat center; background-size: cover; opacity: 0.5;}

    /* 5. أزرار الوصول السريع الدائرية (الأكشن) */
    .action-container {
        display: flex;
        justify-content: space-around;
        padding: 0 15px;
        margin-bottom: 25px;
    }
    .action-item { text-align: center; color: #e1e1e1; font-size: 13px; cursor: pointer; }
    .action-icon {
        width: 55px;
        height: 55px;
        background-color: #1c232d;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 8px;
        font-size: 22px;
        border: 1px solid #30363d;
        color: #d29922; /* لون الأيقونات الذهبي كما في الصورة */
    }
    .action-icon:hover { background-color: #30363d; }

    /* 6. قائمة أعلى الأرباح (Gainers List) */
    .section-title { font-size: 18px; color: #e1e1e1; padding: 0 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;}
    .view-all { font-size: 14px; color: #2ea043; font-weight: bold; }

    .gainer-row {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        margin: 0 10px 8px 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #30363d;
    }
    .coin-info { display: flex; align-items: center; gap: 10px; }
    .coin-logo { width: 35px; height: 35px; background-color: #1c232d; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #8b949e; }
    .coin-name { font-size: 16px; font-weight: bold; }
    .coin-symbol { font-size: 12px; color: #8b949e; }
    .price-info { text-align: right; }
    .current-price { font-size: 16px; font-weight: bold; }
    .gainer-badge {
        background-color: #2ea043;
        color: white;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        margin-left: 10px;
        box-shadow: 0 0 10px rgba(46, 160, 67, 0.4);
    }

    /* 7. القائمة السفلية (Bottom Navigation Bar) */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1c232d;
        border-top: 1px solid #30363d;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 1000;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.3);
    }
    .nav-item { text-align: center; color: #8b949e; font-size: 11px; cursor: pointer; text-decoration: none; }
    .nav-item.active { color: #2ea043; }
    .nav-icon { font-size: 20px; margin-bottom: 4px; }
    
    /* تصحيح للمحتوى ليظهر فوق القائمة السفلية */
    .content-wrapper { padding-bottom: 80px; }

</style>
""", unsafe_allow_html=True)

# --- 4. إدارة الجلسة والدخول ---
if 'auth' not in st.session_state: st.session_state.auth = None
if 'page' not in st.session_state: st.session_state.page = "🏠 الصفحة الرئيسية"

db = load_users()

# واجهة الدخول (محاكاة سريعة للشكل الجديد)
if st.session_state.auth is None:
    st.markdown("<div class='app-header'><h1>💎 VUPEX Exchange</h1><p>ابدأ رحلة الثراء اليوم</p></div>", unsafe_allow_html=True)
    st.markdown("<div style='padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    u_log = st.text_input("اسم المستخدم", key="log_u")
    p_log = st.text_input("كلمة المرور", type="password", key="log_p")
    if st.button("دخول آمن"):
        if u_log in db and db[u_log]["password"] == p_log:
            st.session_state.auth = db[u_log]
            st.session_state.auth["u"] = u_log
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. الصفحة الرئيسية الجديدة (XDCBIT Look) ---
else:
    user = st.session_state.auth
    
    # محتوى الصفحة الأساسي داخل wrapper
    st.markdown("<div class='content-wrapper'>", unsafe_allow_html=True)
    
    # أ: الهيدر الأزرق (XDCBIT Look)
    st.markdown(f"""
        <div class="app-header">
            <div class="user-avatar">👤</div>
            <h1>VUPEX Exchange</h1>
            <p>مرحباً، {user['u']} | رصيدك: $ {user['balance']:,}</p>
            <div class="support-icon">🎧</div>
        </div>
    """, unsafe_allow_html=True)
    
    # ب: شريط التنبيهات المتحرك (Ticker)
    st.markdown("""
        <div class="news-ticker">
            📢 <span>ترقبوا صفقة VIP القادمة بربح 5%.. شارك الرابط الآن لتربح من الإحالات!</span>
        </div>
    """, unsafe_allow_html=True)
    
    # ج: بطاقات الأسعار الحية (Ticker Container)
    st.markdown("""
        <div class="ticker-container">
            <div class="ticker-card">
                <div class="coin-pair">BTCUSDT <span class="change up">+0.05%</span></div>
                <div class="price">66,871.84</div>
                <div class="sparkline"></div>
            </div>
            <div class="ticker-card">
                <div class="coin-pair">ETHUSDT <span class="change up">+0.02%</span></div>
                <div class="price">2,052.64</div>
                <div class="sparkline"></div>
            </div>
            <div class="ticker-card">
                <div class="coin-pair">TRXUSDT <span class="change down">-0.01%</span></div>
                <div class="price">0.13146</div>
                <div class="sparkline"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # د: أزرار الوصول السريع (المحاكاة الكاملة للصورة)
    # ملاحظة: في الـ CSS ربطنا الأزرار بروابط Streamlit الداخلية (Query Params) لتغيير الصفحة
    st.markdown(f"""
        <div class="action-container">
            <a class="action-item" href="/?p=dep" target="_self">
                <div class="action-icon">📥</div>
                إيداع العملة
            </a>
            <a class="action-item" href="/?p=with" target="_self">
                <div class="action-icon">📤</div>
                سحب العملة
            </a>
            <div class="action-item">
                <div class="action-icon">🔄</div>
                صرف سريع
            </div>
            <div class="action-item">
                <div class="action-icon">💬</div>
                المزيد
            </div>
        </div>
    """, unsafe_allow_html=True)

    # هـ: إعلان بانر ترويجي (مثل الصورة)
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1c232d 0%, #238636 100%); padding: 20px; border-radius: 15px; margin: 0 10px 25px 10px; display: flex; align-items: center; justify-content: space-between; border: 1px solid #30363d;">
            <div>
                <h3 style="color: white; margin: 0;">قم بشراء العملات بسرعة</h3>
                <p style="color: #c9d1d9; margin: 5px 0 0 0; font-size: 14px;">آمن ومريح</p>
            </div>
            <div style="width: 40px; height: 40px; background-color: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;">➜</div>
        </div>
    """, unsafe_allow_html=True)

    # و: قائمة أعلى الأرباح (Gainers List)
    st.markdown('<div class="section-title"><span>🔥 أعلى الأرباح</span> <span class="view-all">أعلى الأرباح</span></div>', unsafe_allow_html=True)
    
    # بيانات تجريبية لمحاكاة الصورة
    gainers_data = [
        {"name": "Cardano", "sym": "ADA", "price": "0.2473", "change": "+3.04%"},
        {"name": "Yearn.finance", "sym": "YFI", "price": "2,484.73", "change": "+2.90%"},
        {"name": "Filecoin", "sym": "FIL", "price": "0.838", "change": "+2.57%"},
    ]
    
    for coin in gainers_data:
        st.markdown(f"""
            <div class="gainer-row">
                <div class="coin-info">
                    <div class="coin-logo">🪙</div>
                    <div>
                        <div class="coin-name">{coin['name']}</div>
                        <div class="coin-symbol">{coin['sym']} / USDT</div>
                    </div>
                </div>
                <div class="price-info">
                    <span class="current-price">{coin['price']}</span>
                    <span class="gainer-badge">{coin['change']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True) # Content Wrapper End

    # --- 6. القنبلة البرمجية: القائمة السفلية (Bottom Navigation) ---
    # نستخدم روابط مخصصة تعيد تحميل الصفحة مع بارامتر "p" لتحديد الصفحة النشطة
    st.markdown("""
        <div class="bottom-nav">
            <a class="nav-item active" href="/?p=home" target="_self">
                <div class="nav-icon">🏠</div>
                الرئيسية
            </a>
            <a class="nav-item" href="/?p=markets" target="_self">
                <div class="nav-icon">📊</div>
                الأسواق
            </a>
            <a class="nav-item" href="/?p=trade" target="_self">
                <div class="nav-icon">🎯</div>
                الصفقات
            </a>
            <a class="nav-item" href="/?p=assets" target="_self">
                <div class="nav-icon">💰</div>
                الأصول
            </a>
        </div>
    """, unsafe_allow_html=True)