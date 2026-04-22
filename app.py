import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="專屬 AI 系統", page_icon="✨", layout="wide")

with st.sidebar:
    st.title("⚙️ 系統控制台")
    st.markdown("這是我透過 Google AI Studio 核心打造的專屬系統。")
    st.divider()
    if st.button("🗑️ 清除對話紀錄"):
        st.session_state.messages = []
        st.rerun()

st.title("✨ 核心 AI 助手")

# 設定金鑰
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 您的專屬系統提示詞
my_system_prompt = """
你是我的專屬智能助手。
請用溫和、專業的語氣回答我的問題，並具備臨床心理學的專業素養。
"""

# 使用最穩定的標準模型名稱
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=my_system_prompt
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("請輸入您的指令..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
