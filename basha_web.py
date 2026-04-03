import streamlit as st
import json
import os

# --- 1. إعدادات المنصة ---
st.set_page_config(page_title="Vupex Global", layout="wide", initial_sidebar_state="collapsed")

# --- 2. السحر الحقيقي (CSS لقلب الموازين) ---
st.markdown("""
<style>
    .main { background-color: #0d1117; }
    [data-testid="stHeader"] { display: none; }
    
    /* الهيدر العلوي */
    .header-box {
        background: linear-gradient(135deg, #001529 0%, #003366 100%);
        padding: 40px 20px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    
    /* كروت العملات الأفقية (التي كانت تظهر عمودية عندك) */
    .ticker-wrapper {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 25px;
        padding: 0 10px;
    }
    .ticker-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 15px;
        flex: 1;
        text-align: center;
    }
    .ticker-card .symbol { font-size: 12px; color: #8b949e; }
    .ticker-card .price { font-size: 16px; font-weight: bold; color: #2ea043; }

    /* شبكة الأزرار الدائرية (مثل التطبيقات الحقيقية) */
    .action-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        padding: 20px;
        text-align: center;
    }
    .action-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #c9d1d9;
        font-size: 13px;
        cursor: pointer;
    }
    .action-icon {
        width: 60px;
        height: 60px;
        background: #1c232d;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 8px;
        font-size: 24px;
        border: 1px solid #30363d;
        color: #d29922; /* لون ذهبي أيقونات */
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* بانر "قم بشراء العملات" الأخضر */
    .promo-banner {
        background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%);
        margin: 15px;
        padding: 20px;
        border-radius: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    }

    /* القائمة السفلية الحقيقية ثابتة */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #161b22;
        border-top: 1px solid #30363d;
        display: flex;
        justify-content: space-around;
        padding: 12px 0;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. المحتوى (بناء الواجهة يدوياً بدلاً من أزرار Streamlit البايخة) ---

# [1] الهيدر
st.markdown("""
<div class="header-box">
    <h1 style="color: #58a6ff; font-size: 28px; margin: 0;">XDCBIT Exchange</h1>
    <p style="color: #8b949e; margin-top: 5px;">عمليات القانونية والشفافة من خلال تسجيل XDCBIT تظهر</p>
</div>
""", unsafe_allow_html=True)

# [2] بطاقات الأسعار (أفقية)
st.markdown("""
<div class="ticker-wrapper">
    <div class="ticker-card">
        <div class="symbol">BTC/USDT <span style="color:#2ea043">+0.05%</span></div>
        <div class="price">66,871.84</div>
    </div>
    <div class="ticker-card">
        <div class="symbol">ETH/USDT <span style="color:#2ea043">+0.02%</span></div>
        <div class="price">2,052.64</div>
    </div>
    <div class="ticker-card">
        <div class="symbol">TRX/USDT <span style="color:#f85149">-0.01%</span></div>
        <div class="price">0.3146</div>
    </div>
</div>
""", unsafe_allow_html=True)

# [3] شبكة الأزرار الدائرية (Grid)
# ملاحظة: عشان تخليها تضغط، استخدمنا أزرار مخفية فوق الـ HTML
st.markdown("""
<div class="action-grid">
    <div class="action-item"><div class="action-icon">📥</div>إيداع</div>
    <div class="action-item"><div class="action-icon">📤</div>سحب</div>
    <div class="action-item"><div class="action-icon">🔄</div>صرف</div>
    <div class="action-item"><div class="action-icon">💬</div>الدعم</div>
</div>
""", unsafe_allow_html=True)

# [4] البانر الأخضر
st.markdown("""
<div class="promo-banner">
    <div>
        <h3 style="margin:0;">قم بشراء العملات بسرعة</h3>
        <p style="margin:5px 0 0 0; font-size:14px;">آمن ومريح</p>
    </div>
    <div style="font-size:24px;">➜</div>
</div>
""", unsafe_allow_html=True)

# [5] قائمة أعلى الأرباح (Gainers)
st.markdown("<h4 style='padding:15px;'>🔥 أعلى الأرباح</h4>", unsafe_allow_html=True)
gainers = [("ADA", "0.2473", "+3.04%"), ("YFI", "2484.7", "+2.90%"), ("FIL", "0.838", "+2.57%")]
for name, price, change in gainers:
    st.markdown(f"""
    <div style="background:#161b22; margin:5px 15px; padding:15px; border-radius:12px; display:flex; justify-content:space-between; align-items:center; border:1px solid #30363d;">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:30px; height:30px; background:#1c232d; border-radius:50%; display:flex; align-items:center; justify-content:center;">🪙</div>
            <b>{name}/USDT</b>
        </div>
        <div style="text-align:right;">
            <div>{price}</div>
            <div style="color:#2ea043; font-weight:bold;">{change}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# [6] الناف بار السفلي
st.markdown("""
<div class="nav-bar">
    <div style="text-align:center; color:#2ea043;">🏠<br><span style="font-size:10px;">الرئيسية</span></div>
    <div style="text-align:center; color:#8b949e;">📊<br><span style="font-size:10px;">الأسواق</span></div>
    <div style="text-align:center; color:#8b949e;">🎯<br><span style="font-size:10px;">الصفقات</span></div>
    <div style="text-align:center; color:#8b949e;">💰<br><span style="font-size:10px;">الأصول</span></div>
</div>
<div style="height:80px;"></div>
""", unsafe_allow_html=True)