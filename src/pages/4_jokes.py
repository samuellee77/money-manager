import json
import streamlit as st
import random
import os 

def main():
    st.title("爛笑話")
    if st.button("生成"):
        with open("src/data/joke.json", encoding='utf-8') as f:
            data = json.load(f)
            title, content = random.choice(list(data.items()))
            st.subheader(title)
            for i in range(len(content)):
                st.write(content[i])

if __name__ == '__main__':
    main()