from money_tracker import money_tracker as mt

today = mt(["Samuel", "Jonathan", "Janice", "Allison"])
today.add_expense("market", 3.99 + 6.99 + 5.49, ["Samuel"], "Janice")
today.add_expense("Jonathan_dinner", 21.99*1.143, ["Jonathan"], "Janice")
today.add_expense("Allison_dinner", 21.99*1.143 + 20.99*1.143, ["Allison"], "Janice")
today.add_expense("Samuel_dinner", 17.99*1.143, ["Samuel"], "Janice")

today.update()
print(today.get_owed("Samuel"))
print(mt.numbers())

second = mt(["Cammeele", "Janice", "Allison"])
print(mt.numbers())