import os,sys
PSSE_LOCATION = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import matplotlib.pyplot as plt
import numpy as np
import psspy
import dyntools
casefile=os.path.join(r"C:\Program Files\114\savfile\original file\117P-11007.sav")
dyrfile=os.path.join(r"C:\Program Files\114\savfile\original file\P-11007.dyr")
outfile=os.path.join(r"C:\Program Files\114\outfile\inertia_res_Gen.out")
progfile=os.path.join(r"C:\Program Files\114\txtfile\inertia_res_Gen.txt")

accel = 0.001
step = 0.000008; t0=1.0-step; #chan_i=3;
psspy.psseinit(0)
_i=psspy.getdefaultint();_f=psspy.getdefaultreal();_s=psspy.getdefaultchar();
psspy.progress_output(2,progfile)
psspy.case(casefile)

psspy.fnsl([0,0,0,1,1,0,0,0])
psspy.fnsl([0,0,0,1,1,0,0,0])
Sid=-1 
Flag=3 
ierr, Nmach = psspy.amachcount(Sid, Flag)     
ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER') 
ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')
ierr, mbase = psspy.amachreal(Sid, Flag,string='MBASE')
iMbus=iMbus[0]
cMids=cMids[0]
mbase=mbase[0]

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

for iM in range(0,Nmach):
    ibus = iMbus[iM]
    genId = cMids[iM]
    ierr, genMdl = psspy.mdlnam(ibus, genId, 'GEN')  
    if genMdl == None : continue       #not Gen, is WGen
    # else :  #Gen
    psspy.machine_array_channel([2*iM+1,2,ibus],genId)    #pelec
    psspy.machine_array_channel([2*iM+2,6,ibus],genId)    #pmach
psspy.bus_frequency_channel([2*Nmach+1,9119])

# dynamic
psspy.strt(0,outfile)
psspy.run(0, 1,5000,5000,0)
psspy.dist_machine_trip(107,r"1")
psspy.run(0, 13,5000,5000,0)

chnfobj = dyntools.CHNF(outfile)
title, chanid, chandata = chnfobj.get_data()
inertia_res = [0]*(len(chandata[1]))

for iM in range(0,Nmach):
    ibus = iMbus[iM]
    genId = cMids[iM]
    mbasee = mbase[iM]
    ierr, TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')
    if TgenMdl == None : continue   #not Gen, is WGen
    pelec = [100*pe for pe in chandata[2*iM+1]]           
    pmach = [mbasee*pm for pm in chandata[2*iM+2]]
    for i in range(0,len(pelec)):
        inertia_res[i] += (pelec[i] - pmach[i])
freq = [60*(1+f) for f in chandata[2*Nmach+1]]

plt.figure(1)
plt.plot(chandata['time'],freq,label='freq')
plt.legend()
plt.xlim([0,chandata['time'][-1]])
plt.xlabel('time')
plt.savefig('freq_res.png')
plt.figure(2)
plt.plot(chandata['time'],inertia_res,label='inertia_respose')
plt.legend()
plt.xlim([0,chandata['time'][-1]])
plt.xlabel('time')
plt.savefig('inertia_res_Gen.png')
plt.show()