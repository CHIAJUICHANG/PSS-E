import sys, os
PYTHONPATH = r'C:\Program Files\PTI\PSSE33\PSSBIN'
sys.path.append(PYTHONPATH)
os.environ['PATH'] += ';'+PYTHONPATH
from tkSimpleDialog import askinteger
from Tkinter import Tk
from itertools import chain
import psspy
from func_2 import *

task2 = os.path.join(r"C:\Program Files\114\txtfile\task_2\path.txt")
psspy.psseinit(0)
psspy.case(r'C:\Program Files\114\savfile\task_2.sav')            # opening sav file
ierr, busnum        = psspy.abusint(-1, 1, 'NUMBER')                     # only in-serve bus numbers
ierr, iarray_from   = psspy.abrnint(-1, 1, 3, 1, 1, 'FROMNUMBER')   # only in-serve branch
ierr, iarray_to     = psspy.abrnint(-1, 1, 3, 1, 1, 'TONUMBER')
ierr, iarray_from_2 = psspy.atrnint(-1, 1, 3, 1, 1, 'FROMNUMBER')
ierr, iarray_to_2   = psspy.atrnint(-1, 1, 3, 1, 1, 'TONUMBER')
ierr, iarray_from_3 = psspy.atr3int(-1, 1, 3, 1, 1, 'WIND1NUMBER')
ierr, iarray_to_3   = psspy.atr3int(-1, 1, 3, 1, 1, 'WIND2NUMBER')
ierr, iarray_last_3 = psspy.atr3int(-1, 1, 3, 1, 1, 'WIND3NUMBER')
iarray_from   = iarray_from[0]
iarray_to     = iarray_to[0]
iarray_from_2 = iarray_from_2[0]
iarray_to_2   = iarray_to_2[0]
iarray_from_3 = iarray_from_3[0]
iarray_to_3   = iarray_to_3[0]
iarray_last_3 = iarray_last_3[0]
busnum        = busnum[0]

root = Tk()
root.update()
stt = askinteger("Input", "Enter Starting Bus no.", initialvalue=107)
end = askinteger("Input", "Enter Ending Bus no.", initialvalue=1090)
lev = askinteger(
    "Input", "Enter voltage level in KV's you want to omit", initialvalue=1)
sys.stdout = open(task2, 'w')

#output path
path = {}
for i in range(0,len(busnum)):
    ierr, rval = psspy.busdat(busnum[i], 'BASE')
    if rval <= lev : continue
    path[busnum[i]] = []
    for j in range(0,len(iarray_from)):        
        if (iarray_from[j] == busnum[i]) and (iarray_to[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_to[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_to[j]]
        if (iarray_to[j] == busnum[i]) and (iarray_from[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_from[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_from[j]]
    for j in range(0,len(iarray_from_2)):        
        if (iarray_from_2[j] == busnum[i]) and (iarray_to_2[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_to_2[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_to_2[j]]
        if (iarray_to_2[j] == busnum[i]) and (iarray_from_2[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_from_2[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_from_2[j]]
    for j in range(0,len(iarray_from_3)):        
        if (iarray_from_3[j] == busnum[i]) and (iarray_to_3[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_to_3[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_to_3[j]]
        if (iarray_from_3[j] == busnum[i]) and (iarray_last_3[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_last_3[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_last_3[j]]
        if (iarray_to_3[j] == busnum[i]) and (iarray_from_3[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_from_3[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_from_3[j]]
        if (iarray_to_3[j] == busnum[i]) and (iarray_last_3[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_last_3[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_last_3[j]]
        if (iarray_last_3[j] == busnum[i]) and (iarray_from_3[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_from_3[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_from_3[j]]  
        if (iarray_last_3[j] == busnum[i]) and (iarray_to_3[j] not in path[busnum[i]]):
            ierr, rval = psspy.busdat(iarray_to_3[j], 'BASE')
            if rval > lev : path[busnum[i]] += [iarray_to_3[j]]      
    if (path[busnum[i]] == []):
        del path[busnum[i]]

print('We have to find path between :'+ str(stt) + ' and '+ str(end) + "\n") 
ab= []
ab = main(path, stt, end)
print('**********************************************************************\n')
print('Following paths exist between start and end bus\n')
print('**********************************************************************\n')
if(ab == []):
    print('No found any paths')
else :
    print('found !!!\n')
    print('**********************************************************************\n')
    print('Following paths exist between start and end bus after omitting buses of level : '+ str(lev) + " KV\n")
    print('**********************************************************************\n')
    for w in range(0,len(ab)):
        for l in range(0,len(ab[w])):
            if ab[w][l]
        print("path " + str(w+1) + " : " + str(ab[w]))

sys.stdout.close()
os.startfile(task2)