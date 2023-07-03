class expense:
    def __init__(self, amount: float, payer: str, debtor: str, recorded=False, paid=False):
        self.amount = amount
        self.payer = payer
        self.debtor = debtor
        self.recorded = recorded
        self.paid = paid

    def get_payer(self):
        return self.payer
    
    def get_debtor(self):
        return self.debtor
    
    def get_amount(self):
        return self.amount
    
    def get_recorded(self):
        return self.recorded
    
    def set_recorded(self, flag: bool):
        self.recorded = flag
    
    def get_paid(self):
        return self.paid
    
    def set_paid(self, flag: bool):
        self.paid = flag