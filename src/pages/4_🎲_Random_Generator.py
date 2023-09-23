import random
import streamlit as st
import time

def main():
    st.title("Random Generator")

    if 'opts' not in st.session_state:
        st.session_state.opts = []

    opt = st.text_input("Please enter options!")

    if st.button("Add option"):
        st.session_state.opts.append(opt)
    st.write(f"Current Options: [ {' | '.join(st.session_state.opts)} ]")

    if st.button("choose!"):
        if st.session_state.opts:
            with st.spinner("Please wait..."):
                time.sleep(1.5)
            st.success(f"The final choice is ... {random.choice(st.session_state.opts)}!")
        else:
            st.error("There are no choices entered! Please enter choices")
        
    if st.button("clear choices"):
        del st.session_state.opts
        st.rerun()

if __name__ == "__main__":
    main()