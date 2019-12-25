from tkinter import *
from tkinter import messagebox 
import math
import random
import copy
from Graph import *
from Vec import *

WIDTH = 800
HEIGHT = 1000
ITERATIONS = 10
RADIUS = 20

class GUI:
    def __init__(self,root,nodes, graph):
        self.canvas = Canvas(
            root, width=WIDTH, height=HEIGHT, background="White"
        )
        
        
        #root.overrideredirect(True)
        self.textbox_pth = Entry(root, width = 50)
        self.textbox_graph = Text(root, bg='#FFFFE0', width='90', height='20')
        self.textbox_outs = Text(root, bg='White',width='90', height='20')
        self.textbox_file = Entry(root, width = 50)
        self.button_read = Button(root, text= "Read", command=self.read_file)
        self.button_write = Button(root, text= "Write", command=self.write_file)
        self.button_draw = Button(root, text = "Draw", command=self.draw)
        self.create_path = Button(root, text = "Path",command=self.create_path)
        self.info = Button(root, text = "Info",command="self.info")
        
        #self.canvas.pack()
        #self.button.pack()
        self.graph = graph
        self.nodes = nodes
        self.job = None

    def read_file(self):
        try:
            f = open(self.textbox_file.get(),'r')
            self.textbox_graph.delete(0.0, END)
            self.textbox_graph.insert(0.0,f.read())

            self.graph = Graph()
            self.graph.read(self.textbox_file.get())
            self.nodes = self.graph.nodes
            f.close()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
        
    
    def write_file(self):
        try:
            f = open(self.textbox_file.get(),'w')
            f.writelines(self.textbox_graph.get(0.0,END))
            f.close()
            self.read_file()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
    
    def create_path(self):
        nodes = self.textbox_pth.get().split(",")
        ls = self.graph.hamilton_checks(nodes)
        n=0
        self.textbox_outs.delete("0.0", END)
        for i in ls:
            self.textbox_outs.insert(str(n)+".0",i[0]+"|"+i[1]+"\n")
            n+=1

        
        

    def draw_node(self, x, y, text, r=RADIUS):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="MistyRose")
        self.canvas.create_text(x, y, text=text)

    def draw_graph(self):
        for n in self.nodes:
            self.draw_node(n.vec.x, n.vec.y, n.label)

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
        #circle_layout(self.nodes)
        self.animate()

    def animate(self):
        self.canvas.delete("all")
        for t in range(ITERATIONS):
            force_layout(self.nodes)
        self.draw_graph()
        self.job = root.after(10, self.animate)




def random_layout(nodes):
    for n in nodes:
        n.vec.x = random.randint(RADIUS * 4, WIDTH - RADIUS * 4 - 1)
        n.vec.y = random.randint(RADIUS * 4, HEIGHT - RADIUS * 4 - 1)

def circle_layout(nodes):
    x = 300
    y = 400
    r = 20 + len(nodes)*5
    am = (len(nodes))/2
    c_p = math.pi/2
    for n in nodes:
        n.vec.y = math.sin(c_p)*r+y
        n.vec.x = math.cos(c_p)*r+x
        c_p+=math.pi/am




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
    frc = force_vec.mag()
    #if frc == 0: frc = 0.1
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
g.read("graph.txt")
g.nodes
z = open("traverselits.txt","w")
z.close()


root = Tk();
root.geometry('1000x1000')

w = GUI(root, g.nodes, g)


w.canvas.place(x=0,y=0)
w.button_draw.place(relx=0.0, rely=0.0)
w.textbox_outs.place(relx=0.8, rely=0.0)

w.textbox_pth.place(relx=0.8,rely=0.57)
w.create_path.place(relx=0.8,rely=0.59)

w.textbox_graph.place(relx=0.8,rely=0.7)#
w.textbox_file.place(relx=0.8,rely=0.65)
w.button_read.place(relx=0.8,rely=0.675)#
w.button_write.place(relx=0.9,rely=0.675)#

w.info.place(relx=0.9,rely=0.59)

root.mainloop()