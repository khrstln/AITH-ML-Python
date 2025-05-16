import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
COOKIES_EXPIRE_DAYS = os.getenv("COOKIES_EXPIRE_DAYS", 14)
TOKEN_COOKIE_NAME = os.getenv("TOKEN_COOKIE_NAME")

st.set_page_config(layout="wide")
controller = CookieController()

if "username" not in st.session_state:
    st.session_state.username = None
if "balance" not in st.session_state:
    st.session_state.balance = 0
if "task_status" not in st.session_state:
    st.session_state.task_status = {}
if "show_topup" not in st.session_state:
    st.session_state.show_topup = False

models_price = {"rugpt3small_based_on_gpt2": 0.01}


def register_user(username: str, password: str) -> Dict[str, Any]:
    response = requests.post(f"{BACKEND_URL}/auth/register", json={"username": username, "password": password})
    response.raise_for_status()
    registration_result: Dict[str, Any] = response.json()
    return registration_result


def login_user(username: str, password: str) -> Dict[str, Any]:
    response = requests.post(f"{BACKEND_URL}/auth/login", json={"username": username, "password": password})
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    controller.set(
        TOKEN_COOKIE_NAME,
        data["access_token"],
        expires=datetime.now(timezone.utc) + timedelta(days=int(COOKIES_EXPIRE_DAYS)),
    )
    return data


def get_balance() -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {controller.get(TOKEN_COOKIE_NAME)}"}
    response = requests.get(f"{BACKEND_URL}/user/balance", headers=headers)
    response.raise_for_status()
    balance: Dict[str, Any] = response.json()
    return balance


def top_up_balance(username: str, amount: float) -> Optional[Dict[str, Any]]:
    if amount <= 0:
        return None
    headers = {"Authorization": f"Bearer {controller.get(TOKEN_COOKIE_NAME)}"}
    response = requests.put(
        f"{BACKEND_URL}/user/update_balance",
        json={"username": username, "amount": amount},
        headers=headers,
    )
    response.raise_for_status()
    top_up_balance_result: Dict[str, Any] = response.json()
    return top_up_balance_result


def generate_text(
    model_name: str,
    prompt: str,
    max_length: int,
    temperature: float,
    top_k: int,
    top_p: float,
) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {controller.get(TOKEN_COOKIE_NAME)}"}
    response = requests.post(
        f"{BACKEND_URL}/model/generate_text?model_name={model_name}",
        json={
            "prompt": prompt,
            "max_length": max_length,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
        },
        headers=headers,
    )
    response.raise_for_status()
    generation_result: Dict[str, Any] = response.json()
    return generation_result


def logout():
    st.session_state.username = None
    st.session_state.balance = 0
    st.session_state.task_status = {}
    controller.remove(TOKEN_COOKIE_NAME)
    st.success("Вы вышли из системы.")


def update_balance():
    try:
        result = get_balance()
        st.session_state.balance = result["balance"]
        st.session_state.username = result["username"]
    except Exception:
        pass


def main_page():
    with st.sidebar:
        balance_placeholder = st.empty()
        balance_placeholder.markdown(f"### Баланс: {st.session_state.balance:.2f} 💰")

        if st.button("Пополнить баланс", use_container_width=True):
            st.session_state.show_topup = not st.session_state.show_topup

        if st.session_state.show_topup:
            amount = st.number_input("Сумма пополнения:", min_value=0, step=10)
            if st.button("Подтвердить пополнение"):
                try:
                    result = top_up_balance(st.session_state.username, amount)
                    if result is not None:
                        st.success(f"Баланс пополнен. Новый баланс: {result['balance']}")
                    else:
                        st.error("Введенная сумма должна быть больше 0.")
                    update_balance()
                    balance_placeholder.markdown(f"### Баланс: {st.session_state.balance:.2f} 💰")
                except Exception as e:
                    st.error(f"Ошибка: {str(e)}")

        if st.button("Выйти", use_container_width=True):
            logout()
            st.rerun()

        max_length = st.number_input("Max length:", min_value=1, value=40, step=5)
        temperature = st.slider("Temperature:", min_value=0.01, value=1.0, step=0.01)
        top_k = st.number_input("Top K:", min_value=1, value=10, step=1)
        top_p = st.slider("Top P:", min_value=0.01, max_value=1.0, value=0.95, step=0.01)
        model = st.selectbox("Model:", ["rugpt3small_based_on_gpt2"])

    st.title(f"Добро пожаловать, {st.session_state.username}!")
    prompt = st.text_area("Введите текст:", height=175)

    if st.button("Сгенерировать текст"):
        if st.session_state.balance < max_length * models_price[model]:
            st.error(f"Недостаточно средств для генерации текста длины {max_length}.")
        else:
            try:
                generation_result = generate_text(
                    model,
                    prompt,
                    max_length,
                    temperature,
                    top_k,
                    top_p,
                )

                text_generation_task_status_placeholder = st.empty()
                text_generation_task_status_placeholder.success("Текст успешно сгенерирован:")

                update_balance()
                balance_placeholder.markdown(f"### Баланс: {st.session_state.balance:.2f} 💰")

                generated_text_placeholder = st.empty()
                generated_text_placeholder.code(generation_result["text"], language="text")

            except Exception as e:
                st.error(f"Ошибка при генерации: {str(e)}")

    for task_id, status in st.session_state.task_status.items():
        if status == "completed" or status == "failed":
            st.write(f"Task {task_id}: {status}")


def auth_page():
    st.title("ИИ-генератор поэзии 🪶")
    tab1, tab2 = st.tabs(["Регистрация", "Вход"])

    with tab1:
        username = st.text_input("Имя пользователя", key="reg_username")
        password = st.text_input("Пароль", type="password", key="reg_password")
        if st.button("Зарегистрироваться"):
            try:
                register_user(username, password)
                st.success("Успешно! Теперь войдите в систему.")
            except Exception as e:
                st.error(f"Ошибка: {str(e)}")

    with tab2:
        username = st.text_input("Имя пользователя", key="login_username")
        password = st.text_input("Пароль", type="password", key="login_password")
        if st.button("Войти"):
            try:
                login_user(username, password)
                update_balance()
                st.success("Успешный вход")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка: {str(e)}")


def app():
    if controller.get(TOKEN_COOKIE_NAME) is None:
        auth_page()
    else:
        update_balance()
        main_page()


if __name__ == "__main__":
    app()
