import sys
import os
sys.path.append('C:\Program Files (x86)\PTI\PSSE34\PSSBIN')
sys.path.append('C:\Program Files (x86)\PTI\PSSE34\PSSPY27')
sys.path.append('C:\Users\Administrator\Documents\\alice\lib')

import psse34
import psspy
import SP, H_est, reserve, Q
from file_all import *
import offpeak_patch

# file
file_sav = os.path.join('..\\system_patch', '117L-11106_pmax.sav')
file_dyr = os.path.join('..\\system', 'L-11007.dyr')
file_sav_patch = os.path.join('..\\system_patch', '117L-11106-11p.sav')

# initialize
_i = psspy.getdefaultint();_f = psspy.getdefaultreal();_s = psspy.getdefaultchar()
psspy.psseinit(0)
psspy.lines_per_page_one_device(1, 60)
psspy.report_output(2, file_report, [0, 0])
psspy.progress_output(2, file_progress, [0, 0])

# read
psspy.case(file_sav)
psspy.dyre_new([1, 1, 1, 1], file_dyr, file_conec,file_conet,file_compile)
psspy.addmodellibrary(file_dll)
SP.subsystem()

# machine status (ESS)
psspy.machine_chng_2(9419,r"""1""",intgar1=0)
psspy.machine_chng_2(9119,r"""1""",intgar1=0)

# 1: add wind
i=110003
psspy.machine_data_2(i,'2',[_i,_i,_i,_i,_i,1],
                [2.09,-5.686,8.167,-5.686,19,0,19,0,0.6025,0,0,1,1,1,1,1,0.9])
psspy.seq_machine_data_4(i,'2',_i,
                        [0,0.6025,0,0.6025,0,0.6025,0.6025,0.6025,0,0,0])
psspy.add_wind_model(i,'2',1,'WT4G2',0,[],[],9,
[0.0100,0.0100,0.1500,0.5000,1.2000,1.1600,1.4000,28.0000,0.0200])
psspy.add_wind_model(i,'2',2,'WT4E2',4,[i,0,1,0],["","","",""],34,
[0.0000,15.0000,2.0000,0.0800,0.0100,0.0000,0.0800,1.0000,-1.2000,
1.1000,0.0000,0.5000,-0.5000,0.0500,0.0100,0.8750,1.1250,55.0000,
0.0500,0.0500,1.1150,1.2500,1.0850,0.0200,0.8750,0.0500,0.0000,
2.0000,1.0000,1.0000,1.0000,1.0000,1.1000,0.1415])
psspy.fnsl([0,0,0,1,1,0,99,0]);psspy.fnsl([0,0,0,1,1,0,99,0])

# 2: close all PV wind tune to 11% offpeak
Sid, flag = -1, 1 # all area in-service unit only
ierr, Nmach = psspy.amachcount(Sid,flag)
ierr, nbus = psspy.amachint(Sid,flag,'NUMBER')
ierr, nid = psspy.amachchar(Sid,flag,'ID')
ierr, iswind = psspy.amachint(Sid, flag, 'WMOD')
for i in range(Nmach):
    ibus, cbus, iswinsbus=nbus[0][i],nid[0][i],iswind[0][i]
    if (iswinsbus != 0):
        ierr, genMdl = psspy.windmnam(ibus,cbus, 'WGEN')
        if (genMdl): genMdl=genMdl.strip()
        if (genMdl=='PVGU1'):
            psspy.machine_chng_2(ibus, cbus, intgar1=0)
        else:
            ierr, S = psspy.macdat(ibus, cbus, 'MBASE')
            psspy.machine_chng_2(ibus, cbus, realar1=S*0.11)
# shunt no active power
Sid, flag = 0, 1 # north
ierr, Nshnt = psspy.afxshuntcount(Sid,flag)
ierr, nbus = psspy.afxshuntint(Sid,flag,'NUMBER')
ierr, nid = psspy.afxshuntchar(Sid,flag,'ID')
for i in range(Nshnt):
    ibus, cbus=nbus[0][i],nid[0][i];psspy.shunt_chng(ibus, cbus, _i,[0,_f])
Sid, flag = 4, 1 # east
ierr, Nshnt = psspy.afxshuntcount(Sid,flag)
ierr, nbus = psspy.afxshuntint(Sid,flag,'NUMBER')
ierr, nid = psspy.afxshuntchar(Sid,flag,'ID')
for i in range(Nshnt):
    ibus, cbus=nbus[0][i],nid[0][i];psspy.shunt_chng(ibus, cbus, _i,[0,_f])
psspy.shunt_chng(2650, '1', _i,[-500,_f]);psspy.shunt_chng(2850, '2', _i,[-20,_f])
# open generator
bus = [ [9348, 1, 10],[9349, 1, 10],[9350, 1, 100]]# South
for i in range(len(bus)):
    ibus, cbus = bus[i][0], str(bus[i][1]); Qgen = bus[i][2]
    psspy.machine_chng_2(ibus, cbus,intgar1=1, realar2 = Qgen)
psspy.fnsl([0,0,0,1,1,0,99,0]);psspy.fnsl([0,0,0,1,1,0,99,0])

# 3: open generator
bus = [ [1062,1],# South
        [625, 1],[626, 2],[627, 'S'],]# Central
for i in range(len(bus)):
    ibus, cbus = bus[i][0], str(bus[i][1])
    psspy.machine_chng_2(ibus, cbus,intgar1=1)
Sid, flag = 1, 1 # central
ierr, Nshnt = psspy.afxshuntcount(Sid,flag)
ierr, nbus = psspy.afxshuntint(Sid,flag,'NUMBER')
ierr, nid = psspy.afxshuntchar(Sid,flag,'ID')
for i in range(Nshnt):
    ibus, cbus=nbus[0][i],nid[0][i];psspy.shunt_chng(ibus, cbus, _i,[0,_f])
psspy.shunt_chng(2650, '1', _i,[-200,_f])
psspy.fnsl([0,0,0,1,1,0,99,0]);psspy.fnsl([0,0,0,1,1,0,99,0])


# 4: close generator
bus = [ [304,1],[306,3],[322,1],[326,1]]# North
for i in range(len(bus)):
    ibus, cbus = bus[i][0], str(bus[i][1]);
    psspy.machine_chng_2(ibus, cbus,intgar1=0)
# tune generation
bus = [[1131,1],[1132,1],[1141,1],[1142,1]]# South
for i in range(len(bus)):
    ibus, cbus = bus[i][0], str(bus[i][1]);ierr, Pmax = psspy.macdat(ibus, cbus, 'PMAX')
    psspy.machine_chng_2(ibus, cbus,intgar1=1,realar1=Pmax)
Sid, flag = 2, 1 # South
ierr, Nshnt = psspy.afxshuntcount(Sid,flag)
ierr, nbus = psspy.afxshuntint(Sid,flag,'NUMBER')
ierr, nid = psspy.afxshuntchar(Sid,flag,'ID')
for i in range(Nshnt):
    ibus, cbus=nbus[0][i],nid[0][i];psspy.shunt_chng(ibus, cbus, _i,[0,_f])
psspy.fnsl([0,0,0,1,1,0,99,0]);psspy.fnsl([0,0,0,1,1,0,99,0])

psspy.save(file_sav_patch)

sumS, sumP = SP.conSP(Sid=-1);print('Conventional:',sumS, sumP,round(sumP/sumS*100,2))
sumS, sumP = SP.resSP(isPV=0, Sid=-1);print('WIND:',sumS, sumP,round(sumP/sumS*100,2))
sumS, sumPT = SP.SP(Sid=-1);print('Total:',sumS, sumPT)

# sumS, sumP = SP.SP(Sid=0);print('North:',sumS, sumP, round(sumP/sumPT,3))
# sumS, sumP = SP.SP(Sid=1);print('Central:',sumS, sumP, round(sumP/sumPT,3))
# sumS, sumP = SP.SP(Sid=2);print('South:',sumS, sumP, round(sumP/sumPT,3))
# sumS, sumP = SP.SP(Sid=3);print('East:',sumS, sumP)

sumS, sumP = SP.resSP(isPV=0, Sid=0);print('North WIND:',sumS, sumP)
sumS, sumP = SP.resSP(isPV=0, Sid=1);print('Central WIND:',sumS, sumP)
sumS, sumP = SP.resSP(isPV=0, Sid=2);print('South WIND:',sumS, sumP)
sumS, sumP = SP.resSP(isPV=0, Sid=3);print('East WIND:',sumS, sumP)

# sumP = SP.shntP(Sid=-1);print('Shunt:', sumP)
# sumP = SP.shntP(Sid=0);print('North:', sumP)
# sumP = SP.shntP(Sid=1);print('Central:', sumP)
# sumP = SP.shntP(Sid=2);print('South:', sumP)
# sumP = SP.shntP(Sid=3);print('East:', sumP)

sumS, sumP = SP.conSP(Sid=-1);print('Conventional:',sumS, sumP)
sumS, sumP = SP.conSP(Sid=0);print('North:',sumS, sumP)
sumS, sumP = SP.conSP(Sid=1);print('Central:',sumS, sumP)
sumS, sumP = SP.conSP(Sid=2);print('South:',sumS, sumP)
sumS, sumP = SP.conSP(Sid=3);print('East:',sumS, sumP)

# H=H_est.H(Sid=-1); print('Total:', H)
# H=H_est.H(Sid=0); print('North:', H)
# H=H_est.H(Sid=1); print('Central:', H)
# H=H_est.H(Sid=2); print('South:', H)
# H=H_est.H(Sid=3); print('East:', H)

# sumQ = Q.resQ(1,-1); print('PV Q: ', sumQ)
# sumQ = Q.resQ(1, 0); print('North PV Q: ', sumQ)
# sumQ = Q.resQ(1, 1); print('Central PV Q: ', sumQ)
# sumQ = Q.resQ(1, 2); print('South PV Q: ', sumQ)
# sumQ = Q.resQ(1, 3); print('East PV Q: ', sumQ)

r, r_ = reserve.reserve(); print('reserve', r,r_)
offpeak_patch.dyr()
bus = offpeak_patch.ibusgovoff
for i in range(len(bus)):
    psspy.plmod_status(bus[i][0],str(bus[i][1]),7,0)
r, r_ = reserve.reserve(); print('reserve', r,r_)
psspy.fnsl([0,0,0,1,1,0,99,0]);psspy.fnsl([0,0,0,1,1,0,99,0])