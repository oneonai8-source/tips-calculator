import streamlit as st

st.set_page_config(page_title="Калькулятор чаевых", layout="wide")

st.title("🍻 Калькулятор чаевых")

# ------------------------
# Список сотрудников
# ------------------------
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

# ------------------------
# Блок добавления/удаления сотрудников
# ------------------------
top_left, top_right = st.columns([3, 1])

with top_right:
    with st.expander("⚙️ Управление сотрудниками"):
        new_name = st.text_input("Новый сотрудник")
        new_gender = st.selectbox("Пол", ["male", "female"], format_func=lambda x: "Мужчина" if x == "male" else "Женщина")

        if st.button("Добавить сотрудника"):
            if new_name.strip():
                st.session_state.waiters[new_name.strip()] = new_gender
                st.success(f"Сотрудник {new_name.strip()} добавлен")

        delete_name = st.selectbox(
            "Удалить сотрудника",
            [""] + sorted(st.session_state.waiters.keys())
        )

        if st.button("Удалить сотрудника"):
            if delete_name:
                del st.session_state.waiters[delete_name]
                st.success(f"Сотрудник {delete_name} удален")

# ------------------------
# Ввод данных смены
# ------------------------
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

# ------------------------
# Вспомогательные функции
# ------------------------
def earned_word(gender):
    return "заработала" if gender == "female" else "заработал"

def debt_word(gender):
    return "должна" if gender == "female" else "должен"

# ------------------------
# Расчет чаевых
# ------------------------
if st.button("Рассчитать"):

    if not employees:
        st.error("Добавьте сотрудников")
        st.stop()

    total_cards = sum(e["card"] for e in employees)
    total_tips = cash + total_cards

    # Мойка: отдельно для официантов и бара
    if day in ["Понедельник", "Вторник", "Среда", "Четверг"]:
        waiter_wash = len(employees) * 200
        bar_wash = 300
    else:
        waiter_wash = len(employees) * 250
        bar_wash = 350

    wash = waiter_wash + bar_wash

    # Бар: 10% от оставшегося после менеджера и мойки
manager = 1000

    bar_base = total_tips - manager - wash
    bar_percent = round(bar_base * 0.10)

    # Чистые деньги бара с учетом их части на мойку
    bar = bar_percent - bar_wash

    # Чистые чаевые для официантов
    waiter_tips = total_tips - manager - wash - bar

    # ------------------------
    # Распределение по приходу
    # ------------------------
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

    # Финальный слой на всех
    already_counted = round(previous_point * 0.90)
    final_layer = waiter_tips - already_counted
    final_part = round(final_layer / len(employees))

    for e in employees:
        e["earned"] += final_part

    # ------------------------
    # Вывод результата
    # ------------------------
    st.subheader("Результат")

    st.write(f"На мойку {wash}")
    st.write(f"Менеджер 1000")
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