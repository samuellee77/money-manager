import random
import streamlit as st

def main():
    st.title("Random Generator")

    if 'opts' not in st.session_state:
        st.session_state.opts = []

    opt = st.text_input("Please enter option!")

    if st.button("Add option"):
        st.session_state.opts.append(opt)

    st.write(f"Current Options: [ {' | '.join(st.session_state.opts)} ]")

    if st.button("choose!"):
        st.write(random.choice(st.session_state.opts))

    if st.button("clear"):
        del st.session_state.opts
        st.experimental_rerun()

if __name__ == "__main__":
    main()