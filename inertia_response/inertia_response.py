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
psspy.psseinit(0)
_i=psspy.getdefaultint();_f=psspy.getdefaultreal();_s=psspy.getdefaultchar();
psspy.progress_output(2,progfile)
psspy.case(casefile)

psspy.fnsl([0,0,0,1,1,0,0,0])
Sid=-1 
Flag=1 
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

psspy.machine_array_channel([1,2,9119],r"1")    #pelec
psspy.machine_array_channel([2,6,9119],r"1")    #pmach

for iM in range(0,Nmach):
    ibus = iMbus[iM]
    genId = cMids[iM]  
    TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')
    if TgenMdl == None : #not Gen, is WGen
        psspy.machine_array_channel([2*iM+1,2,ibus],genId)    #pelec
        psspy.machine_array_channel([2*iM+2,6,ibus],genId)    #pmach
    else :  #Gen
        psspy.machine_array_channel([2*iM+1,2,ibus],genId)    #pelec
        psspy.machine_array_channel([2*iM+2,6,ibus],genId)    #pmach

# dynamic
psspy.strt(0,outfile)
psspy.run(0, 1,100,100,0)
psspy.dist_machine_trip(107,r"1")
psspy.run(0, 12,100,100,0)

chnfobj = dyntools.CHNF(outfile)
title, chanid, chandata = chnfobj.get_data()
inertia_res_t = 0
inertia_re2 = 0
for iM in range(0,Nmach):
    ibus = iMbus[iM]
    genId = cMids[iM]
    mbasee = mbase[iM]
    pelec = [100*pe for pe in chandata[2*iM+1]]           
    pmach = [mbasee*pm for pm in chandata[2*iM+2]]
    for i in range(0,len(pelec)):
        inertia_res1 = pelec[i] - pmach[i]
        if((inertia_re2 == inertia_res1) and  (inertia_res1 != 0)):   
            inertia_res_t += inertia_res1
            break
        else : inertia_re2 = inertia_res1      
# plt.plot(chandata['time'],pmach,label='pmach')
plt.plot(chandata['time'],pelec,label='pelec')
plt.legend()
plt.xlim([0,chandata['time'][-1]])
plt.xlabel('time')
# plt.savefig('9119.png')
plt.show()
# print(inertia_res_t)