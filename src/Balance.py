
class Balance:
    MIN_TO_DOLLAR_MULTIPLIER = 2/60

    PENALTY_MIN_FOR_ALERT = 5
    PENALTY_MONEY_FOR_ALERT = 0.25

    def __init__(self, balanceFilepath):
        self.balanceFilpath = balanceFilepath


    def changeBal(self, amount):
        with open(self.balanceFilpath, 'r') as file:
            currentBal = float(file.read())
        with open(self.balanceFilpath, 'w') as file:
            file.write(str(currentBal + amount))

    def getBal(self):
        with open(self.balanceFilpath, 'r') as file:
            return float(file.read())


    def changeBalWithTimeMin(self, focusMins):
        self.changeBal(focusMins * self.MIN_TO_DOLLAR_MULTIPLIER)



