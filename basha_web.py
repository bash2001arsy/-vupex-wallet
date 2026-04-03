# --- 1. تحديث منطق التنقل في بداية الكود ---
if 'page' not in st.session_state:
    st.session_state.page = "home"

# --- 2. دالة لتغيير الصفحة برمجياً ---
def ch_pg(name):
    st.session_state.page = name

# --- 3. استبدال قسم الـ Action Container (أزرار الإيداع والسحب) ---
st.markdown("<div class='section-title'>الوصول السريع</div>", unsafe_allow_html=True)
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    if st.button("📥\nإيداع", key="btn_dep", on_click=ch_pg, args=("dep",)): pass
with col_b:
    if st.button("📤\nسحب", key="btn_with", on_click=ch_pg, args=("with",)): pass
with col_c:
    if st.button("🔄\nصرف", key="btn_exch", on_click=ch_pg, args=("home",)): pass
with col_d:
    if st.button("💬\nدعم", key="btn_supp", on_click=ch_pg, args=("home",)): pass

# --- 4. استبدال القائمة السفلية (Bottom Nav) بأزرار حقيقية ---
st.markdown("<br><br>", unsafe_allow_html=True) # مساحة للحماية
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    st.button("🏠 الرئيسية", on_click=ch_pg, args=("home",), use_container_width=True)
with nav_col2:
    st.button("📊 الأسواق", on_click=ch_pg, args=("markets",), use_container_width=True)
with nav_col3:
    st.button("🎯 الصفقات", on_click=ch_pg, args=("trade",), use_container_width=True)
with nav_col4:
    st.button("💰 الأصول", on_click=ch_pg, args=("assets",), use_container_width=True)

# --- 5. عرض المحتوى بناءً على الصفحة المختارة ---
if st.session_state.page == "home":
    # هنا تضع كود الصفحة الرئيسية (البانر والقائمة)
    st.write("أهلاً بك في الرئيسية")
elif st.session_state.page == "dep":
    st.header("إيداع العملات")
    st.code(user['wallet'])
elif st.session_state.page == "trade":
    st.header("منصة التداول")
    # شارت التداول