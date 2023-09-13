import sys, os
PYTHONPATH = r'C:\Program Files\PTI\PSSE33\PSSBIN'
sys.path.append(PYTHONPATH)
os.environ['PATH'] += ';'+PYTHONPATH
from tkSimpleDialog import askinteger
from Tkinter import Tk
from itertools import chain
import psspy

dyrfile  = os.path.join(r"C:\Program Files\114\savfile\p20.dyr")
progfile = os.path.join(r"C:\Program Files\114\txtfile\p_seach.txt")
psspy.psseinit(0)
psspy.progress_output(2,progfile)
psspy.case(r'C:\Program Files\114\savfile\p20.sav')            # opening sav file
ierr, busnum = psspy.abusint(-1, 1, 'NUMBER')                     # only in-serve bus numbers
ierr, iarray_from = psspy.abrnint(-1, 1, 3, 3, 1, 'FROMNUMBER')   # only in-serve branch
ierr, iarray_to = psspy.abrnint(-1, 1, 3, 3, 1, 'TONUMBER')
iarray_from = iarray_from[0]
iarray_to = iarray_to[0]
busnum = busnum[0]
Sid  = -1  
Flag = 1   
ierr, Nmach=psspy.amachcount(Sid, Flag)        
ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER') 
ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')  
ierr, machloadp = psspy.amachreal(Sid, Flag,string='PGEN')
iMbus     = iMbus    [0]
cMids     = cMids    [0]
machloadp = machloadp[0]
psspy.dyre_new([1,1,1,1],dyrfile)

#output path
path = {}
for i in range(0,len(busnum)):
    ierr, rval = psspy.busdat(busnum[i], 'BASE')
    path[busnum[i]] = []
    for j in range(0,len(iarray_from)):        
        if (iarray_from[j] == busnum[i]) and (iarray_to[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_to[j], 'BASE')
            path[busnum[i]] += [iarray_to[j]]
        if (iarray_to[j] == busnum[i]) and (iarray_from[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_from[j], 'BASE')
            path[busnum[i]] += [iarray_from[j]]
    if (path[busnum[i]] == []):
        del path[busnum[i]]

root = Tk()
root.update()
stt = askinteger("Input", "Enter Starting Bus no.", initialvalue=533)
lev = askinteger("Input", "Enter Level", initialvalue=10)
list1 =[[stt]]
list_reg = []
all = []
path_found = []
alll = []
for i in range(0, lev+1):                   #len(path)
    all += list1
    genn = []
    windd = []
    print("Level " + str(i))
    for l in range(0,len(list1)):
        if list1[l][-1] in iMbus and list1[l][-1] not in alll:
            num = iMbus.index(list1[l][-1])
            ierr, genMdl = psspy.mdlnam(list1[l][-1], cMids[num], 'GEN')
            if genMdl != None :        # is Gen     
                genn += [list1[l][-1]]
            else:
                windd += [list1[l][-1]]
            alll += [list1[l][-1]] 
    print("Gen : "),
    print(genn)
    print("Wind : "),
    print(windd)
    for j in range(0,len(list1)):
        for k in range(0,len(path[list1[j][len(list1[j])-1]])):
            if (path[list1[j][len(list1[j])-1]][k] not in list1[j]) and ((list1[j]+[path[list1[j][len(list1[j])-1]][k]]) not in list_reg):            
                list_reg = list_reg+[list1[j]+[path[list1[j][len(list1[j])-1]][k]]]          
    if (list_reg == []): break
    list1 = list_reg
    list_reg = []