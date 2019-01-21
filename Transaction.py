import datetime
class Transaction: #交易类
    def __init__(self, payer, recer, count): # ，，金额
        self.payer = payer  # 付款方
        self.recer = recer  # 收款方
        self.count = count  # 额度
        self.timestamp = datetime.datetime.now()    # 交易的时间

    def __repr__(self):
        return str(self.payer) + " pay " + str(self.recer) + " " + str(self.count) + " in " + str(self.timestamp)