import streamlit as st

st.title("Калькулятор чаевых")

col1, col2 = st.columns(2)

with col1:
    bill_amount = st.number_input("Сумма счета (₽)", value=100.0, min_value=0.0, step=10.0)

with col2:
    tip_percent = st.slider("Процент чаевых (%)", min_value=0, max_value=50, value=15, step=1)

col3, col4 = st.columns(2)

with col3:
    num_people = st.number_input("Количество человек", value=1, min_value=1, step=1)

with col4:
    st.empty()

if st.button("Рассчитать", use_container_width=True):
    tip_amount = bill_amount * (tip_percent / 100)
    total_amount = bill_amount + tip_amount
    per_person = total_amount / num_people
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Сумма счета", f"₽{bill_amount:.2f}")
    with col2:
        st.metric("Чаевые", f"₽{tip_amount:.2f}")
    with col3:
        st.metric("Всего", f"₽{total_amount:.2f}")
    
    st.divider()
    
    st.metric("На человека", f"₽{per_person:.2f}", delta=f"{tip_percent}%")
