import json
import streamlit as st
import random

def main():
    st.title("GRE Vocabulary Quiz")
    st.write("Test your GRE vocabulary knowledge with this quiz!")
    with open("src/data/vocab_dict.json", encoding='utf-8') as f:
        data = json.load(f)
    if st.button("Generate Quiz"):
        word, definition = random.choice(list(data.items()))
        st.session_state.word = word
        st.session_state.definition = definition
        st.subheader(word)
    if st.button("Show Answer"):
        st.subheader(st.session_state.word)
        st.write(st.session_state.definition)

if __name__ == '__main__':
    main()