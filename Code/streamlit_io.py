# streamlit_io.py
# 引入Streamlit包
import streamlit as st
# 获取输入文本
text = st.text_input("Input Something")
# 输出文本
st.text(text)
