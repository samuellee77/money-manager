from datetime import date
import numpy as np
import pandas as pd


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

        self.member_index = {}
        for i in range(len(self.members)):
            self.member_index[self.members[i]] = i

        self.members_payment = pd.DataFrame(index=self.members)
        lsts = []
        for i in range(len(self.members)):
            lsts.append([])
        amount_dict = {}
        for person in self.members:
            amount_dict[person] = 0
        dict_lsts = []
        for i in range(len(self.members)):
            dict_lsts.append(amount_dict.copy())
        self.members_payment['unpaid_record'] = lsts
        self.members_payment['amount_owed'] = dict_lsts

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
        for person in self.members:
            if person == payer and person in people:
                self.members_payment.at[person, 'unpaid_record']\
                    .append(('payer', - round(shared_amount * (len(people) - 1), 2)))
            elif person == payer:
                self.members_payment.at[person, 'unpaid_record'].append(('payer', - round(amount, 2)))
            elif person in people:
                self.members_payment.at[person, 'unpaid_record'].append((payer, shared_amount))
            else:
                continue

    def update(self):
        '''A method to update members_payment's 'amount_owed' column'''
        amount_owed_lst = self.members_payment.get('amount_owed').tolist()
        people = self.members.copy()
        for person in people:
            records = self.members_payment.loc[person].get('unpaid_record')
            for record in records:
                if record[0] != 'payer':
                    amount_owed_lst[self.member_index[person]][record[0]] += record[1]
                    amount_owed_lst[self.member_index[record[0]]][person] -= record[1]
        self.members_payment.assign(amount_owed=pd.Series(amount_owed_lst))

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
        record = self.members_payment.loc[payer]['unpaid_record']
        amount_needed = sum([tup[1] for tup in record if tup[0] == recipient])
        if amount_needed == amount:
            self.members_payment.at[payer, 'amount_owed'][recipient] -= amount
            self.members_payment.at[payer, 'unpaid_record'] = []
            return True
        return False
