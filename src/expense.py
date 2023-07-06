class expense:
    def __init__(self, amount: float, payer: str, debtor: str, recorded=False):
        self.amount = amount
        self.payer = payer
        self.debtor = debtor
        self.recorded = recorded

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