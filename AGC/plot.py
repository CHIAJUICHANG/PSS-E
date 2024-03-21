import os, sys
import matplotlib.pyplot as plt
import numpy as np
psse_location       = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(psse_location)
os .environ['path'] = os.environ['path'] + ';' + psse_location
import psspy
import dyntools

# ----------------------open file-------------------------
casefile = os.path.join(r"D:\github\PSS-E\AGC\117P-11007.sav")
dyrfile  = os.path.join(r"D:\github\PSS-E\AGC\P-11007-AGC8.dyr")
outfile  = os.path.join(r"C:\Program Files\114\outfile\agc.out")
progfile = os.path.join(r"C:\Program Files\114\txtfile\agc.txt")

# ----------------------newton & convert-------------------------
psspy.psseinit(0)
psspy.progress_output(2,progfile)
psspy.case(casefile)
_i   = psspy.getdefaultint()
_f   = psspy.getdefaultreal()
_s   = psspy.getdefaultchar()
# step = 0.0008333
step = 0.001
psspy.fnsl([1,0,0,0,1,1,-1,0])
psspy.fnsl([0,0,0,0,0,0,0,0])
psspy.cong(0)
psspy.conl(0,1,1,[0,0],[0.0,0.0,0.0,0.0])
psspy.conl(0,1,2,[0,0],[0.0,0.0,0.0,0.0])
psspy.conl(0,1,3,[0,0],[0.0,0.0,0.0,0.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.dyre_new([1,1,1,1],dyrfile)
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[_f,_f,step,_f,_f,_f,_f,_f])
psspy.set_netfrq(1)
psspy.bus_frequency_channel([1,704])
psspy.var_channel([2,1883]) 
psspy.var_channel([3,1884]) 
psspy.var_channel([4,1885])
NDM   = 8
bus   = [  704, 831, 832,   861,   862,   863,   864,   865]
id    = [  "4", "1", "1",   "1",   "1",   "1",   "1",   "1"]
pmax  = [240.5, 105, 105, 24.05, 24.05, 24.05, 24.05, 24.05]
for i in range(0, NDM*4+2):
    psspy.var_channel([5+i,1886+i])     # L+3 

# ----------------------run dyrnamic simulation-------------------------
psspy.strt(0,outfile)
psspy.run (0,  1, 1000, 1000, 0)
psspy.dist_machine_trip(107, r"1")  # 423
# psspy.dist_machine_trip(321, r"1")  # 270
# psspy.dist_machine_trip(301, r"1")  # 150
psspy.run (0, 45, 1000, 1000, 0)

# ----------------------plot-------------------------
chnfobj = dyntools.CHNF(outfile)
title, chanid, chandata = chnfobj.get_data()
freq    = [60*(1+f) for f in chandata[1]]
avg = 0
steady_s = 0
plt.figure (1)
plt.plot   (chandata['time'], freq, label='freq')
plt.legend ()
plt.xlim   ([0,chandata['time'][-1]])
plt.xlabel ('time')
for i in range(0, len(chandata['time'])):
    if chandata['time'][i] > 20: 
        avg      += freq[i]
        steady_s += 1 
avg = avg/steady_s
avg_arr = [avg for i in range(0, len(chandata['time']))]
plt.plot   (chandata['time'], avg_arr, label=str(avg_arr[0]))
print(avg_arr[0])

# plt.savefig('after1.png')
# # print(chandata[5])
for i in range(2, 5):
    if i == 3:
        continue
    freq    = [f for f in chandata[i]]
    plt.figure (i)
    if i == 2:
        plt.plot   (chandata['time'], freq, label='ACE')
    if i == 4:
        plt.plot   (chandata['time'], freq, label='AACt')    
    plt.legend ()
    plt.xlim   ([0,chandata['time'][-1]])
    plt.xlabel ('time')

#     # plt.savefig('ACE1590.png')
#     # if i == 5:
#     #     plt.savefig('reg.png')
# for i in range(5, 9):
#     if i == 5:
#         freq1    = [f for f in chandata[4*(i-4)+2]]
#         freq2    = [f for f in chandata[4*(i-4)+3]]
#         freq3    = [f for f in chandata[4*(i-4)+4]]
#         freq4    = [f for f in chandata[4*(i-4)+5]]
#     plt.figure (i)
#     if i == 5:
#         plt.plot   (chandata['time'], freq1, label='P(I)')
#     if i == 6:    
#         plt.plot   (chandata['time'], freq2, label='Preg(I)')
#     if i == 7:
#         plt.plot   (chandata['time'], freq3, label='GREF(I)')
#     if i == 8:
#         plt.plot   (chandata['time'], freq4, label='AAC(I)')
#     plt.legend ()
#     plt.xlim   ([0,chandata['time'][-1]])
#     plt.xlabel ('time')
# for i in range(5, NDM+5):
#     for j in range(0, 4):
#         freq    = [f for f in chandata[4*(i-4)+j+1]]
#         if j == 0:
#             plt.figure (4*(i-4)+j+1)
#             plt.plot   (chandata['time'], freq, label='P(I)')
#             pmaxx      = [pmax[i-5] for k in range(0, len(chandata['time']))]
#             plt.plot   (chandata['time'], pmaxx, label='Pmax')
        #     print('P('+str(i-4)+')'+str(freq[len(freq)-1]))
        # if j == 1:    
        #     plt.plot   (chandata['time'], freq, label='Preg(I)')
        # if j == 2:
        #     plt.plot   (chandata['time'], freq, label='GREF(I)')
        # if j == 3:
        #     plt.plot   (chandata['time'], freq, label='AAC(I)')
        #     print('AAC('+str(i-4)+')'+str(freq[len(freq)-1]))
        # plt.legend ()
        # plt.xlim   ([0,chandata['time'][-1]])
        # plt.xlabel ('time')

    # plt.savefig('ACE1590.png')
    # if i == 5:
    #     plt.savefig('reg.png')
    # if i == 5:
    #     AACT = freq3
    # else:
    #     for j in range(0, len(freq3)):
    #         AACT[j] += freq3[j]
    # if  i == NDM+5-1:
    #     plt.figure (i+1)
    #     plt.plot   (chandata['time'], AACT, label='AACT(I)')
    #     plt.legend ()
    #     plt.xlim   ([0,chandata['time'][-1]])
    #     plt.xlabel ('time')
for i in range(38, 39):
    freq    = [f for f in chandata[i]]
    plt.figure (i)
    plt.plot   (chandata['time'], freq, label='freq')
    plt.legend ()
    plt.xlim   ([0,chandata['time'][-1]])
    plt.xlabel ('time')
    # plt.savefig('ACE1590.png')
    # if i == 5:
    #     plt.savefig('reg.png')
plt.show   ()