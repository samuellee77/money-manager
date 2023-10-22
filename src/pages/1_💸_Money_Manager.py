import streamlit as st
from money_tracker import money_tracker as mt
import numpy as np
import pandas as pd
import io

st.set_page_config(page_title="Samuel's APPPE!!")
members = ["Samuel", "Janice", "Jonathan", "Allison", "Ryliee", "Jeffy"]

if 'money_group' not in st.session_state:
    st.session_state.money_group = mt(members)

def to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    processed_data = output.getvalue()
    return processed_data

# Main Streamlit app
def main():
    st.title("💸 Money Manager")
    st.caption("1.0 version by Samuel Lee (2023-07-03)")
    tab_add, tab_del = st.tabs(["ADD", "DELETE"])
    with tab_add:
        st.subheader("Add Expense!")
        with st.form("my_form"):
            expense_name = st.text_input("Please enter the expense Name")
            participants = st.multiselect("Please select the members", members)
            payer = st.selectbox("Please select the payer", members)
            amount = st.number_input("Please enter the amount of this expense", min_value=0.0)
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.session_state.money_group.add_expense(expense_name, amount, participants, payer)
                st.success("Add successfully")
    with tab_del:
        st.subheader("Delete Expense!")
        expense_name = st.text_input("Please enter the name of the expense you want to delete")
        submitted = st.button("Delete")
        if expense_name:
            st.warning("Are you sure to delete this expense?")
            submitted = st.button("Pretty Sure!")
            if submitted:
                flag = st.session_state.money_group.del_expense(expense_name)
                if flag:
                    st.success("Delete successfully")
                else:
                    st.error("Failed to delete! Are you sure this is the correct expense name?")
    
    tab1, tab2, tab3 = st.tabs(["🧾TAX", "📑Record", "📊OWED"])

    with tab1:
        st.subheader("Tax Calculator Tool")
        col1, col2 = st.columns(2)
        with col1:
            with st.form("after_form"):
                st.subheader("After Tax & Tip")
                before_amount = st.number_input("Please enter the amount of this expense before tax",
                                                 min_value=0.0, format="%.2f")
                tax_rate = st.number_input("Please enter tax rate in decimal (e.g. 0.0775)", 
                                           min_value=0.0, value=0.0775, format="%.4f")
                tip = st.number_input("Please enter the amount of tip", min_value=0.0, format="%.2f")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    after_amount = round(before_amount * (1 + tax_rate) + tip, 3)
                    st.success(f"The total amount after tax & tip is {after_amount}!")
        with col2:
            with st.form("before_form"):
                st.subheader("Before Tax & Tip")
                after_amount = st.number_input("Please enter the amount of this expense after tax & tip", 
                                               min_value=0.0, format="%.2f")
                tax_rate = st.number_input("Please enter tax rate in decimal (e.g. 0.0775)",
                                           min_value=0.0, value=0.0775, format="%.4f")
                tip = st.number_input("Please enter the amount of tip", min_value=0.0, format="%.2f")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    before_amount = round((after_amount - tip) / (1 + tax_rate), 3)
                    st.success(f"The original amount before tax & tip is {before_amount}!")
    with tab2:
        if st.session_state.money_group.get_record().empty:
            st.write("The record is empty! Plz add something!") 
        else:
            st.dataframe(st.session_state.money_group.get_record())
            st.write(f"Total amount: {st.session_state.money_group.get_record().get('amount').sum()}")
            df_xlsx = to_excel(st.session_state.money_group.get_record())
            st.download_button(label='📥 Download Records',
                                data=df_xlsx,
                                file_name='records.xlsx')
    with tab3:
        if st.session_state.money_group.get_record().empty:
            st.write("The record is empty! Plz add something!")
        else:
            person = st.selectbox("Which person you want to know?", members)
            if st.session_state.money_group:
                st.caption("Negative value means the person owes you")
                output_string = person + ": "
                for key, value in st.session_state.money_group.get_owed(person):
                    output_string += f" {key}: {round(value)}"
                st.write(output_string)
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