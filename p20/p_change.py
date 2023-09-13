import os,sys
PSSE_LOCATION = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import matplotlib.pyplot as plt
import numpy as np
import psspy
import dyntools
casefile1 = os.path.join(r"C:\Program Files\114\savfile\p20\p20.sav")        # after
casefile2 = os.path.join(r"C:\Program Files\114\savfile\117p.sav")       # before
dyrfile   = os.path.join(r"C:\Program Files\114\savfile\p20\p20.dyr")
outfile  = os.path.join(r"C:\Program Files\114\outfile\p20.out")
progfile = os.path.join(r"C:\Program Files\114\txtfile\p20.txt")

# -----------------------------------------------------------------------
psspy.psseinit(0)
psspy.progress_output(2,progfile)
psspy.case(casefile1)
psspy.fnsl([1,0,0,0,1,1,-1,0])
psspy.fnsl([0,0,0,0,0,0,0,0])

Sid  = -1  
Flag = 1
ierr, Nmach1  = psspy.amachcount(Sid, Flag)            
ierr, iMbus1 = psspy.amachint(Sid, Flag, 'NUMBER') 
ierr, cMids1 = psspy.amachchar(Sid, Flag, 'ID')  
ierr, machloadp1 = psspy.amachreal(Sid, Flag,string='PGEN')
psspy.dyre_new([1,1,1,1],dyrfile)
iMbus1     = iMbus1    [0]
cMids1     = cMids1    [0]
machloadp1 = machloadp1[0]
pga = 0
pwa = 0
ppvv = 0
pwindd = 0
for iM in range(0,Nmach1): 
    ibus=iMbus1[iM]
    genId=cMids1[iM]
    machloadpp=machloadp1[iM]
    ierr, genMdl = psspy.mdlnam(ibus, genId, 'GEN')
    # print(ierr)
    if genMdl != None :        # is Gen
        pga += machloadpp
    else:
        pwa += machloadpp
        ierr, WgenMdl = psspy.windmnam(ibus, genId, 'WGEN')
        WgenMdl = WgenMdl.strip()
        if WgenMdl == "PVGU1"            :
            ppvv += machloadpp
        else:
            pwindd += machloadpp

psspy.case(casefile2)
psspy.fnsl([1,0,0,0,1,1,-1,0])
psspy.fnsl([0,0,0,0,0,0,0,0])
ierr, Nmach2  = psspy.amachcount(Sid, Flag)
ierr, iMbus2 = psspy.amachint(Sid, Flag, 'NUMBER') 
ierr, cMids2 = psspy.amachchar(Sid, Flag, 'ID')  
ierr, machloadp2 = psspy.amachreal(Sid, Flag,string='PGEN')
iMbus2     = iMbus2    [0]
cMids2     = cMids2    [0]
machloadp2 = machloadp2[0]
pgb = 0
pwb = 0
for iM in range(0,Nmach2): 
    ibus=iMbus2[iM]
    genId=cMids2[iM]
    machloadpp=machloadp2[iM]
    ierr, genMdl = psspy.mdlnam(ibus, genId, 'GEN')
    if genMdl != None :        # is Gen
        pgb += machloadpp
    else:
        pwb += machloadpp

inct = 0
dect = 0
print("---------------ON or OFF---------------")
for i in range(len(iMbus1)):
    if(iMbus1[i] not in iMbus2):
        print("increase  bus:" + str(iMbus1[i]) + "  pgen:" + str(machloadp1[i]))
        inct += machloadp1[i]
for i in range(len(iMbus2)):
    if(iMbus2[i] not in iMbus1):
        print("decrease  bus:" + str(iMbus2[i]) + "  pgen:" + str(machloadp2[i]))
        dect += machloadp2[i]
print("---------------INC or DEC---------------")
ppv = 0
pwind = 0
pi = 0
pj = 0
pk = 0
for i in range(len(iMbus1)):
    for j in range(len(iMbus2)):
        if(iMbus1[i] == iMbus2[j] and machloadp1[i] > machloadp2[j] and cMids1[i] == cMids2[j]):
            print("increase bus:   " + str(iMbus1[i]) + "  pgen:" + str(machloadp1[i]-machloadp2[j]))
            inct += (machloadp1[i]-machloadp2[j])
            ierr, WgenMdl = psspy.windmnam(iMbus1[i], cMids1[i], 'WGEN')
            ierr, area = psspy.busint(iMbus1[i], 'AREA')
            WgenMdl = WgenMdl.strip()
            if WgenMdl == "PVGU1"            :        # is Gen
                ppv += (machloadp1[i]-machloadp2[j])
            else:
                pwind += (machloadp1[i]-machloadp2[j])
            if area == 1:
                pi += (machloadp1[i]-machloadp2[j])
            elif area == 2:
                pj += (machloadp1[i]-machloadp2[j])
            elif area == 3:
                pk += (machloadp1[i]-machloadp2[j])
            else:
                print("eeeeeeeeeeee")
        elif(iMbus1[i] == iMbus2[j] and machloadp1[i] < machloadp2[j] and cMids1[i] == cMids2[j]):
            print("decrease bus:   " + str(iMbus1[i]) + "  pgen:" + str(machloadp2[j]-machloadp1[i]))
            dect += (machloadp2[j]-machloadp1[i])
print("total increase: " + str(inct))
print("total decrease: " + str(dect) + "\n")
print("after gen:      " + str(pga))
print("after PV:       " + str(pwa))
print("after total:    " + str(pwa+pga))
print("after percent:  " + str(100*pwa/(pwa+pga)) + "\n")
print("before gen:     " + str(pgb))
print("before PV:      " + str(pwb))
print("before total:   " + str(pwb+pgb))
print("before percent: " + str(100*pwb/(pwb+pgb)))

print(ppvv)
print(pwindd)
