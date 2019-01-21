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
        self.blockNodeindex = []    # 添加发送过块的节点index
    # 生成节点
    def GenerateNode(self,index):
        #   随机生成一个节点的x,y,speed,radius
        x = random.uniform(0,10)
        x = round(x, 2)
        y = random.uniform(0,10)
        y = round(y, 2)
        speed = random.uniform(0,0.05)
        speed = round(speed, 2)
        Gnode = Node(index,x,y,speed)
        self.NodeList.append(Gnode)

    #   计算所有节点的邻居节点
    def calculate_all_neiborNodes(self):
        for fnum in range(0, len(self.NodeList)):
            for snum in range(fnum + 1, len(self.NodeList)):
                R = pow((self.NodeList[fnum].x - self.NodeList[snum].x), 2) + pow((self.NodeList[fnum].y - self.NodeList[snum].y), 2)
                if R <= pow(self.NodeList[fnum].radius, 2):
                    self.NodeList[fnum].neiborlist.append(self.NodeList[snum])
                    self.NodeList[snum].neiborlist.append(self.NodeList[fnum])

    """# 重新对网络中节点的index编号
    def resortindex(self):
        index0 = 0
        for node in self.NodeList:
            node.index = index0
            index0 = index0 + 1"""

    # 将不在网络区域中的节点删除
    def delnode(self):
        List1 = []
        for node in self.NodeList:
            if 0 <= float(node.x) <= float(10) and 0 <= float(node.y) <= float(10):
                List1.append(node)
                # graphic.NodeList.remove(node)
        self.NodeList = List1

    # 从leader节点开始通过深度优先遍历，将块扩散到网络中其他节点（代码要修改）
    def DFS(self, long_node, depth, visit):
        if depth < 3:
            for node in long_node.neiborlist:
                if node not in visit:
                    node.kmblockchain = long_node.kmblockchain
                    visit.append(node.index)
                    visit = list(set(visit))
                    depth = depth + 1
                    self.DFS(node,depth,visit)

    # 随着时间的变化，节点也将移动
    def moveNode(self, time):
        for node in self.NodeList:
            theta = random.randint(0, 360)
            s = node.speed * time
            node.x = node.x + s * math.cos(theta * math.pi / 180)
            node.x = round(node.x,2)
            node.y = node.y + s * math.sin(theta * math.pi / 180)
            node.y = round(node.y, 2)

    # 表示网络中的节点信息
    def __repr__(self):
        return "The information of Node:\n" + str(self.NodeList)

if __name__ == '__main__':
    nodenet = Nodenet() # 初始化一个网络
    global_time = 0 #定义一个全局初始时间
    ktime = 100  # 设置每100秒生成一个keyblock
    mtime = 10  # 每10 秒生成一个mincroblock
    # 设置块的大小为1M,带宽为 512bit,传输速率为 512bps
    comfirm_time = 2  # 每个块确认加入到链的时间是keyblock传输到节点的时间
    # 生成10个节点，并计算出他们的邻居节点
    num_node = 0
    while num_node < 10:
        nodenet.GenerateNode(num_node)
        num_node = num_node + 1
    nodenet.calculate_all_neiborNodes()
    # 每个节点开始初始化生成一些交易形成交易池
    for tnode in nodenet.NodeList:
        num_trans = random.randint(5, 20)
        while num_trans > 0:
            tnode.Generate_tansaction()
            num_trans = num_trans - 1
    # 算力最强的节点生成创世块，并初始化区块链，并确定为leader
    long_node = random.choice(nodenet.NodeList)
    long_node.create_genesis()
    leader = long_node
    global_time = global_time + ktime
    flag = 1
    # 其他节点发送交易到leader
    while flag > 0:
        interval = 0  # 生成microblock 的
        while interval < ktime:
            for node in nodenet.NodeList:
                if leader in node.neiborlist:
                    node.sendtransections(leader)
            # 找到最长链的尾块，并且leader生成microblock
            latest_block = long_node.kmblockchain[-1]
            block = leader.Gen_microblock(latest_block)
            global_time = global_time + mtime
            interval = interval + mtime

            leader.sendblock(block,long_node)
            global_time = global_time + comfirm_time
            # 在网络中将最长链进行扩散，尽可能多的节点下载该最长链
            for node in nodenet.NodeList:
               if node in long_node.neiborlist:
                    node.kmblockchain = long_node.kmblockchain
            # 通过深度优先遍历，将最长链节点的连通图中每个节点都下载最长链
            visit = [long_node.index]
            nodenet.DFS(long_node, 4, visit)

        # 一个时间期间之后，节点开始移动
        nodenet.moveNode(ktime)
        # 计算并删除不再范围内的节点，重新对节点中的index编号
        nodenet.delnode()
        # 生成新的节点加入到网络中
        num_newnode = random.randint(2,5)
        latest_index = num_node
        numbernode = num_newnode + latest_index
        while num_node < numbernode:
            nodenet.GenerateNode(num_node)
            num_node = num_node + 1
        nodenet.calculate_all_neiborNodes()
        # 在网络中将最长链进行扩散，尽可能多的节点下载该最长链
        for node in nodenet.NodeList:
            if node in long_node.neiborlist:
                node.kmblockchain = long_node.kmblockchain
        # 通过深度优先遍历，将最长链节点的连通图中每个节点都下载最长链
        visit = [long_node.index]
        nodenet.DFS(long_node, 4, visit)
        # 各节点生成新的交易
        for tnode in nodenet.NodeList:
            num_trans = random.randint(5, 20)
            while num_trans > 0:
                tnode.Generate_tansaction()
                num_trans = num_trans - 1
        # 新节点挖矿成功，生成keyblock, 成为leader
        leader = random.choice(nodenet.NodeList)
        latest_block = long_node.kmblockchain[-1]
        block = leader.miner(latest_block,3)
        global_time = global_time + ktime
        # 将块发送给最长链节点
        if len(leader.kmblockchain) == len(long_node.kmblockchain):
            long_node = leader
        else:
            for node in leader.neiborlist:
                if len(node.kmblockchain) == len(long_node.kmblockchain):
                    long_node = node
                    break
        leader.sendblock(block,long_node)

        global_time = global_time + comfirm_time
        flag = flag - 1
    for node in nodenet.NodeList:
        print("\n Node Index: " + str(node.index) + " Node Recie_A: " + str(node.recie_A) + " Node Recie_B: " +
              str(node.recie_B) + " Node RecieB_A: " + str(node.recieB_A))