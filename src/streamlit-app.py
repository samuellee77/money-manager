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
    if expense_name and participants and payer and amount and flag:
        money_group.add_expense(expense_name, amount, participants, payer)
        st.success("Success!")

# Main Streamlit app
def main():
    st.title("Money Manager")
    st.caption("0.0 version by Samuel Lee (2023-05-21)")
    add()
    st.write(money_group.get_record())
    # # Button to create a new member
    # if st.button("Add Expense"):
    #     if member_name:
    #         create_member(member_name)
    #         st.success(f"Member '{member_name}' created!")
    #     else:
    #         st.warning("Please enter a valid member name.")

if __name__ == '__main__':
    main()