# streamlit_demo.py
import streamlit as st

# mask_filling_llm 是我实现的一个输入Prompt返回分数和生成文本的函数
from api.LLM import mask_filling_llm
# markdown方法会把输入的文本当做Markdown进行渲染并展示到前端上
st.markdown("# Prompt Console")
st.markdown("## Input Panel")
# 使用text_area进行多行输入
input = st.text_area("Prompt")
# 判断是否空文本
if input:
  # 调用方法
	generated = mask_filling_llm(input)
	st.markdown("## Output")
  # 展示调用方法返回的信息
	st.markdown(f"### Score:\n{generated['logit'][0]}")
	st.markdown(f"### Generated:")
	st.text(generated['output'][0])