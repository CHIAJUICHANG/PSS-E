import os,sys
PSSE_LOCATION = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import matplotlib.pyplot as plt
import numpy as np
import psspy
import dyntools
casefile = os.path.join(r"C:\Program Files\114\savfile\p20.sav")
dyrfile  = os.path.join(r"C:\Program Files\114\savfile\p20.dyr")
outfile  = os.path.join(r"C:\Program Files\114\outfile\p20.out")
progfile = os.path.join(r"C:\Program Files\114\txtfile\p20.txt")

accel = 0.15 
step = 0.0005
psspy.psseinit(0)
_i=psspy.getdefaultint();_f=psspy.getdefaultreal();_s=psspy.getdefaultchar()
psspy.progress_output(2,progfile)
psspy.case(casefile)

psspy.fnsl([1,0,0,0,1,1,-1,0])
psspy.fnsl([0,0,0,0,0,0,0,0])
# ierr = psspy.machine_data_2(iMbus, cMids, [_i, _i, _i, _i, _i, _i],[pminval, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                        
psspy.cong(0)
psspy.conl(0,1,1,[0,0],[0.0,0.0,0.0,0.0])
psspy.conl(0,1,2,[0,0],[0.0,0.0,0.0,0.0])
psspy.conl(0,1,3,[0,0],[0.0,0.0,0.0,0.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.dyre_new([1,1,1,1],dyrfile)
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[accel,_f,step,_f,_f,_f,_f,_f])
psspy.set_netfrq(1)
psspy.bus_frequency_channel([1,1900])

# dynamic
psspy.strt(0,outfile)
ierr = psspy.okstrt()
print(ierr)
# ierr = 1
if ierr == 0:
    psspy.run(0, 1, 100, 100, 0)
    psspy.dist_machine_trip(107,r"1")
    psspy.run(0, 5, 100, 100, 0)
    accel = 0.05
    step = 0.0003
    psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[accel,_f,step,_f,_f,_f,_f,_f])
    psspy.run(0, 10, 100, 100, 0)
    chnfobj = dyntools.CHNF(outfile)
    title, chanid, chandata = chnfobj.get_data()
    freq = [60*(1+f) for f in chandata[1]]
    plt.figure(1)
    plt.plot(chandata['time'], freq, label='freq')
    plt.legend()
    plt.xlim([0,chandata['time'][-1]])
    plt.xlabel('time')
    plt.savefig('p20_final_3.png')
    plt.show()

    # psspy.case(r"C:\Program Files\114\savfile\p201.sav")
    # psspy.fnsl([1,0,0,0,1,1,-1,0])
    # psspy.fnsl([0,0,0,0,0,0,0,0])
    # psspy.save(r"C:\Program Files\114\savfile\p202.sav")
    # psspy.case(casefile)
    # psspy.fnsl([1,0,0,0,1,1,-1,0])
    # psspy.fnsl([0,0,0,0,0,0,0,0])
    # psspy.save(casefile)
    # psspy.save(r"C:\Program Files\114\savfile\p201.sav")
    # psspy.save(r"C:\Program Files\114\savfile\p20_final.sav")
else:
    psspy.case(r"C:\Program Files\114\savfile\p201.sav")
    psspy.save(casefile)
    # psspy.case(casefile)
    # psspy.fnsl([1,0,0,0,1,1,-1,0])
    # psspy.fnsl([0,0,0,0,0,0,0,0])                        
    # psspy.cong(0)
    # psspy.conl(0,1,1,[0,0],[0.0,0.0,0.0,0.0])
    # psspy.conl(0,1,2,[0,0],[0.0,0.0,0.0,0.0])
    # psspy.conl(0,1,3,[0,0],[0.0,0.0,0.0,0.0])
    # psspy.ordr(0)
    # psspy.fact()
    # psspy.tysl(0)
    # psspy.dyre_new([1,1,1,1],dyrfile)
    # psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[accel,_f,step,_f,_f,_f,_f,_f])
    # psspy.set_netfrq(1)
    # psspy.bus_frequency_channel([1,1900])
    # psspy.strt(0,outfile)
    # ierr = psspy.okstrt()
    # print(ierr)
