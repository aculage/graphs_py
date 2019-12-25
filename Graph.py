import copy
import re
from Vec import *

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

    def deg(self):
        return len(self.targets)

    


class Graph:
    def __init__(self):
        self.nodes = []
        self.adjacency_mx = []

    def read(self, file):
        f = open(file, 'r')
        node_info = []
        for line in f:
            if ':' in line:
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

                        
            self.adjacency_mx.append(ad_mx_row)

    def depth_check(self, cur_build, adjacency_mx, adjacency_mx_size, weight):
        flag = True
        for i in range(adjacency_mx_size) :
          
            if adjacency_mx[int(cur_build[-1])-1][i] > 0 :
                weight+=adjacency_mx[int(cur_build[-1])-1][i]
                flag = False  
                perm_adjacency_mx = copy.deepcopy(adjacency_mx) #OHRENET` ESLI BI NE DOPER SHO TUT SSILKA VMESTO KOPII PEREDAVALAS` NA OBJEKT DROPNUL BI NAHUI ETU ZADACHU
                perm_adjacency_mx[i][int(cur_build[-1])-1] = 0
                perm_adjacency_mx[int(cur_build[-1])-1][i] = 0
                traf_cur_build = copy.deepcopy(cur_build)
                traf_weight = copy.deepcopy(weight)
                self.depth_check(traf_cur_build+" "+str(i+1),perm_adjacency_mx,adjacency_mx_size,weight)
        if flag:
            f = open('traverselits.txt', 'a+')
            f.writelines(cur_build+"w"+str(weight)+'\n')
            f.close()



    def hamilton_checks(self,nodes):
        self.depth_check(nodes[0],self.adjacency_mx,len(self.adjacency_mx),0)
        f_ = open('traverselits.txt','r')
        brdrs=""
        paths= []
        for lines in f_:
            paths.append(lines.strip('\n'))
        brdrs = nodes[0]
        brdrs_ = nodes[-1]
            
    
        nodes.remove(brdrs)
        nodes.remove(brdrs_)
        for nd_id in nodes:
            
            
            comp = re.compile(".*"+brdrs+"+.*"+nd_id+"+.*"+brdrs_+"+.*w")
            temp_paths=[]
            for pt in paths:
                if re.match(comp, pt):
                    f_p=pt.split("w")[0]
                    comp_=re.compile(brdrs+"+.*"+brdrs_)
                    r=re.match(comp_,f_p)
                    if r is not None:
                        temp_paths.append(r.group(0)+"w"+pt.split("w")[1])
        
            paths = copy.deepcopy(temp_paths)
        
        if len(nodes) ==0:
            comp = re.compile(".*"+brdrs+"+.*"+brdrs_+"+.*w")
            temp_paths=[]
            for pt in paths:
                if re.match(comp, pt):
                    f_p=pt.split("w")[0]
                    comp_=re.compile(brdrs+"+.*"+brdrs_)
                    r=re.match(comp_,f_p)
                    if r is not None:
                        temp_paths.append(r.group(0)+"w"+pt.split("w")[1])
            paths = copy.deepcopy(temp_paths)

        p_=[]
        for p in paths:
            p_.append([p.split("w")[0],p.split("w")[1]])

        p_=sorted(p_, key=lambda x: int(x[1]))
        return p_