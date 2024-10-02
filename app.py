import streamlit as st
from searcher import Searcher
searcher = Searcher('./data/wiki_zh.index', './data/wiki_map.txt')

st.title('Wiki搜索引擎')

query = st.text_input('输入你的查询', '')

if query:
    results = searcher.search(query, k=5)  # 可以调整 k 的值来改变返回的结果数量
    if results:
        st.subheader('搜索结果')
        for url in results:
            st.write(url)
    else:
        st.write('没有找到相关结果')