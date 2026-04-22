import streamlit as st
import google.generativeai as genai

# 1. 網頁外觀設定 (換上正念的風格)
st.set_page_config(page_title="正念衛教專屬空間", page_icon="🌿", layout="wide")

with st.sidebar:
    st.title("🌿 正念導航控制台")
    st.markdown("這是我專屬打造的正念衛教智能系統。")
    st.divider()
    if st.button("🗑️ 重新開始對話"):
        st.session_state.messages = []
        # 加入預設的歡迎語
        st.session_state.messages.append({"role": "assistant", "content": "你好！我是你的專屬正念導航員 🌿 \n\n想了解什麼是正念，或者現在就想開始一段簡單的放鬆練習嗎？請隨時告訴我！"})
        st.rerun()

st.title("🌿 正念衛教核心 AI 助手")

# 2. 設定金鑰
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ==========================================
# 3. 【AI Studio 的靈魂：您的專屬設計與提示詞】
# ==========================================
my_system_prompt = """
你是一個專業、溫暖且具備臨床心理學素養的正念導航員。
請依照以下風格與結構與使用者互動：

【特色與風格】
1. 有故事感：一開始就讓使用者覺得被帶入平靜、放鬆的情境。
2. 有教育感：內容簡單，邏輯清楚，讓新手也能快速理解。
3. 視覺風格：排版要現代、乾淨、有層次感（多使用條列式或粗體重點）。
4. 語氣：自然、誠懇、有說服力，像是一個值得信賴的專業朋友，絕對不要生硬。

【核心內容範圍】
當使用者詢問時，請自然地帶入以下資訊：
- 正念的介紹與衛教說明。
- 什麼時候適合做正念？
- 提供可以進行正念練習的具體方法或情境。
- 結尾請總是給予一句溫暖的總結與鼓勵 (CTA)。
"""

# 4. 初始化模型
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=my_system_prompt
)

# 5. 聊天室核心運作
if "messages" not in st.session_state:
    # 預設第一句話，讓畫面不再全白！
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是你的專屬正念導航員 🌿 \n\n想了解什麼是正念，或者現在就想開始一段簡單的放鬆練習嗎？請隨時跟我說！"}
    ]

# 顯示對話紀錄
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收輸入與產出回覆
if prompt := st.chat_input("請輸入您的問題，例如：請幫我介紹什麼是正念？"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
