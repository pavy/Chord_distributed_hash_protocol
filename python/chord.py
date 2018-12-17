import os, sys, re, random
import argparse
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#from chord_protocol import ChordRing

class ChordNode:
    def __init__(self, node_num, m):
        self.finger_table = []
        self.node_num=node_num
        self.m=m
        for val in range(m):
            st = (self.node_num+2**val)%(2**self.m)
            end = (self.node_num+2**(val+1))%(2**self.m)
            node = self##self.find_successor(st) # MAKE THIS NONE (MAYBE)
            self.finger_table.append({'start':st, 'interval':[st, end-1], 'node':node})
        self.predecessor=None
        self.finger_table[0]['node']=self

    def find_successor(self, id):
        pred_n = self.find_predecessor(id)
        return pred_n.successor()

    def successor(self):
        return self.finger_table[0]['node']

    def find_predecessor(self, id):
        n_pred = self
        # print(set(range(0, n_pred.successor.node_num)))
        #print(n_pred.node_num+1,n_pred.successor.node_num)
        total_set= set(range(0, 2**self.m))
        find_set=set()

        start = (n_pred.node_num+1)%(2**self.m)
        end = (n_pred.successor().node_num+1)%(2**self.m)
        if start < end:
            find_set = set(range(start, end))
        elif start==end:
            return self
        else:
            find_set = total_set - set(range(end, start))
        while id not in find_set:
            #print("n_pred", n_pred.node_num, n_pred.successor().node_num, self.node_num, id)
            n_pred = n_pred.closest_preceding_finger(id)
            #print("n_pred", n_pred.node_num, n_pred.successor().node_num, self.node_num, id)

            start = (n_pred.node_num+1)%(2**self.m)
            end = (n_pred.successor().node_num+1)%(2**self.m)

            if start < end:
                find_set = set(range(start, end))
            elif start == end:
                return n_pred
            else:
                find_set = total_set - set(range(end, start))

        return n_pred

    def closest_preceding_finger(self, id):
        #print(id)
        for i in range(self.m-1, -1, -1):
            if self.finger_table[i]['node'] == None:
                continue
            if((self.node_num+1)%(2**self.m)<=id):
                if self.finger_table[i]['node'].node_num in set(range((self.node_num+1)%(2**self.m),id)):
                    return self.finger_table[i]['node']
            else:
                if self.finger_table[i]['node'].node_num in set(range((self.node_num+1)%(2**self.m),2**self.m)) or self.finger_table[i]['node'].node_num in set(range(0,id)):
                    #print('closet',self.node_num, i, self.finger_table[i]['node'].node_num)
                    return self.finger_table[i]['node']

        return self

    # def join(self, node_dash):
    #     if node_dash:
    #         self.init_finger_table(node_dash)
    #         self.update_others()
    #     else:
    #         for i in range(self.m):
    #             self.finger_table[i]['node']=self
    #         self.predecessor=self

    def join(self, node_dash):
        self.predecessor = None
        if(node_dash):
            self.finger_table[0]['node'] = node_dash.find_successor(self.node_num)
        else:
            self.finger_table[0]['node'] = self

    def init_finger_table(self, node_dash):
        #print(node_dash.node_num)
        self.finger_table[0]['node']=node_dash.find_successor(self.finger_table[0]['start'])
        #print(self.finger_table[0]['start'], self.finger_table[0]['node'].node_num)
        self.predecessor=self.successor().predecessor
        self.successor().predecessor=self
        self.predecessor.finger_table[0]['node'] = self ###Adding now check later   
        for i in range(0, self.m-1):
            total_set= set(range(0, 2**self.m))
            find_set=set()
            if self.node_num <= self.finger_table[i]['node'].node_num:
                find_set=set(range(self.node_num, self.finger_table[i]['node'].node_num))
            else:
                find_set = total_set - set(range(self.finger_table[i]['node'].node_num, self.node_num))

            if self.finger_table[i+1]['start'] in find_set: ## -1 in end
                self.finger_table[i+1]['node']=self.finger_table[i]['node']
            else:
                self.finger_table[i+1]['node']=node_dash.find_successor(self.finger_table[i+1]['start'])
            #print(self.finger_table[i+1]['start'], self.finger_table[i+1]['node'].node_num)

    def update_others(self):
        for i in range(self.m):
            p=self.find_predecessor((self.node_num - 2**i)%(2**self.m))
            if(p.successor().node_num == (self.node_num - 2**i)%(2**self.m)):     #Adding this condition check later
                p = p.successor()
            p.update_finger_table(self, i) ## CHECK THIS, MAYBE i instead of i+1.

    def update_finger_table(self, s, i):
        if self==s:
            return
        #print('printing', s.node_num, self.node_num, i, self.finger_table[i]['node'].node_num )
        start = self.node_num
        end = self.finger_table[i]['node'].node_num
        total_set = set(range(0, 2**self.m))
        if start<=end:
            if start==end or s.node_num in set(range(self.node_num, self.finger_table[i]['node'].node_num)):
                self.finger_table[i]['node']=s
                p=self.predecessor
                p.update_finger_table(s, i)
        else:
            if s.node_num in (total_set - set(range(end, start))):
                self.finger_table[i]['node']=s
                p=self.predecessor
                p.update_finger_table(s, i)

    def show(self):
        if(self.predecessor):
            self.message = "Node "+str(self.node_num)+": suc " + str(self.successor().node_num) + ", pre " + str(self.predecessor.node_num) + ": finger " ##self.finger_table[0]['node'].node_num
        else:
            self.message = "Node "+str(self.node_num)+": suc " + str(self.successor().node_num) + " pre None: finger " ##self.finger_table[0]['node'].node_num
        for i in range(self.m):
            if(self.finger_table[i]['node']!=None):
                self.message = self.message + str(self.finger_table[i]['node'].node_num) + ","
        print(self.message[:-1])

    def stabilize(self):
        x = self.successor().predecessor
        if(x == None):
            self.successor().notify(self)
            return

        if((self.node_num+1)%2**self.m<=(self.successor().node_num)%2**self.m):
            if x.node_num in set(range((self.node_num+1)%(2**self.m),(self.successor().node_num)%(2**self.m))):
                self.finger_table[0]['node']=x
        else:
            if x.node_num in set(range((self.node_num+1)%(2**self.m),2**self.m)) or x.node_num in set(range(0,(self.successor().node_num)%(2**self.m))):
                self.finger_table[0]['node']=x

        self.successor().notify(self)

    def notify(self, node_dash):
        #print('came here for', self.node_num, node_dash.node_num)
        if(self.predecessor==None):
            self.predecessor = node_dash
        else:
            if(self.node_num==self.predecessor.node_num):
                #print('came here for', self.node_num, node_dash.node_num)
                self.predecessor = node_dash
            elif((self.predecessor.node_num+1)%(2**self.m)<=self.node_num):
                #print('came here for', self.node_num, node_dash.node_num)
                if(node_dash.node_num in set(range((self.predecessor.node_num+1)%(2**self.m),self.node_num))):
                    #print('came here for', self.node_num, node_dash.node_num)
                    self.predecessor = node_dash
            else:
                if(node_dash.node_num in set(range((self.predecessor.node_num+1)%(2**self.m),2**self.m)) or node_dash.node_num in set(range(0,self.node_num))):
                    self.predecessor = node_dash

    def fix_fingers(self):
        #i = random.randint(0,self.m-1)
        #print("fix_finger", i, self.finger_table[i]['node'].node_num)
        for i in range(self.m):
            self.finger_table[i]['node'] = self.find_successor(self.finger_table[i]['start'])

    def drop(self):
        self.successor().predecessor = self.predecessor
        self.predecessor.finger_table[0]['node'] = self.successor()
        #self.successor().fix_fingers()

class ChordRing:

    def __init__(self, m):
        self.ring_size=m
        self.node_list = {};


    def add_node(self, node_num):
        node=ChordNode(node_num, self.ring_size)
        self.node_list[node_num] = node
        print("Added node", node_num)

    def join(self, from_node, to_node):
        if(to_node==-1):
            self.node_list[from_node].join(None)
        else:
            self.node_list[from_node].join(self.node_list[to_node])

    def show(self, node_num):
        self.node_list[node_num].show()

    def fix(self, node_num):
        self.node_list[node_num].fix_fingers()

    def stab(self, node_num):
        self.node_list[node_num].stabilize()

    def drop(self, node_num):
        self.node_list[node_num].drop()
        del self.node_list[node_num]
        print("Dropped node", node_num)

parser = argparse.ArgumentParser()
parser.add_argument('-i', metavar='i', type=str, help='file name for batch mode')
parser.add_argument('m', metavar='N', type=int, nargs='+',help='2^m nodes in the ring')
args = vars(parser.parse_args())

filename = args['i']
m = args['m'][0]

ring = ChordRing(int(m))

def process_command(command):
	tokens = command.split(" ")
	if tokens[0]=="end":
		if len(tokens) > 1:
			print("SYNTAX ERROR: list expects 0 parameters not",len(tokens)-1)
			return
		sys.exit(0)
	elif tokens[0]=="list":
		if len(tokens) > 1:
			print("SYNTAX ERROR: list expects 0 parameters not",len(tokens)-1)
			return
		print("Nodes:"+str(sorted(ring.node_list.keys()))[1:-1])
	elif tokens[0]=="add":
		if len(tokens) > 2:
			print("SYNTAX ERROR: list expects 1 parameter not",len(tokens)-1)
			return
		try:
			node = int(tokens[1])
		except:
			print("ERROR: invalid integer "+tokens[1])
			return
		if node not in range(0, 2**m):
			print("ERROR: node id must be in [0,"+str(2**m)+")")
			return
		if node in ring.node_list:
			print("ERROR: Node", node,"exists")
			return
		ring.add_node(node)
	elif tokens[0]=="join":
		if len(tokens) != 3:
			print("SYNTAX ERROR: list expects 2 parameters not",len(tokens)-1)
			return
		try:
			int(tokens[1])
		except:
			print("ERROR: invalid integer "+tokens[1])
			return
		try:
			int(tokens[2])
		except:
			print("ERROR: invalid integer "+tokens[2])
			return
		if int(tokens[1]) not in range(0, 2**m):
			print("ERROR: node id must be in [0,"+str(2**m)+")")
			return
		if int(tokens[2]) not in range(0, 2**m):
			print("ERROR: node id must be in [0,"+str(2**m)+")")
			return
		if int(tokens[2]) not in ring.node_list:
			print("ERROR: Node", int(tokens[2]),"does not exist")
			return
		ring.join(int(tokens[1]), int(tokens[2]))
	elif tokens[0]=="drop":
		if len(tokens) > 2:
			print("SYNTAX ERROR: list expects 1 parameters not",len(tokens)-1)
			return
		try:
			node=int(tokens[1])
		except:
			print("ERROR: invalid integer "+tokens[1])
			return
		if node not in range(0, 2**m):
			print("ERROR: node id must be in [0,"+str(2**m)+")")
			return
		if node not in ring.node_list:
			print("ERROR: Node", node,"does not exist")
			return
		ring.drop(node)
	elif tokens[0]=="fix":
		if len(tokens) > 2:
			print("SYNTAX ERROR: list expects 1 parameters not",len(tokens)-1)
			return
		try:
			node=int(tokens[1])
		except:
			print("ERROR: invalid integer "+tokens[1])
			return
		if node not in range(0, 2**m):
			print("ERROR: node id must be in [0,"+str(2**m)+")")
			return
		if node not in ring.node_list:
			print("ERROR: Node", node,"does not exist")
			return
		ring.fix(node)
	elif tokens[0]=="stab":
		if len(tokens) > 2:
			print("SYNTAX ERROR: list expects 1 parameters not",len(tokens)-1)
			return
		try:
			node=int(tokens[1])
		except:
			print("ERROR: invalid integer "+tokens[1])
			return
		if node not in range(0, 2**m):
			print("ERROR: node id must be in [0,"+str(2**m)+")")
			return
		if node not in ring.node_list:
			print("ERROR: Node", node,"does not exist")
			return
		ring.stab(node)
	elif tokens[0]=="show":
		if len(tokens) > 2:
			print("SYNTAX ERROR: list expects 1 parameters not",len(tokens)-1)
			return
		try:
			node=int(tokens[1])
		except:
			print("ERROR: invalid integer "+tokens[1])
			return
		if node not in range(0, 2**m):
			print("ERROR: node id must be in [0,"+str(2**m)+")")
			return
		if node not in ring.node_list:
			print("ERROR: Node", node,"does not exist")
			return
		ring.show(node)
	else:
		print("ERROR: Enter a valid chord function")
		return


if filename == None:
    ## RUN IN INTERACTIVE MODE
    while True:
        command = input()
        process_command(command)
else:
    with open(filename, 'r') as f:
        commands = f.readlines()
        for command in commands:
            process_command(command[:-1])




