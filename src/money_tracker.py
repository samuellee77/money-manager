import numpy as np
import pandas as pd
from datetime import datetime
class money_tracker:

    total_group = 0
    
    def __init__(self, members):
        '''
        A constructor to initialize the money tracker

        Params:
        members (list of str): a list of strings representing each person
        '''
        self.members = members
        self.expenses = pd.DataFrame()
        self.expenses["expense_name"]= np.nan
        self.expenses["amount"] = np.nan
        self.expenses["people"] = np.nan
        self.expenses["payer"] = np.nan
        self.expenses["date_created"] = np.nan

        self.members_payment = pd.DataFrame(index = self.members)
        lsts = []
        for i in range(len(self.members)):
            lsts.append([])
        amount_dict = {}
        for person in self.members:
            amount_dict[person] = 0
        dict_lsts = []
        for i in range(len(self.members)):
            dict_lsts.append(amount_dict)
        self.members_payment['unpaid_record'] = lsts
        self.members_payment['amount_owed'] = dict_lsts

        money_tracker.total_group += 1

        return

    def clear(self):
        '''clear the money tracker group'''
        del self.expenses
        del self.members_payment
        money_tracker.total_group -= 1
        return

    def price_after_tax_and_tip(self, amount, tax_rate, tip):
        '''
        A method to calculate total price after tax and tip.

        Params:
        amount (int or float): the original amount
        tax_rate (float): the tax rate
        tip (int or float): the tip given

        Return:
        int or float: the total price after tax and tip
        '''
        return amount * (1 + tax_rate) + tip

    def add_expense(self, expense_name, amount, people, payer):
        '''
        A method to add an expense to the money tracker

        Params:
        expense_name (str): the name of the expense
        amount (int or float): the amount of the expense
        people (list of str): the people who share this expense
        payer (str): the person who pay this expense
        '''
        curr = datetime.now()
        time_created = f"{curr.month}/{curr.date} {curr.hour}:{curr.minute}"
        self.expenses.loc[len(self.expenses.index)] = [expense_name, amount, people, payer, time_created]
        shared_amount = round(amount / len(people), 2)
        for person in self.members:
            if person == payer:
                self.members_payment.at[person, 'unpaid_record'].append(('payer', -amount))
            elif person in people:
                self.members_payment.at[person, 'unpaid_record'].append((payer, shared_amount))
            else:
                continue
        return

    def payment_needed(self, name):
        '''
        A method to summarize each person's debt and who he/she owes

        Param:
        name (str): the person name

        Returns:
        a dictionary with names as keys and the amount of debt as values.
        '''
        debts = {}
        people = self.members.copy()
        for person in people:
            debts[person] = 0
        records = self.members_payment.loc[name].get('unpaid_record')
        for record in records:
            if record[0] != 'payer':
                debts[person] += record[1]
        return debts

    def update(self):
        '''A method to update members_payment's 'amount_owed' column'''
        for person in self.members:
            self.members_payment.loc[person]['amount_owed'] = self.payment_needed(person)
        return
    
    def pay(self, payer, recipient, amount):
        '''
        A method that payer pay the 'amount' to the recipient and update the
        members_payment's 'amount_owed' column

        Params:
        payer: the name of the payer (str)
        recipient: the name of the recipient (str)
        amount: the amount of money paid to the recipient (int or float)
        '''
        record = self.members_payment.loc[payer]['unpaid_record']
        amount_needed = sum([tup[1] for tup in record if tup[0] == recipient])
        if amount_needed == amount:
            self.members_payment.loc[payer]['unpaid_record'] = []
            self.members_payment.loc[payer]['amount_owed'][recipient] -= amount
        return