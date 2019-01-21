import datetime
import time
import random
from Transaction import Transaction
from keyblock import keyblock
from microblock import microblock
# 构建一个节点的类
class Node:
    def __init__(self,index,x,y,speed):
        self.index = index
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 250
        self.kmblockchain = []  # 存储的最长链
        self.transactionlists = []  # 交易池
        self.neiborlist = []    # 存储邻居节点
        self.recie_A = 0 # 节点收到的交易数量
        self.recie_B = 0 # 节点收到的块的数量
        self.recieB_A = 0 #节点收到的块中交易的数量

    # 节点可以自己生成一些交易，并将将以放入到交易池中
    def Generate_tansaction(self):
        # 给定一组字符串列表，随机从中选取一个字符串作为支付方和收钱方
        transactors = ['张三','李四','王五','赵六']
        payer = random.choice(transactors)
        recer = random.choice(transactors)
        # 随机生成一个5以内的浮点数作为支付金额
        count = random.uniform(0,2)
        count = round(count, 2)
        trans = Transaction(payer, recer,count)
        self.transactionlists.append(trans)

    # 节点可以生成创世块，并将其添加到链中
    def create_genesis(self):
        first_trans = Transaction("rewarder", "miner", "1.2")
        gene = keyblock('Genesis keyblock', 3)
        gene.transactionlist.append(first_trans)
        gene.proof_of_work()
        self.kmblockchain.append(gene)
    # 从交易池中获取一定数量的交易作为数据
    def getdata(self):
        num_trans = random.randint(30,40)
        if len(self.transactionlists) < num_trans:
            data = self.transactionlists  # 从交易列表中获取剩余的数据
            self.transactionlists = []  # 交易池为空
        else:
            data = self.transactionlists[0:num_trans]  # 从交易列表中选取部分数据
            self.transactionlists = self.transactionlists[num_trans:]  # 更新交易列表
        return data

    # 节点挖矿成功，生成keyblock,并且选取节点矿池中的交易封装到块中
    def miner(self,latestblock, difficulty):
        previoushash = latestblock.hash
        block = keyblock(previoushash, difficulty)
        data = self.getdata()
        block.addTransaction(data)
        block.proof_of_work()
        return  block

    # 节点确定为leader之后，生成一些microblock, 并且选取节点矿池中的交易封装到块中
    def Gen_microblock(self,latestblock):
        previoushash = latestblock.hash
        block = microblock(previoushash)
        data = self.getdata()
        block.transactionlist = block.transactionlist + data
        block.set_microhash()
        return block

    # 发送交易数据到节点的邻居节点
    def sendtransections(self,node):
        data = self.getdata()
        node.recie_A = node.recie_A + len(data)
        node.transactionlists = node.transactionlists + data

    # 节点生成block，并发送到其他节点
    def sendblock(self, block, node):
        node.recie_B = node.recie_B + 1
        node.recieB_A = node.recieB_A + len(block.transactionlist)
        node.kmblockchain.append(block)


    """def __repr__(self):
        return "\nNode index: " + str(self.index) + "\n Node x: " + str(self.x) + "\n Node y: " + str(self.y) + "\n Node speed: " + str(self.speed) \
               + "\n Node radius: " + str(self.radius) + "\n Node transactionlist: " + str(len(self.transactionlists)) + "\n Node neiborlist: " \
               + str(len(self.neiborlist)) + "\n Node kmblockchain: " + str(len(self.kmblockchain))"""

    """def __repr__(self):
    return "\n Node index: " + str(self.index) + " Node.x: " + str(self.x) + " Node.y: " + str(self.y) +\
           " Recie_A: " + str(self.recie_A) + " Recie_B: " + str(self.recie_B ) + " RecieB_A: " + str(self.recieB_A)"""

    def __repr__(self):
        return "\n Node index: " + str(self.index) + " Node.neighbor: " + str(len(self.neiborlist))  + " Node.speed: " + str(self.speed) +\
               " Recie_A: " + str(self.recie_A) + " Recie_B: " + str(self.recie_B ) + " RecieB_A: " + str(self.recieB_A)