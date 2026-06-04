import streamlit as st

st.set_page_config(page_title="Калькулятор чаевых", layout="wide")

st.title("🍻 Калькулятор чаевых")

DEFAULT_WAITERS = {
    "Алена Емельянова": "female",
    "Андрей Головко": "male",
    "Арина Хорошун": "female",
    "Виталий Ульченко": "male",
    "Данила Романовский": "male",
    "Иван Гузовский": "male",
    "Игорь Смирнов": "male",
    "Максим Слетов": "male",
    "Наташа Воронова": "female",
    "Никита Поцелуев": "male",
    "Никита Свешников": "male",
    "Полина Мурченко": "female",
    "Рафаэль Шафиков": "male",
    "Таня Потапова": "female",
}

if "waiters" not in st.session_state:
    st.session_state.waiters = DEFAULT_WAITERS.copy()

if "rows" not in st.session_state:
    st.session_state.rows = 1

top_left, top_right = st.columns([3, 1])

with top_right:
    with st.expander("⚙️ Сотрудники"):
        new_name = st.text_input("Новый сотрудник")
        new_gender = st.selectbox("Пол", ["male", "female"], format_func=lambda x: "Мужчина" if x == "male" else "Женщина")

        if st.button("Добавить"):
            if new_name.strip():
                st.session_state.waiters[new_name.strip()] = new_gender
                st.success("Сотрудник добавлен")

        delete_name = st.selectbox(
            "Удалить сотрудника",
            [""] + sorted(st.session_state.waiters.keys())
        )

        if st.button("Удалить"):
            if delete_name:
                del st.session_state.waiters[delete_name]
                st.success("Сотрудник удален")

day = st.selectbox(
    "День недели",
    ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
)

cash = st.number_input("Наличка", min_value=0, value=0, step=100)

st.subheader("Сотрудники в смене")

if st.button("➕ Добавить строку"):
    st.session_state.rows += 1

employees = []
waiter_names = sorted(st.session_state.waiters.keys())

for i in range(st.session_state.rows):
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        name = st.selectbox(
            "Имя",
            [""] + waiter_names,
            key=f"name_{i}"
        )

    with col2:
        card = st.number_input(
            "Карта",
            min_value=0,
            value=0,
            step=10,
            key=f"card_{i}"
        )

    with col3:
        arrival = st.number_input(
            "Пришел при чае",
            min_value=0,
            value=0,
            step=100,
            key=f"arrival_{i}"
        )

    if name:
        employees.append({
            "name": name,
            "gender": st.session_state.waiters[name],
            "card": card,
            "arrival": arrival,
            "earned": 0
        })


def earned_word(gender):
    return "заработала" if gender == "female" else "заработал"


def debt_word(gender):
    return "должна" if gender == "female" else "должен"


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
                f"{e['name']} — {earned_word(e['gender'])} {e['earned']}, скинуть {result}"
            )
        else:
            st.write(
                f"{e['name']} — {earned_word(e['gender'])} {e['earned']}, {debt_word(e['gender'])} {abs(result)}"
            )