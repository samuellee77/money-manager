import streamlit as st

def main():
    st.title("Change Log")

    md = """
    2023-07-07: change theme to light; add bad jokes and change log pages
    """
    st.markdown(md)

if __name__ == '__main__':
    main()