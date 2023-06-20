import streamlit as st
from money_tracker import money_tracker as mt
import numpy as np

st.set_page_config(page_title="Samuel's APPPE!!")
members = ["Samuel", "Janice", "Jonathan", "Allison", "Ryliee", "Jeffy"]
money_group = mt(members)

def add():
    expense_name = st.text_input("Please enter the expense Name")
    participants = st.multiselect("Please select the members", members)
    payer = st.selectbox("Please select the payer", members)
    amount = st.number_input("Please enter the amount of this expense", min_value=0)
    flag = st.button("Add!")
    # money_group.add_expense(expense_name, amount, participants, payer)
    # st.success("Success!")

# Main Streamlit app
def main():
    st.title("Money Manager")
    st.caption("0.0 version by Samuel Lee (2023-06-16)")
    st.subheader("Add Expense!")
    with st.form("my_form"):
        expense_name = st.text_input("Please enter the expense Name")
        participants = st.multiselect("Please select the members", members)
        payer = st.selectbox("Please select the payer", members)
        amount = st.number_input("Please enter the amount of this expense", min_value=0)
        submitted = st.form_submit_button("Submit")
        if submitted:
            money_group.add_expense(expense_name, amount, participants, payer)
            st.success("Add successfully")

    tab1, tab2 = st.tabs(["📑Record", "📊OWED"])

    with tab1:
        if money_group.get_record().empty:
            st.write("The record is empty! Plz add something!")
        else:
            st.dataframe(money_group.get_record())
    with tab2:
        if money_group.get_record().empty:
            st.write("The record is empty! Plz add something!")
        else:
            person = st.selectbox("Which person you want to know?", members)
            if money_group.get_owed(person):
                st.caption("Negative value")
                st.dataframe(money_group.get_owed(person))
    
    
    
    
    
    # # Button to create a new member
    # if st.button("Add Expense"):
    #     if member_name:
    #         create_member(member_name)
    #         st.success(f"Member '{member_name}' created!")
    #     else:
    #         st.warning("Please enter a valid member name.")

if __name__ == '__main__':
    main()