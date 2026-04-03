import streamlit as st
import pandas as pd
import requests
import json
import os
import uuid
from datetime import datetime, timedelta

# --- 1. إعدادات المنصة الاحترافية ---
st.set_page_config(page_title="Vupex Global | Professional Terminal", page_icon="💎", layout="wide")

# --- 2. ستايل "الهيبة" (Modern Dark UI) ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(90deg, #238636 0%, #2ea043 100%); color: white; font-weight: bold; border: none; height: 3em; }
    .section-box { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
    code { color: #58a6ff; font-size: 1.1em; }
    .status-verified { color: #238636; font-weight: bold; }
    .status-pending { color: #d29922; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك قاعدة البيانات ---
DB_FILE = "users_db.json"

if 'active_signals' not in st.session_state: st.session_state.active_signals = {}
if 'system_announcement' not in st.session_state: st.session_state.system_announcement = "📢 نظام الإحالات نشط! ابنِ فريقك الآن واربح من 3 مستويات."

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"basha": {"password": "1234", "id": "BOSS-001", "balance": 100000.0, "total_deposited": 10000.0, "capital": 10000.0, "wallet": "T-MASTER-WALLET", "referred_by": None, "referral_earnings": 0.0, "kyc": "Verified", "role": "admin"}}

def save_user(u, p, ref_by=None):
    db = load_users()
    if u in db: return False, ""
    uid = str(uuid.uuid4())[:8].upper()
    unique_wallet = "T" + "".join(str(uuid.uuid4()).split("-")).upper()[:33]
    db[u] = {
        "password": p, "id": uid, "balance": 0.0, "total_deposited": 0.0, "capital": 0.0, 
        "wallet": unique_wallet, "referred_by": ref_by, "referral_earnings": 0.0, "kyc": "Not Verified", "role": "user"
    }
    with open(DB_FILE, "w") as f: json.dump(db, f)
    return True, uid

# --- 4. إدارة الجلسة والدخول ---
if 'auth' not in st.session_state: st.session_state.auth = None

if st.session_state.auth is None:
    st.markdown("<h1 style='text-align: center; color: #58a6ff;'>💎 VUPEX GLOBAL</h1>", unsafe_allow_html=True)
    ref_code = st.query_params.get("ref", None)
    
    col_log, _ = st.columns([1, 1])
    with col_log:
        t1, t2 = st.tabs(["🔒 دخول", "✨ إنشاء حساب"])
        with t1:
            ul = st.text_input("اسم المستخدم")
            pl = st.text_input("كلمة المرور", type="password")
            if st.button("دخول المنصة"):
                db = load_users()
                if ul in db and db[ul]["password"] == pl:
                    st.session_state.auth = {"u": ul}; st.rerun()
        with t2:
            nu = st.text_input("اسم المستخدم الجديد"); np = st.text_input("كلمة المرور الجديدة", type="password")
            if ref_code: st.info(f"كود الإحالة النشط: {ref_code}")
            if st.button("إنشاء حسابي"):
                db = load_users()
                owner = next((k for k, v in db.items() if v["id"] == ref_code), None)
                s, mid = save_user(nu, np, ref_by=owner)
                if s: st.success(f"تم التسجيل! معرفك: {mid}")

# --- 5. المنصة الرئيسية (داخل الحساب) ---
else:
    db = load_users()
    u_name = st.session_state.auth['u']
    u = db[u_name]
    is_vip = u["total_deposited"] >= 300.0
    
    st.sidebar.markdown(f"### 👋 مرحباً، {u_name}")
    st.sidebar.markdown(f"الحالة: <span class='status-verified' if u['kyc']=='Verified' else 'status-pending'>{u['kyc']}</span>", unsafe_allow_html=True)
    if is_vip: st.sidebar.warning("🌟 VIP MEMBER")
    
    menu = ["🏠 الرئيسية", "📊 التداول الحي", "💰 المحفظة", "👥 الشركاء (Referral)", "🛡️ التوثيق (KYC)"]
    if u['role'] == "admin": menu.append("⚙️ الإدارة")
    choice = st.sidebar.radio("القائمة", menu)

    # --- القسم 1: الرئيسية ---
    if "الرئيسية" in choice:
        st.header("🏠 نظرة عامة")
        st.info(st.session_state.system_announcement)
        c1, c2, c3 = st.columns(3)
        c1.metric("الرصيد", f"$ {u['balance']:,}")
        c2.metric("أصل الإيداع", f"$ {u['capital']:,}")
        c3.metric("أرباح الإحالة", f"$ {u['referral_earnings']:,}")

    # --- القسم 2: التداول الحي (شارت TradingView) ---
    elif "التداول الحي" in choice:
        st.header("📊 منصة التداول العالمية")
        st.components.v1.html("""
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=H&theme=dark" width="100%" height="500" frameborder="0"></iframe>
        """, height=500)
        
        st.markdown("<div class='section-box'><h4>🎯 تنفيذ الصفقات الذكي</h4>أدخل كود الإشارة المباشر للبدء</div>", unsafe_allow_html=True)
        code_in = st.text_input("Signal Code").upper()
        if st.button("تنفيذ الآن"):
            if code_in in st.session_state.active_signals:
                sig = st.session_state.active_signals[code_in]
                if sig["type"] == "VIP" and not is_vip: st.error("⚠️ هذا الكود مخصص لأعضاء VIP فقط (إيداع 300+)")
                else: st.balloons(); st.success(f"تم التنفيذ بنجاح! ربح الصفقة: {sig['profit']}%")
            else: st.error("الكود غير صحيح")

    # --- القسم 3: المحفظة (إيداع وسحب + حماية رأس المال) ---
    elif "المحفظة" in choice:
        st.header("💰 إدارة المحفظة")
        t_dep, t_with = st.tabs(["📥 إيداع USDT", "📤 سحب الأرباح"])
        with t_in:
            st.markdown(f"<div class='section-box'><h4>عنوان إيداعك الفريد (TRC20)</h4><code>{u['wallet']}</code></div>", unsafe_allow_html=True)
            st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={u['wallet']}")
        with t_with:
            st.warning("⚠️ عمولة السحب 5% | لا يمكن سحب رأس المال إلا عند مضاعفته.")
            amt_out = st.number_input("المبلغ المطلوب", min_value=20.0)
            profit = u['balance'] - u['capital'] if u['balance'] > u['capital'] else 0
            if st.button("طلب سحب"):
                if u['balance'] >= (u['capital'] * 2) or amt_out <= profit:
                    st.success(f"تم إرسال الطلب. المبلغ الصافي: ${amt_out*0.95}")
                else: st.error("⚠️ عذراً، لا يمكنك سحب أصل الإيداع حالياً. يمكنك سحب الأرباح فقط.")

    # --- القسم 4: الشركاء (3 مستويات) ---
    elif "الشركاء" in choice:
        st.header("👥 شبكة شركاء Vupex")
        ref_url = f"https://vupex-global.app/?ref={u['id']}"
        st.code(ref_url, language="text")
        
        # منطق الشجرة
        l1 = [k for k, v in db.items() if v.get("referred_by") == u_name]
        l2 = [k for k, v in db.items() if v.get("referred_by") in l1]
        l3 = [k for k, v in db.items() if v.get("referred_by") in l2]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("المستوى 1 (10%)", f"{len(l1)}")
        c2.metric("المستوى 2 (3%)", f"{len(l2)}")
        c3.metric("المستوى 3 (1%)", f"{len(l3)}")
        
        st.subheader("📋 تتبع فريقك")
        for friend in l1:
            status = "✅ مودع" if db[friend]['total_deposited'] > 0 else "❌ لم يودع"
            st.write(f"👤 {friend} - {status} (${db[friend]['total_deposited']})")

    # --- القسم 5: التوثيق (KYC) ---
    elif "التوثيق" in choice:
        st.header("🛡️ الأمان والتوثيق")
        if u['kyc'] == "Verified": st.success("✅ حسابك موثق بالكامل.")
        elif u['kyc'] == "Pending": st.warning("⏳ الوثائق قيد المراجعة.")
        else:
            st.file_uploader("ارفع صورة الهوية")
            if st.button("إرسال للتوثيق"):
                db[u_name]["kyc"] = "Pending"; save_user("",""); st.rerun()

    # --- القسم 6: الإدارة (Admin) ---
    elif "الإدارة" in choice:
        st.title("⚙️ لوحة التحكم - المدير")
        pin = st.text_input("Master PIN", type="password")
        if pin == "9988":
            msg = st.text_area("تحديث إعلان النظام", st.session_state.system_announcement)
            if st.button("نشر"): st.session_state.system_announcement = msg; st.rerun()
            
            st.subheader("توليد كود صفقة")
            s_type = st.radio("النوع", ["Standard (3%)", "VIP (5%)"])
            if st.button("توليد الكود"):
                nc = str(uuid.uuid4())[:6].upper()
                st.session_state.active_signals[nc] = {"type": "VIP" if "VIP" in s_type else "STD", "profit": 5 if "VIP" in s_type else 3}
                st.success(f"كود جديد: {nc}")

    if st.sidebar.button("Logout"): st.session_state.auth = None; st.rerun()
