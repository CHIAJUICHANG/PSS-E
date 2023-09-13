import os,sys
sys.path.append(r"C:\Program Files\PTI\PSSE33\PSSBIN")

import dyntools
import matplotlib.pyplot as plt
import numpy as np
import psspy
import redirect
j=2;
x=[25,50,100,-100,-50]
a=int(sys.argv[1])
casefile=os.path.join('..\\system', '10411_P_OK_01.sav')
dyrfile=os.path.join('..\system', '1041104_Peak_v32.dyr')
outfile=os.path.join('..\\out', 'freq'+str(a)+'1.out')
progfile=os.path.join('..\\prog', 'prog'+str(j)+'.txt')
dyrefile_1=os.path.join('..\system', '1041104_Peak_v32_1.dyr')
step=0.0008333; t0=1.0-step; chan_i=1;
redirect.psse2py(); psspy.psseinit(0);
_i=psspy.getdefaultint();_f=psspy.getdefaultreal();_s=psspy.getdefaultchar();
psspy.progress_output(2,progfile)

psspy.case(casefile)
psspy.dyre_new([1,1,1,1],dyrfile)
## gen Damping remove
# Sid=-1; Flag=1;
# ierr, Nmach=psspy.amachcount(Sid, Flag)           # get no of machines in the subsystem
# ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER') # get machine bus numbers
# ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')    # get machine IDs
# for iM in range(0,Nmach):  # iterate through the list of machines
    # ibus=iMbus[0][iM]; genId=cMids[0][iM]; iD=0;
    # ierr, icon0 = psspy.mdlind(ibus, genId, 'GEN', 'CON') # get initial CON address (index)
    # ierr, genMdl = psspy.mdlnam(ibus, genId, 'GEN') # get generator model name
    # if (icon0==0): print('*'+genMd1)
    # if (genMdl): genMdl=genMdl.strip() # remove blanks                
    # if (genMdl=='GENSAL')|(genMdl=='GENSAE'): iD=icon0+4    
    # if (genMdl=='GENROU')|(genMdl=='GENROE'): iD=icon0+5
    # if (iD != 0): psspy.change_con(iD, 0)

# psspy.dyda(0,1,[2,1,0],0,dyrefile_1)
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[_f,_f, step,_f,_f,_f,_f,_f])
psspy.dyre_new([1,1,1,1],dyrefile_1)
psspy.set_netfrq(1)
# channel
#ierr, buses = psspy.abuscount(-1,1);
#ierr, ibus = psspy.abusint(-1,1,'NUMBER');
buses = [301,1500]
for i in buses:
 psspy.bus_frequency_channel([chan_i,i]); chan_i=chan_i+1;

# bus=[301,'1',101,'1',701,'1',711,'1',831,'1']
# for i in range(len(bus)/2):
    # ibus=bus[2*i];genId=str(bus[2*i+1]);
    # psspy.machine_array_channel([chan_i,2,ibus],genId); chan_i=chan_i+1; # elec
    # psspy.machine_array_channel([chan_i,6,ibus],genId); chan_i=chan_i+1; # pm
    # psspy.machine_array_channel([chan_i,7,ibus],genId); chan_i=chan_i+1; # speed

# power flow
psspy.fnsl([0,0,0,1,1,0,99,0])
psspy.cong(0)
psspy.conl(0,1,1,[0,0],[0.0,0.0,0.0,0.0])
psspy.conl(0,1,2,[0,0],[0.0,0.0,0.0,0.0])
psspy.conl(0,1,3,[0,0],[0.0,0.0,0.0,0.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
 
# dynamic
ierr=psspy.strt(0,outfile)
psspy.run(0, 0.1-step,10,10,0)
psspy.run(0, 1.0-step+1,10,10,0)
if a==1: psspy.shunt_data(3222,'1',1,REALAR1=x[j]); # 1 3
if a==3: psspy.shunt_data(9617,'1',1,REALAR1=x[j]); # 3 20
if a==2: psspy.shunt_data(625,'1',1,REALAR1=x[j]); # 2 102
psspy.run(0, 1.0-step+1+0.05,10,10,0)
psspy.run(0, 10,10,10,0)