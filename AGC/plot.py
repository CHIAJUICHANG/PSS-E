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
NDM = 8
for i in range(0, NDM*3+2):
    psspy.var_channel([5+i,1886+i])     # L+3 

# ----------------------run dyrnamic simulation-------------------------
psspy.strt(0,outfile)
psspy.run (0,  1, 100000, 100, 0)
psspy.dist_machine_trip(107, r"1")
psspy.run (0, 30, 100000, 100, 0)

# ----------------------plot-------------------------
chnfobj = dyntools.CHNF(outfile)
title, chanid, chandata = chnfobj.get_data()
freq    = [60*(1+f) for f in chandata[1]]
plt.figure (1)
plt.plot   (chandata['time'], freq, label='freq')
plt.legend ()
plt.xlim   ([0,chandata['time'][-1]])
plt.xlabel ('time')
# plt.savefig('after1590.png')
# print(chandata[5])
for i in range(2, 4):
    freq    = [f for f in chandata[i]]
    plt.figure (i)
    plt.plot   (chandata['time'], freq, label='freq')
    plt.legend ()
    plt.xlim   ([0,chandata['time'][-1]])
    plt.xlabel ('time')
    # plt.savefig('ACE1590.png')
    # if i == 5:
    #     plt.savefig('reg.png')
for i in range(0, NDM):
    freq1    = [f for f in chandata[3*(i+1)+1]]
    freq2    = [f for f in chandata[3*(i+1)+2]]
    freq3    = [f for f in chandata[3*(i+1)+3]]
    plt.figure (i)
    plt.plot   (chandata['time'], freq, label='freq')
    plt.legend ()
    plt.xlim   ([0,chandata['time'][-1]])
    plt.xlabel ('time')
    # plt.savefig('ACE1590.png')
    # if i == 5:
    #     plt.savefig('reg.png')
for i in range(28, 30):
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