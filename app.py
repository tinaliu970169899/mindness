import streamlit as st
import google.generativeai as genai

# 1. 網站基本設定
st.set_page_config(page_title="正念衛教網站", page_icon="🌿", layout="centered")

# 2. 設定 API 金鑰 (請確保 Streamlit Secrets 已設定 GEMINI_API_KEY)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 【直接貼上您的設計】
# 請把 AI Studio 的 System Instruction 內容貼在下面引號內
my_design_instruction = """
請在此處貼上您在 AI Studio 左側寫的所有指令...
例如：你是一個專業的正念導師，請用故事感的方式介紹衛教內容...
"""

# 請參考 AI Studio 的參數設定
my_generation_config = {
  "temperature": 0.7,  # 請改為您在 AI Studio 設定的數值
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

# 4. 初始化模型
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=my_design_instruction,
    generation_config=my_generation_config
)

# 5. 網頁畫面呈現
st.title("🌿 正念衛教專區")
st.write("---")

# 讓網站一打開就根據您的設計「自動生成」內容
if "web_content" not in st.session_state:
    with st.spinner('正在載入您的設計內容...'):
        # 這裡的指令是觸發 AI 根據 System Instruction 開始撰寫
        response = model.generate_content("請依照設定的格式與語氣，直接呈現完整的正念衛教資訊。")
        st.session_state.web_content = response.text

# 顯示產出的內容
st.markdown(st.session_state.web_content)

st.divider()
st.caption("本網站內容由 Google Gemini 核心技術依照設計指令自動產出")
