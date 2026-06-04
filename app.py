import streamlit as st

st.set_page_config(page_title="Калькулятор чаевых", layout="wide")

st.title("🍻 Калькулятор чаевых")

day = st.selectbox(
    "День недели",
    ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
)

cash = st.number_input("Наличка", min_value=0, value=0, step=100)

st.subheader("Сотрудники")

employees = []

for i in range(8):
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        name = st.text_input(f"Имя {i+1}", key=f"name_{i}")

    with col2:
        card = st.number_input(f"Карта {i+1}", min_value=0, value=0, step=10, key=f"card_{i}")

    with col3:
        arrival = st.number_input(
            f"Пришел при чае {i+1}",
            min_value=0,
            value=0,
            step=100,
            key=f"arrival_{i}"
        )

    if name:
        employees.append({
            "name": name.strip(),
            "card": card,
            "arrival": arrival,
            "earned": 0
        })


def word_for_debt(name):
    return "должна" if name.endswith(("а", "я")) else "должен"


if st.button("Рассчитать"):

    if not employees:
        st.error("Добавьте сотрудников")
        st.stop()

    total_cards = sum(e["card"] for e in employees)
    total_tips = cash + total_cards

    manager = 1000

    if day in ["Понедельник", "Вторник", "Среда", "Четверг"]:
        wash = len(employees) * 200 + 300
    else:
        wash = len(employees) * 250 + 350

    bar_base = total_tips - manager - wash
    bar = round(bar_base * 0.10)

    waiter_tips = total_tips - manager - wash - bar

    # Все точки прихода, кроме 0
    arrival_points = sorted(set(e["arrival"] for e in employees if e["arrival"] > 0))

    previous_point = 0

    for point in arrival_points:
        active = [e for e in employees if e["arrival"] <= previous_point]

        if active:
            layer_amount = round((point - previous_point) * 0.90)
            part = round(layer_amount / len(active))

            for e in active:
                e["earned"] += part

        previous_point = point

    # Последний слой делится на всех
    already_counted = round(previous_point * 0.90)
    final_layer = waiter_tips - already_counted
    final_part = round(final_layer / len(employees))

    for e in employees:
        e["earned"] += final_part

    st.subheader("Результат")

    st.write(f"На мойку {wash}")
    st.write(f"Менеджер {manager}")
    st.write(f"На бар {bar}")

    st.divider()

    for e in employees:
        result = e["earned"] - e["card"]

        if result >= 0:
            st.write(
                f"{e['name']} — заработал {e['earned']}, скинуть {result}"
            )
        else:
            debt_word = word_for_debt(e["name"])
            st.write(
                f"{e['name']} — заработал {e['earned']}, {debt_word} {abs(result)}"
            )