import tkinter as tk
import math
import random

WIDTH = 600
HEIGHT = 800
ITERATIONS = 10
RADIUS = 20

class GUI:
    def __init__(self,root,nodes):
        self.canvas = tk.Canvas(
            root, width=WIDTH, height=HEIGHT, background="White"
        )
        self.button = tk.Button(root, text = "Draw", command=self.draw)
        self.canvas.pack()
        self.button.pack()
        self.nodes = nodes
        self.job = None

    def draw_node(self, x, y, text, r=RADIUS):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="MistyRose")
        self.canvas.create_text(x, y, text=text)

    def draw_graph(self):
        for s in self.nodes:
            for t in s.targets:
                self.canvas.create_line(s.vec.x, s.vec.y, t[1].vec.x, t[1].vec.y)
        for n in self.nodes:
            self.draw_node(n.vec.x, n.vec.y, n.label)

    def draw(self):
        self.canvas.delete("all")
        if self.job:
            root.after_cancel(self.job)
        random_layout(self.nodes)
        self.animate()

    def animate(self):
        self.canvas.delete("all")
        for t in range(ITERATIONS):
            force_layout(self.nodes)
        self.draw_graph()
        self.job = root.after(5, self.animate)

def random_layout(nodes):
    for n in nodes:
        n.vec.x = random.randint(RADIUS * 4, WIDTH - RADIUS * 4 - 1)
        n.vec.y = random.randint(RADIUS * 4, HEIGHT - RADIUS * 4 - 1)

class Node:
    def __init__(self, label):
        self.label = label
        self.targets = []
        self.vec = Vec(0, 0)

    def edge(self, weights, *nodes ):
        for n in nodes:
            self.targets.append((weights,n))
            
            n.targets.append((weights,self))

        return self

    


class Graph:
    def __init__(self):
        self.nodes = []
        self.adjacency_mx = []

    def read(self, file):
        f = open(file, 'r')
        node_info = []
        for line in f:
            line = line.strip('\n')
            lspl = line.split(':')
            inline = (lspl[0], lspl[1].split(','))
            node_info.append(inline)
            self.node(lspl[0])

            
        for nd in self.nodes:
            #pick a node
            for ninf in node_info:
                #scroll through the info
                if nd.label == ninf[0]:
                    #found info about the node
                    #process targets correctly
                    trgts = []
                    for trgt in ninf[1]:
                        trgts.append(trgt.split('*'))
                    for nd_edge in trgts:
                        #scroll through the targets
                        for nd_tar in self.nodes:
                            #find instances of targets
                            if nd_tar.label == nd_edge[0]:
                                nd.edge(nd_edge[1],nd_tar) 
        self.adjacency_mx_gen()

            

    def node(self, label):
        self.nodes.append(Node(label))
        return self.nodes[-1]
    
    def adjacency_mx_gen(self):
        for nd in self.nodes: #main traverse
            ad_mx_row = []
            for nd_ in self.nodes: #for each node go through nodes again
                flag = True
                for trgt in nd.targets: #for each 2-nd layer node find out if it`s a target
                    if nd_.label == trgt[1].label:
                        ad_mx_row.append(int(trgt[0]))
                        flag = False
                if flag :
                    ad_mx_row.append(0)

                        
            self.adjacency_mx.append([ad_mx_row])




class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y)

    def __mul__(self, n):
        return Vec(self.x * n, self.y * n)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def unit(self):
        m = self.mag()
        return Vec(self.x / m, self.y / m) if m else Vec(0, 0)


C1, C2, C3, C4 = 2, 100, 20000, 0.001


def spring(v1, v2):
    
    force_vec = (v1-v2)
    #dist = force_vec.mag()
    force_vec = Vec (force_vec.x, force_vec.y) 
    #node has mass
    #eval
    if (force_vec.mag()>=100) :
        return(Vec(-force_vec.x, -force_vec.y))
    else : return(force_vec)


def ball(v1, v2):
    force_vec = (v1-v2)

    return(force_vec*(400/force_vec.mag()-1))


def force_layout(nodes):
    forces = {}
    for n in nodes:
        forces[n] = Vec(0, 0)
        for t in n.targets:
            forces[n] += spring(n.vec,t[1].vec)
        for nod in nodes:

            #if nod is not n.targets[1]:
                if nod is not n:
                    forces[n] += ball(n.vec,nod.vec)
                    
    for n in nodes:
        #if (forces[n])
        n.vec += forces[n] * C4



#main code

g = Graph()
g.read("graph-3.txt")
g.nodes
root = tk.Tk();

w = GUI(root, g.nodes)

root.mainloop()