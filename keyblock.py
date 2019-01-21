import datetime  # 导入时间库
import hashlib  # 导入哈希函数库
import time
from Transaction import Transaction  # 导入交易类
from microblock import microblock     # 导入microblock类
# 构建一个keyblock，在将交易信息放入到块中之后，需要矿工进行挖块，一旦成功，便将这个块连接到最长链上
class keyblock:  # 交易块的类，也称作microblock 的类

    def __init__(self, previoushash, difficulty):
        self.transactionlist = []   # 交易数据列表
        self.timestamp = datetime.datetime.now()    # 当前交易块时间
        self.hash = None           # 交易块hash
        self.previoushash = previoushash    # 上一个块的hash
        self.difficulty = difficulty      # 定义挖矿的难度
        self.nonce = 0           # 一个随机值

    def addTransaction(self, data):  # 添加新的交易到交易数据列表
        self.transactionlist = self.transactionlist + data

    def set_keyhash(self):
        combination = str(self.timestamp) + str(self.previoushash) + str(self.nonce)
        for trans in self.transactionlist:
            combination = combination + str(trans)
        self.hash = hashlib.sha256( combination.encode("utf-8")).hexdigest()


    def proof_of_work(self):
        start = 0
        self.set_keyhash()
        while [v for v in self.hash[start:self.difficulty]] != ['0' for v in range(start, self.difficulty)]:
            self.nonce = self.nonce + 1
            self.set_keyhash()
        """print("Mining a block:" + "\nPrevious hash: " + str(self.previoushash) +
              "\nHash: " + str(self.hash) + "\nTransactionList: " + str(self.transactionlist) + "\nDifficulty: "
              + str(self.difficulty) + "\nNonce: " + str(self.nonce) + "\nTimestamp: " + str(self.timestamp))"""

    def __repr__(self):
        return "\nblock PreviouHash: " + str(self.previoushash) + "\nblock Transactionlist: " + str(len(self.transactionlist)) \
               + "\nblock TimeStamp: " + str(self.timestamp) + "\nblock Hash: " + str(self.hash) + "\nblock Difficulty: " \
               + str(self.difficulty) + "\nblock Nonce: " + str(self.nonce) + "\n"
