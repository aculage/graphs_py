
def create_adjacency_mx(raw_graph,adjacency_mx_size):
    adjacency_mx=[[0]*adjacency_mx_size for i in range(adjacency_mx_size)]
    adress_rows = raw_graph[1::2]

    for i in range(len(adress_rows)) :
        #adjacency_mx[i][i] = 1
        for j in adress_rows[i].split(',') :
            adjacency_mx[i][int(j)-1] = 1
    return(adjacency_mx)

def check_for_strongbound(adjacency_mx,adjacency_mx_size):
    for i in range(adjacency_mx_size) :
        for j in range(adjacency_mx_size) :
            if (adjacency_mx[i][j]!=adjacency_mx[j][i]) : return False
    return True

def depth_check(cur_build, adjacency_mx, adjacency_mx_size):
    for i in range(adjacency_mx_size) :
        if adjacency_mx[int(cur_build[-1])-1][i] == 1 :  
            perm_adjacency_mx = copy.deepcopy(adjacency_mx) #OHRENET` ESLI BI NE DOPER SHO TUT SSILKA VMESTO KOPII PEREDAVALAS` NA OBJEKT DROPNUL BI NAHUI ETU ZADACHU
            perm_adjacency_mx[i][int(cur_build[-1])-1] = 0
            perm_adjacency_mx[int(cur_build[-1])-1][i] = 0
            traf_cur_build = copy.deepcopy(cur_build)
            depth_check(traf_cur_build+str(i+1),perm_adjacency_mx,adjacency_mx_size)
        f = open('traverselits.txt', 'a+')
        f.writelines(cur_build+'\n')
        f.close