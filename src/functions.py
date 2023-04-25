from money_tracker import *

test = money_tracker(["Samuel", "Jonathan", "Janice"])
print(test.members)
print('\n')
print(test.expenses)
print('\n')
print(test.members_payment)
print('\n')

test.add_expense("haha", 10, ["Samuel"], "Janice")

test.add_expense("idiot", 30, ["Jonathan", "Samuel"], "Janice")
print(test.expenses)
print('\n')
print(test.members_payment)
print('\n')

print(test.payment_needed('Jonathan'))
print(money_tracker.total_group)

test.update()
print(test.members_payment)

test.pay('Samuel', 'Janice', 25)
print(test.members_payment)
print('\n')
print(test.payment_needed('Samuel'))