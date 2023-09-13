import os,sys
PSSE_LOCATION=r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import psspy
SAV=r"C:\Program Files\114\savfile\114p.sav"   
psspy.psseinit(0)
psspy.case(SAV)
ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
DYR=r"C:\Program Files\114\savfile\drive-download-20220113T053726Z-001\P-11007.dyr"
psspy.dyre_new([1,1,1,1],DYR) 

# ---------------------------------------------------------------
Sid=-1  
Flag=1 
ierr, Nmach = psspy.amachcount(Sid, Flag)          
ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER') 
ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')  
ierr, machloadp = psspy.amachreal(Sid, Flag,string='PGEN')
ierr, machloadq = psspy.amachreal(Sid, Flag,string='QGEN')
ierr, machloads = psspy.amachreal(Sid, Flag,string='MBASE')

iMbus=iMbus[0]
cMids=cMids[0]
machloadp=machloadp[0]
machloadq=machloadq[0]
machloads=machloads[0]

fout=open(r"C:\Program Files\114\txtfile\Gen_inertia_list.txt",'w')
savFn, snpFn = psspy.sfiles()
fout.write('MODEL: Load flow:     %s\n       Dynamic model: %s\n\n' % (savFn,snpFn))
fout.write('   BUS    NAME              GEN   MODEL   H(sec)   MBASE      PGEN     QGEN   GOVERNOR\n----------------------------------------------------------------------------------------\n')

for iM in range(0,Nmach): 
    ibus=iMbus[iM]
    genId=cMids[iM]
    machloadpp=machloadp[iM]
    machloadqq=machloadq[iM]
    machloadss=machloads[iM]
    ierr,busN=psspy.notona(ibus)
    iH=0 
    ierr, icon0 = psspy.mdlind(ibus, genId, 'GEN', 'CON') 
    ierr, genMdl = psspy.mdlnam(ibus, genId, 'GEN')
    if genMdl == None : continue #not Gen, is WGen
    ierr, govMdl = psspy.mdlnam(ibus, genId, 'GOV')
    if govMdl == None: govMdl="None"
    govMdl=govMdl.strip()
    genMdl=genMdl.strip()                    
    if genMdl=='GENCLS': iH=icon0                           
    if (genMdl=='GENSAL')|(genMdl=='GENSAE'): iH=icon0+3    
    if (genMdl=='GENROU')|(genMdl=='GENROE'): iH=icon0+4
    ierr,H=psspy.dsrval('CON', iH)
    fout.write ('%6d  %12s   %2s  %6s  %6.3f  %8.3f  %7.3f  %7.3f  %7s\n' % (ibus,busN,genId,genMdl,H,machloadss,machloadpp,machloadqq,govMdl))
fout.close()