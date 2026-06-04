import streamlit as st

st.set_page_config(page_title="Калькулятор чаевых", layout="wide")

st.title("🍻 Калькулятор чаевых")

day = st.selectbox(
    "День недели",
    [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]
)

cash = st.number_input(
    "Наличка",
    min_value=0,
    value=0,
    step=100
)

st.subheader("Сотрудники")

employees = []

for i in range(8):
    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        name = st.text_input(
            f"Имя {i+1}",
            key=f"name_{i}"
        )

    with col2:
        card = st.number_input(
            f"Карта {i+1}",
            min_value=0,
            value=0,
            key=f"card_{i}"
        )

    with col3:
        arrival = st.number_input(
            f"Пришел при чае {i+1}",
            min_value=0,
            value=0,
            key=f"arrival_{i}"
        )

    if name:
        employees.append({
            "name": name,
            "card": card,
            "arrival": arrival
        })

if st.button("Рассчитать"):

    if len(employees) == 0:
        st.error("Добавьте сотрудников")
        st.stop()

    total_cards = sum(x["card"] for x in employees)
    total_tips = cash + total_cards

    manager = 1000

    if day in [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг"
    ]:
        wash = len(employees) * 200 + 300
    else:
        wash = len(employees) * 250 + 350

    bar = round((total_tips - manager - wash) * 0.10)

    st.subheader("Результат")

    st.write(f"На мойку {wash}")
    st.write(f"Менеджер {manager}")
    st.write(f"На бар {bar}")

    st.divider()

    st.write(
        f"Общий чай: {total_tips}"
    )