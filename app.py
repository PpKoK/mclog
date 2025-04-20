import streamlit as st
import openai
import re

# 设置页面标题和图标
st.set_page_config(page_title="MC错误分析器", page_icon="🧊")

# 侧边栏配置
with st.sidebar:
    st.title("配置")
    api_key = st.text_input("输入OpenAI API Key", type="password")
    openai.api_key = api_key
    model = st.selectbox("选择模型", ["gpt-3.5-turbo", "gpt-4"])

# 主界面
st.title("⛏️ Minecraft 错误日志分析器")
uploaded_file = st.file_uploader("上传日志文件", type=[".log", ".txt"])
log_text = st.text_area("或直接粘贴日志内容", height=200)

if st.button("分析日志"):
    if not api_key:
        st.error("请先输入API Key")
    elif not (uploaded_file or log_text):
        st.error("请提供日志内容")
    else:
        with st.spinner("AI正在分析中..."):
            # 读取日志内容
            if uploaded_file:
                log_content = uploaded_file.getvalue().decode("utf-8")
            else:
                log_content = log_text
            
            # 调用AI分析
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个专业的Minecraft错误分析专家。"},
                    {"role": "user", "content": f"请分析以下Minecraft错误日志，用中文回答：\n\n{log_content}"}
                ],
                temperature=0.3
            )
            
            # 显示结果
            st.subheader("分析结果")
            st.write(response.choices[0].message.content)
            
            # 提取关键信息（示例：Mod检测）
            mods = re.findall(r"mods?[/\\]([a-zA-Z0-9_-]+)", log_content)
            if mods:
                st.info(f"检测到可能涉及的Mod: {', '.join(set(mods))}")
