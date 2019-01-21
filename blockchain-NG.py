import math
import random
import time
from Node import Node
from microblock import microblock
from keyblock import keyblock

# 构造节点网络
class Nodenet:
    def __init__(self):
        self.NodeList = []

    # 生成节点
    def GenerateNode(self, index,x,y,speed):
        Gnode = Node(index, x, y, speed)
        self.NodeList.append(Gnode)

    #   计算所有节点的邻居节点
    def calculate_all_neiborNodes(self):
        for fnum in range(0, len(self.NodeList)):
            for snum in range(fnum + 1, len(self.NodeList)):
                R = pow((self.NodeList[fnum].x - self.NodeList[snum].x), 2) + pow(
                    (self.NodeList[fnum].y - self.NodeList[snum].y), 2)
                if R <= pow(self.NodeList[fnum].radius, 2):
                    self.NodeList[fnum].neiborlist.append(self.NodeList[snum])
                    self.NodeList[snum].neiborlist.append(self.NodeList[fnum])
    # 从最长链节点开始通过深度优先遍历，扩散到网络中所有节点下载最长链节点的最长链
    def DFS(self, leader, depth, visit, block):
        if depth < 5:
            for node in leader.neiborlist:
                if node not in visit:
                    if block not in node.kmblockchain:
                        leader.sendblock(block,node)
                        visit.append(node.index)
                        visit = list(set(visit))
                        depth = depth + 1
                        self.DFS(node, depth, visit, block)

    # 找到所有节点到leader的路径
    def findpath(self, node, leader, path):
        path.append(node)
        if leader in node.neiborlist:
            path.append(leader)
            return
        else:
            for fnode in node.neiborlist:
                if fnode not in path:
                    if leader in path:
                        return
                    self.findpath(fnode, leader, path)

    # 沿着一条路径将交易发送给leader
    def SendTrans(self, node, leader, path, data):
        for index in range(1, len(path) - 1):
            knode = path[index]
            knode.recie_A = knode.recie_A + len(data)
        knode = path[-1]
        knode.recie_A = knode.recie_A + len(data)
        knode.transactionlists = knode.transactionlists + data

    # 随着时间的变化，节点也将移动
    def moveNode(self, time):
        for node in self.NodeList:
            theta = random.randint(0, 360)
            s = node.speed * time
            node.x = node.x + s * math.cos(theta * math.pi / 180)
            node.x = round(node.x, 2)
            node.y = node.y + s * math.sin(theta * math.pi / 180)
            node.y = round(node.y, 2)

    # 表示网络中的节点信息
    def __repr__(self):
        return "The information of Node:\n" + str(self.NodeList)

if __name__ == '__main__':
    nodenet = Nodenet() # 初始化一个网络
    global_time = 0  # 定义一个全局初始时间
    ktime = 100  # 设置每100秒生成一个keyblock
    mtime = 10  # 每10 秒生成一个mincroblock
    # 设置块的大小为1M,带宽为 512bit,传输速率为 512bps，发送时间是 2
    comfirm_time = 2  # 每个块确认加入到链的时间是keyblock传输到节点的时间
    # 生成10个节点，并计算出他们的邻居节点
    num_node = 1
    speed = 20
    while num_node <= 100:
        x = random.randint(0, 1000)
        y = random.randint(0, 500)
        nodenet.GenerateNode(num_node,x,y,speed)
        num_node = num_node + 1
    # 计算出每个节点的邻居节点
    nodenet.calculate_all_neiborNodes()
    # 每个节点开始初始化生成一些交易形成交易池
    for tnode in nodenet.NodeList:
        num_trans = random.randint(100, 200)
        while num_trans > 0:
            tnode.Generate_tansaction()
            num_trans = num_trans - 1
    # 节点生成创世块
    for node in nodenet.NodeList:
        node.create_genesis()
    flag = 6
    # 节点开始挖矿
    while flag > 0:
        # 网络中有节点挖矿成功，生成keyblock
        leader = random.choice(nodenet.NodeList)
        latest_block = leader.kmblockchain[-1]
        block = leader.miner(latest_block, 3)
        leader.kmblockchain.append(block)
        global_time = global_time + ktime
        # 挖矿时间比较长，节点应该发生了移动
        nodenet.moveNode(ktime)
        for node in nodenet.NodeList:
            node.neiborlist = []
        nodenet.calculate_all_neiborNodes()

        # 将keyblock扩散给其他节点，同时其他节点生成micrblock
        visit = [leader.index]
        nodenet.DFS(leader, 0, visit, block)
        interval = 0
        while interval < ktime:
            latest_block = leader.kmblockchain[-1]
            block = leader.Gen_microblock(latest_block)
            leader.kmblockchain.append(block)
            nodenet.moveNode(mtime)
            for node in nodenet.NodeList:
                node.neiborlist = []
            nodenet.calculate_all_neiborNodes()
            # 将microblock扩散给其他节点
            visit = [leader.index]
            nodenet.DFS(leader, 0, visit, block)
            # 每个节点生成一些交易
            for tnode in nodenet.NodeList:
                num_trans = random.randint(30, 40)
                while num_trans > 0:
                    tnode.Generate_tansaction()
                    num_trans = num_trans - 1

            interval = interval + mtime
        flag = flag - 1
    print(nodenet)
    print(global_time)

















