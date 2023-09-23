import streamlit as st

def main():
    st.title("Rent Record")
    if 'access' not in st.session_state:
        st.session_state.access = False

    if not st.session_state.access:
        password = st.text_input("Please enter password")
        if password == "CoolSamuel87":
            st.session_state.access = True
            st.experimental_rerun()
    else:
        st.write("Samuel is Cool!!!!!!")

if __name__ == '__main__':
    main()