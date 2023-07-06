from datetime import date
import numpy as np
import pandas as pd
from expense import expense

class money_tracker:
    '''
    A class of money_tracker, which can be used to store expense records and
    calculate the money owed by each person
    '''
    total_group = 0        
    
    def __init__(self, members):
        '''
        A constructor to initialize the money tracker

        Params:
        members (list of str): a list of strings representing each person
        '''
        self.members = members
        self.expenses = pd.DataFrame()
        self.expenses["amount"] = np.nan
        self.expenses["people"] = np.nan
        self.expenses["payer"] = np.nan
        self.expenses["date_created"] = np.nan
        self.expense_list = []

        self.members_payment = pd.DataFrame(index=self.members)
        self.members_payment['amount_owed'] = \
            [{person:0 for person in self.members} for i in range(len(self.members))]
        money_tracker.total_group += 1

    def __str__(self):
        return ", ".join(self.members) + " are in the money group!"

    def __del__(self):
        '''clear the money tracker group'''
        money_tracker.total_group -= 1

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
        people (str): the people who share this expense
        payer (str): the person who pay this expense
        '''
        curr = date.today()
        time_created = str(curr)
        for ppl in people:
            if not ppl in self.members:
                raise NameError()
        self.expenses.loc[expense_name] = [amount, people, payer, time_created]
        shared_amount = round(amount / len(people), 2)
        # Place to edit the record system
        for ppl in people:
            if not ppl == payer:
                self.expense_list.append(expense(shared_amount, payer, ppl))
        for exp in self.expense_list:
            if not exp.get_recorded():
                self.members_payment.at[exp.get_debtor(), 'amount_owed'][exp.get_payer()] += exp.get_amount()
                self.members_payment.at[exp.get_payer(), 'amount_owed'][exp.get_debtor()] -= exp.get_amount()
                exp.set_recorded(True)

    def del_expense(self, expense_name):
        if not expense_name in self.expenses.index:
            return False
        people = self.expenses.loc[expense_name].get('people')
        payer = self.expenses.loc[expense_name].get('payer')
        amount = self.expenses.loc[expense_name].get('amount')
        shared_amount = round(amount / len(people), 2)
        for exp in self.expense_list:
            if exp.get_amount() == shared_amount and exp.get_payer() == payer and exp.get_debtor() in people:
                if exp.get_recorded():
                    self.members_payment.at[exp.get_debtor(), 'amount_owed'][exp.get_payer()] -= exp.get_amount()
                    self.members_payment.at[exp.get_payer(), 'amount_owed'][exp.get_debtor()] += exp.get_amount()
        self.expenses.drop(expense_name, inplace=True)
        return True

    def get_owed(self, person):
        return self.members_payment.get('amount_owed').loc[person]

    def get_record(self):
        return self.expenses

    def pay(self, payer, recipient, amount):
        '''
        A method that payer pay the 'amount' to the recipient and update the
        members_payment's 'amount_owed' column

        Params:
        payer: the name of the payer (str)
        recipient: the name of the recipient (str)
        amount: the amount of money paid to the recipient (int or float)
        '''
        amount_needed = self.members_payment.at[recipient, 'amount_owed'][payer]
        if (amount_needed == -amount) and (not payer == recipient):
            self.members_payment.at[payer, 'amount_owed'][recipient] -= amount
            self.members_payment.at[recipient, 'amount_owed'][payer] += amount
            return True
        else:
            return False
        # record = self.members_payment.loc[payer]['unpaid_record']
        # amount_needed = sum([tup[1] for tup in record if tup[0] == recipient])
        # if amount_needed == amount:
        #     self.members_payment.at[payer, 'amount_owed'][recipient] -= amount
        #     self.members_payment.at[payer, 'unpaid_record'] = []
        #     return True
        # return False
