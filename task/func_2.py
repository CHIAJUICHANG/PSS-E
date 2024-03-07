import sys, os
PYTHONPATH = r'C:\Program Files\PTI\PSSE33\PSSBIN'
sys.path.append(PYTHONPATH) 
os.environ['PATH'] += ';'+PYTHONPATH
import psspy

def main(path, stt, end):
    list1 =[[stt]]
    list_reg = []
    all = []
    path_found = []
    for i in range(0,10):                   #len(path)
        all += list1
        for j in range(0,len(list1)):
            for k in range(0,len(path[list1[j][len(list1[j])-1]])):
                if (path[list1[j][len(list1[j])-1]][k] == end):
                    path_found += [list1[j]+[path[list1[j][len(list1[j])-1]][k]]]
                    break
                if (path[list1[j][len(list1[j])-1]][k] not in list1[j]) and ((list1[j]+[path[list1[j][len(list1[j])-1]][k]]) not in list_reg):            
                    list_reg = list_reg+[list1[j]+[path[list1[j][len(list1[j])-1]][k]]]
        if (list_reg == []): break
        list1 = list_reg
        list_reg = []
    return path_found

# def voltagecheck(path, lev):
#     change = 0
#     unable = 0
#     final = []
#     for i in range(0,len(path)):
#         for j in range(0,len(path[i])):
#             ierr, rval = psspy.busdat(ab[i][j], 'BASE')         # return real bus values (bus base voltage, kV)
#             if (rval <= lev):
#                 unable = 1 
#                 change = 1
#                 break
#         if(unable == 0):
#             final += [ab[i]]
#         unable = 0
#     return final, change