import os,sys
PSSE_LOCATION = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import matplotlib.pyplot as plt
import numpy as np
import psspy
import dyntools

casefile=os.path.join(r"C:\Program Files\114\savfile\drive-download-20220113T053726Z-001\117P-11007.sav")
dyrfile=os.path.join(r"C:\Program Files\114\savfile\drive-download-20220113T053726Z-001\P-11007.dyr")
outfile=os.path.join(r"C:\Program Files\114\outfile\114p.odut")
progfile=os.path.join(r"C:\Program Files\114\txtfile\114p.txt")

step=0.0008333; t0=1.0-step; #chan_i=3;
psspy.psseinit(0);
_i=psspy.getdefaultint();_f=psspy.getdefaultreal();_s=psspy.getdefaultchar();
psspy.progress_output(2,progfile)
psspy.case(casefile)
psspy.fnsl([0,0,0,1,1,0,0,0])
psspy.cong(0)
psspy.conl(0,1,1,[0,0],[0.0,0.0,0.0,0.0])
psspy.conl(0,1,2,[0,0],[0.0,0.0,0.0,0.0])
psspy.conl(0,1,3,[0,0],[0.0,0.0,0.0,0.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.dyre_new([1,1,1,1],dyrfile)

# psspy.dyda(0,1,[2,1,0],0,dyrefile_new)
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[_f,_f,step,_f,_f,_f,_f,_f])
psspy.set_netfrq(1)


psspy.machine_array_channel([1,2,9119],'1')    #pelec
psspy.machine_array_channel([2,6,9119],'1')    #pmach

# dynamic
psspy.strt(0,outfile)
psspy.run(0, 1,100,100,0)
psspy.dist_machine_trip(107,r"1")
psspy.run(0, 10,100,100,0)

chnfobj = dyntools.CHNF(outfile)
title, chanid, chandata = chnfobj.get_data()

ierr, mbase = psspy.macdat(9119, '1', 'MBASE')
pelec = [100*pe for pe in chandata[1]]
pmach = [mbase*pm for pm in chandata[2]]             

plt.plot(chandata['time'],pmach,label='pmach')
plt.plot(chandata['time'],pelec,label='pelec')
plt.legend()
plt.xlim([0,chandata['time'][-1]])
plt.xlabel('time')
plt.savefig('9119.png')
plt.show()