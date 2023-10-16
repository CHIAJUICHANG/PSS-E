import os,sys
PSSE_LOCATION = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import matplotlib.pyplot as plt
import numpy as np
import psspy
import dyntools
# a=int(sys.argv[1]) #select conver
a=1
casefile=os.path.join(r"C:\Program Files\114\savfile\drive-download-20220113T053726Z-001\117P-11007.sav")
dyrfile=os.path.join(r"C:\Program Files\114\savfile\drive-download-20220113T053726Z-001\P-11007.dyr")
# casefile=os.path.join(r"C:\Program Files\114\savfile\original file\117P-11007.sav")
# dyrfile=os.path.join(r"C:\Program Files\114\savfile\original file\P-11007.dyr")
outfile=os.path.join(r"C:\Program Files\114\outfile\114p.odut")
progfile=os.path.join(r"C:\Program Files\114\txtfile\114p.txt")

step=0.0008333; t0=1.0-step; #chan_i=3;
psspy.psseinit(0);
_i=psspy.getdefaultint();_f=psspy.getdefaultreal();_s=psspy.getdefaultchar();
psspy.progress_output(2,progfile)
psspy.case(casefile)
psspy.fnsl([0,0,0,1,1,0,0,0])
psspy.cong(0)
if a==1 :
    psspy.conl(0,1,1,[0,0],[0.0,0.0,0.0,0.0])
    psspy.conl(0,1,2,[0,0],[0.0,0.0,0.0,0.0])
    psspy.conl(0,1,3,[0,0],[0.0,0.0,0.0,0.0])
# elif a==2 :
#     psspy.conl(0,1,1,[0,0],[0.0, 100.0,0.0, 100.0])
#     psspy.conl(0,1,2,[0,0],[0.0, 100.0,0.0, 100.0])
#     psspy.conl(0,1,3,[0,0],[0.0, 100.0,0.0, 100.0])
# elif a==3 :
#     psspy.conl(0,1,1,[0,0],[0.0,0.0,0.0, 100.0])
#     psspy.conl(0,1,2,[0,0],[0.0,0.0,0.0, 100.0])
#     psspy.conl(0,1,3,[0,0],[0.0,0.0,0.0, 100.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.dyre_new([1,1,1,1],dyrfile)

# psspy.dyda(0,1,[2,1,0],0,dyrefile_new)
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[_f,_f,step,_f,_f,_f,_f,_f])
psspy.set_netfrq(1)

# for i in buses:
#     psspy.bus_frequency_channel([chan_i,i])
#     chan_i=chan_i+1
# psspy.bsys(1,0,[0.0,0.0],0,[],1,[9419],0,[],0,[])
# for i in range(29,38):
#     psspy.chsb(1,0,[-1,-1,-1,1,i,0])

psspy.state_channel([1,7127])                   #s6
psspy.var_channel([2,1906])                     #plant ref
psspy.bus_frequency_channel([3,9119])           #frequency
psspy.var_channel([4,1905])                     #frequency ref
psspy.machine_array_channel([5,2,9119],r"1")    #pelec
# psspy.state_channel([6,7125])                   #s4
# psspy.var_channel([7,1911])                     #l8

# dynamic
psspy.strt(0,outfile)
# psspy.change_wnmod_var(9119,r"1",r"REPCAU1",4, 0.01)
psspy.run(0, 1,100,100,0)
psspy.dist_machine_trip(107,r"1")
psspy.run(0, 12,100,100,0)

chnfobj = dyntools.CHNF(outfile)
title, chanid, chandata = chnfobj.get_data()
# print(title)
# print(chanid)
# print(chandata)

s6 = [f for f in chandata[1]]                
plant_ref = [f for f in chandata[2]]           
freq = [f for f in chandata[3]]               
freq_ref = [f for f in chandata[4]]  
pelec = [1.66*f for f in chandata[5]]           
# s4 = [f for f in chandata[6]]                 
# l8 = [f for f in chandata[7]]           

pdroop = []       
for i in range(len(freq)) :
    freq[i] = freq_ref[i] - freq[i]
    if freq[i] > (0.00017) : pdroop += [20*(freq[i]-(0.00017))]
    elif freq[i] < (-0.00017) : pdroop += [20*(freq[i]-(-0.00017))]
    else : pdroop += [0]
    pdroop[i] += plant_ref[i]

# print("\ns6:")
# print(s6)
# print("\nplant_ref:")
# print(plant_ref)
# print("\nfreq:")
# print(freq)
# print("\npelec:")
# print(pelec)
# print("\npdroop:")
# print(pdroop)
# print("\ns4:")
# print(s4)
# print("\nl8:")
# print(l8)

seq_01 = []
start = 18
for i in range(0, start):
    seq_01 += [0]
for i in range(start, len(pelec)):
    seq_01 += [0.00993]
# plt.plot(chandata['time'],pdroop,label='pdroop')
plt.plot(chandata['time'], seq_01, label = 'Power Command' , color = "red")
plt.plot(chandata['time'], pelec , label = 'Power Response', color = "blue")
# plt.plot(chandata['time'],s6,label='s6')
# plt.plot(chandata['time'],s4,label='s4')

plt.legend()
plt.xlim([0,chandata['time'][-1]])
plt.xlabel('time(s)')
plt.xlabel('p.u.')
plt.savefig('9119.png')
plt.show()