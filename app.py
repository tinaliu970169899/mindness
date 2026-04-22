import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. 網頁介面升級 (加上側邊欄與專業排版)
# ==========================================
st.set_page_config(page_title="專屬 AI 系統", page_icon="✨", layout="wide")

with st.sidebar:
    st.title("⚙️ 系統控制台")
    st.markdown("這是我透過 Google AI Studio 核心打造的專屬系統。")
    st.divider() # 分隔線
    
    # 加上一個清除對話紀錄的按鈕，感覺更專業
    if st.button("🗑️ 清除對話紀錄"):
        st.session_state.messages = []
        st.rerun()

st.title("✨ 核心 AI 助手")

# ==========================================
# 2. 注入 AI Studio 的「靈魂」(系統提示詞)
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 👇 這裡最重要！把您在 AI Studio 設定的角色背景寫在這裡
my_system_prompt = """
你是我的專屬智能助手。
請用溫和、專業的語氣回答我的問題。
(您可以在這裡貼上您在 AI Studio 的 System Instructions，
 把這個 AI 設定成任何您想要的專家角色！)
"""

# 在初始化模型時，把系統提示詞 (system_instruction) 加進去
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=my_system_prompt
)

# ==========================================
# 3. 聊天室核心運作邏輯
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示過去的對話紀錄
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收使用者的輸入
if prompt := st.chat_input("請輸入您的指令..."):
    # 顯示使用者的訊息
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 呼叫 Gemini API 產生回覆
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    
    # 儲存 AI 的回覆到紀錄中
    st.session_state.messages.append({"role": "assistant", "content": response.text})
