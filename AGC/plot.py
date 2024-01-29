import os, sys
import matplotlib.pyplot as plt
import numpy as np
psse_location       = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(psse_location)
os .environ['path'] = os.environ['path'] + ';' + psse_location
import psspy
import dyntools

# ----------------------open file-------------------------
casefile = os.path.join(r"C:\Users\user\Desktop\AGC\117P-11007.sav")
dyrfile  = os.path.join(r"C:\Users\user\Desktop\AGC\P-11007-AGC.dyr")
outfile  = os.path.join(r"C:\Program Files\114\outfile\agc.out")
progfile = os.path.join(r"C:\Program Files\114\txtfile\agc.txt")

# ----------------------newton & convert-------------------------
psspy.psseinit(0)
psspy.progress_output(2,progfile)
psspy.case(casefile)
_i   = psspy. getdefaultint()
_f   = psspy.getdefaultreal()
_s   = psspy.getdefaultchar()
step = 0.0008333
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

# ----------------------run dyrnamic simulation-------------------------
psspy.strt(0,outfile)
psspy.run (0, 1, 100, 100, 0)
psspy.dist_machine_trip(107, r"1")
psspy.run (0, 10, 100, 100, 0)

# ----------------------plot-------------------------
chnfobj = dyntools.CHNF(outfile)
title, chanid, chandata = chnfobj.get_data()
freq    = [60*(1+f) for f in chandata[1]]
plt.figure (1)
plt.plot   (chandata['time'], freq, label='freq')
plt.legend ()
plt.xlim   ([0,chandata['time'][-1]])
plt.xlabel ('time')
plt.savefig('after.png')
plt.show   ()