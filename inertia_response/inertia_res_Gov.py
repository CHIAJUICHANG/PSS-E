import os,sys
PSSE_LOCATION = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import matplotlib.pyplot as plt
import numpy as np
import psspy
import dyntools
casefile=os.path.join(r"C:\Program Files\114\savfile\original file\shunt.sav")
dyrfile=os.path.join(r"C:\Program Files\114\savfile\original file\P-11007.dyr")
outfile=os.path.join(r"C:\Program Files\114\outfile\inertia_res_Gov.out")
progfile=os.path.join(r"C:\Program Files\114\txtfile\inertia_res_Gov.txt")

step=0.0008; t0=1.0-step; accel = 1
psspy.psseinit(0)
_i=psspy.getdefaultint();_f=psspy.getdefaultreal();_s=psspy.getdefaultchar();
psspy.progress_output(2,progfile)
psspy.case(casefile)

psspy.fnsl([0,0,0,1,1,0,0,0])
Sid = -1 
Flag = 3
ierr, Nmach = psspy.amachcount(Sid, Flag)     
ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER') 
ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')
ierr, mbase = psspy.amachreal(Sid, Flag, 'MBASE')
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
    ierr, govMdl = psspy.mdlnam(ibus, genId, 'GOV') 
    if ((genMdl == None) or (govMdl == None)): continue       #not Gen, is WGen
    ierr, icon0 = psspy.mdlind(ibus, genId, 'GEN', 'CON')
    # psspy.plmod_status(ibus,genId,3,0)
    # psspy.plmod_status(ibus,genId,6,0)
    # if genMdl=='GENCLS': psspy.change_plmod_con(ibus,genId,genMdl,2,0)                          
    # if (genMdl=='GENSAL')|(genMdl=='GENSAE'): psspy.change_plmod_con(ibus,genId,genMdl,5,0)   
    # if (genMdl=='GENROU')|(genMdl=='GENROE'): psspy.change_plmod_con(ibus,genId,genMdl,6,0)
    psspy.machine_array_channel([2*iM+1,2,ibus],genId)    #pelec
    psspy.machine_array_channel([2*iM+2,6,ibus],genId)    #pmach
psspy.bus_frequency_channel([2*Nmach+1,314])

# dynamic
psspy.plmod_status(301,r"1",6,0)
psspy.plmod_status(302,r"2",6,0)
psspy.plmod_status(303,r"3",6,0)
psspy.plmod_status(304,r"1",6,0)
psspy.plmod_status(305,r"2",6,0)
psspy.plmod_status(306,r"3",6,0)
psspy.strt(0,outfile)
psspy.run(0, 1,200,200,0)
psspy.dist_machine_trip(311,r"1")
psspy.dist_machine_trip(312,r"1")
psspy.dist_machine_trip(313,r"1")
psspy.dist_machine_trip(314,r"1")
psspy.dist_machine_trip(315,r"1")
psspy.dist_machine_trip(316,r"1")
psspy.dist_machine_trip(317,r"1")
psspy.dist_machine_trip(318,r"1")
psspy.dist_machine_trip(107,r"1")
psspy.dist_machine_trip(108,r"1")
psspy.run(0, 10,200,200,0)

chnfobj = dyntools.CHNF(outfile)
title, chanid, chandata = chnfobj.get_data()
inertia_res = [0]*(len(chandata[1]))

for iM in range(0,Nmach):
    ibus = iMbus[iM]
    genId = cMids[iM]
    mbasee = mbase[iM]
    ierr, genMdl = psspy.mdlnam(ibus, genId, 'GEN')
    ierr, govMdl = psspy.mdlnam(ibus, genId, 'GOV')
    if ((genMdl == None) or (govMdl == None)) : continue   #not Gen, no gov
    pelec = [100*pe for pe in chandata[2*iM+1]]           
    pmach = [mbasee*pm for pm in chandata[2*iM+2]]
    for i in range(0,len(pelec)):
        inertia_res[i] += (pelec[i] - pmach[i])
freq = [60*(1+f) for f in chandata[2*Nmach+1]]
for i in range(len(freq)/2,len(freq)):
    if((freq[i] > 59.75) or (freq[i] < 59.65)):
        print(chandata['time'][i])

print("inertia_respone : " + str(inertia_res[len(pelec)-1]))
print("frequency : " + str(freq[len(freq)-1]))

plt.figure(1)
plt.plot(chandata['time'],freq,label='frequency')
plt.legend()
plt.xlim([0,chandata['time'][-1]])
plt.xlabel('time')
plt.savefig('freq_res_change.png')
plt.figure(2)
plt.plot(chandata['time'],inertia_res,label='inertia_respose')
plt.legend()
plt.xlim([0,chandata['time'][-1]])
plt.xlabel('time')
plt.savefig('inertia_res_Gov_change.png')
plt.show()