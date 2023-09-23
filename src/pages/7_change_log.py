import streamlit as st

def main():
    st.title("Change Log")

    md = """
    2023-08-08: add download function to download current records
    2023-07-24: add random generator
    2023-07-07: add bad jokes and change log pages
    """
    st.markdown(md)

if __name__ == '__main__':
    main()