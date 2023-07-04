import streamlit as st
from money_tracker import money_tracker as mt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Samuel's APPPE!!")
members = ["Samuel", "Janice", "Jonathan", "Allison", "Ryliee", "Jeffy"]

if 'money_group' not in st.session_state:
    st.session_state.money_group = mt(members)

# Main Streamlit app
def main():
    st.title("Money Manager")
    st.caption("1.0 version by Samuel Lee (2023-07-03)")
    st.subheader("Add Expense!")
    with st.form("my_form"):
        expense_name = st.text_input("Please enter the expense Name")
        participants = st.multiselect("Please select the members", members)
        payer = st.selectbox("Please select the payer", members)
        amount = st.number_input("Please enter the amount of this expense", min_value=0)
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.money_group.add_expense(expense_name, amount, participants, payer)
            st.success("Add successfully")

    tab1, tab2 = st.tabs(["📑Record", "📊OWED"])

    with tab1:
        if st.session_state.money_group.get_record().empty:
            st.write("The record is empty! Plz add something!")
            placeholder1 = st.empty()
        else:
            st.dataframe(st.session_state.money_group.get_record())
    with tab2:
        if st.session_state.money_group.get_record().empty:
            st.write("The record is empty! Plz add something!")
            placeholder2 = st.empty()
        else:
            person = st.selectbox("Which person you want to know?", members)
            if st.session_state.money_group:
                st.caption("Negative value means the person owes you")
                st.write(person + ": " + str(st.session_state.money_group.get_owed(person)))
    st.divider()
    st.subheader("Pay!")
    with st.form("pay_form"):
        payer = st.selectbox("Please select the payer", members)
        recipient = st.selectbox("Please select the receiver of this payment", members)
        amount = st.number_input("Please enter the amount of this payment", min_value=0)
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner('Processing, Please wait for a moment'):
                flag = st.session_state.money_group.pay(payer, recipient, amount)
            if flag:
                st.success("Successfully paid! Your record is now refreshed!")
            else:
                st.error("Payment failed! Are you sure you paid the correct amount to the correct person?")
    st.divider()
    st.write("Any issues? Please contact hsl023@ucsd.edu")
    st.write("GitHub Repo: https://github.com/samuellee77/money-manager")
    
if __name__ == '__main__':
    main()