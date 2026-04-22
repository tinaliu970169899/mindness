import streamlit as st
import google.generativeai as genai

# 1. 網頁頁面設定 (正念清爽風格)
st.set_page_config(page_title="正念衛教空間", page_icon="🌿", layout="centered")

# 隱藏 Streamlit 預設的選單按鈕，讓它看起來更像真正的衛教網站
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. 設定 AI 金鑰
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ==========================================
# 3. 【這就是您在 AI Studio 的靈魂】
# 我們把系統提示詞設定成「網站編輯員」
# ==========================================
my_system_prompt = """
你是一個專業的「正念衛教網站編輯」。
請依照使用者的需求，撰寫出一篇具有故事感、教育意義且視覺美觀的衛教文章。
排版請多使用 Markdown 語法（例如：# 大標題, ## 小標題, **粗體**, 條列式）。
語氣要溫暖且專業，結尾要有一個暖心的鼓勵。
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=my_system_prompt
)

# 4. 網站標題與視覺
st.image("https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&q=80&w=1000", use_column_width=True)
st.title("🌿 找回內心的平靜：正念衛教專區")
st.subheader("Mindfulness Education Space")
st.divider()

# 5. 自動產生衛教內容 (一打開就執行)
# 我們讓 AI 針對「正念衛教」的主題自動寫出一篇精美的文章
@st.cache_data # 這可以讓網站跑得更快，不必每次重整都重新問 AI
def get_initial_content():
    response = model.generate_content("請幫我撰寫一份完整的『正念初學者衛教指南』，包含什麼是正念、好處、以及三個簡單的練習方法。")
    return response.text

with st.spinner('正在為您佈置平靜的衛教空間...'):
    content = get_initial_content()
    st.markdown(content)

# 6. (選配) 下方保留一個與專家互動的小框框
st.divider()
st.write("### 💬 還有其他正念方面的疑問嗎？")
user_q = st.text_input("您可以輸入感興趣的主題（例如：失眠、壓力）：")

if user_q:
    with st.spinner('正在為您查詢建議...'):
        q_response = model.generate_content(f"關於使用者提到的「{user_q}」，請提供相關的正念練習建議。")
        st.info(q_response.text)

# 頁尾
st.divider()
st.caption("© 2026 正念衛教空間 | 以 Google Gemini 核心技術驅動")
