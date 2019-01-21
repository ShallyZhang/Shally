import datetime # 导入时间库
import hashlib  #  导入哈希函数库
from Transaction import Transaction # 导入交易类

class microblock:   # 交易块的类，也称作microblock 的类

    def __init__(self,previoushash):
        self.transactionlist = []   # 交易数据列表
        self.timestamp = datetime.datetime.now()       # 当前交易块时间
        self.hash = None            # 交易块hash
        self.previoushash = previoushash    # 上一个块的hash

    def addTransaction(self,data):  # 添加新的交易到交易数据列表
            self.transactionlist = self.transactionlist + data

    def set_microhash(self):    # 设置microblock 的自身ID
        combination =  str(self.timestamp) + str(self.previoushash)
        for trans in self.transactionlist:
            combination = combination + str(trans)
        self.hash = hashlib.sha256( combination.encode("utf-8")).hexdigest()

    def __repr__(self):
        return "\nIndex: " + str(self.index) + "\nPreviousHash: " + str(self.previoushash) + "\nTransactionlist: " + str(len(self.transactionlist)) \
               + "\nTimeStamp: " + str(self.timestamp) + "\nHash: " + str(self.hash)+ "\n"

