import os,sys
PSSE_LOCATION=r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import psspy
SAV=r"C:\Program Files\114\savfile\114p.sav"  
psspy.psseinit(buses=15000)
psspy.case(SAV)

ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
ierr=psspy.fnsl([0,0,0,1,0,0,0,0])

SNP=r"C:\Program Files\114\snpfile\114p.snp"
psspy.rstr(SNP) 
# ------- SUBSYSTEM DEFINITION AND MACHINE SELECTION CRITERIA ---------
#         (a basic example shown here)
Sid=-1      # All machines
Flag=1      # Only in-service machines at in-service plants
ierr, Nmach=psspy.amachcount(Sid, Flag)                 # get no of machines in the subsystem
ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER')       # get machine bus numbers
ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')          # get machine IDs
ierr, machloads = psspy.amachreal(Sid, Flag,string='MBASE')
ierr, machloadp = psspy.amachreal(Sid, Flag,string='PGEN')
ierr, machloadpmax = psspy.amachreal(Sid, Flag,string='PMAX')
iMbus=iMbus[0]
cMids=cMids[0]
machloads=machloads[0]
machloadp=machloadp[0]
machloadpmax=machloadpmax[0]
Hgsys=0 
Htsys=0
HS=0  #all inertia*S
Sg=0  #all Gen S
St=0  #all  Gen+WGen S
Rg=0  #Gen R
Rt=0  #Gen+WGen R
Rgov=0

for iM in range(0,Nmach):   # iterate through the list of machines
    ibus=iMbus[iM]
    genId=cMids[iM]
    machloadss=machloads[iM]
    machloadpp=machloadp[iM]
    machloadpmaxx=machloadpmax[iM]
    ierr,busN=psspy.notona(ibus)
    iH=0        # resetting the intertia value index   
    ierr, icon0 = psspy.mdlind(ibus, genId, 'GEN', 'CON')   # get initial CON address (index) 
    ierr, TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')        # get generator model name
    if TgenMdl == None : #not Gen, is WGen
        H=0  
        St += machloadss
        Rt +=(machloadpmaxx-machloadpp)    
    else :  #Gen
#   Find absolute index iH in CONS array using relative CON index in the generator model and
#   previously found starting CON index of the generator model
#  (here shown only for the three most common models)
        TgenMdl=TgenMdl.strip()     # remove blanks                    
        if TgenMdl=='GENCLS': iH=icon0                         
        if (TgenMdl=='GENSAL')|(TgenMdl=='GENSAE'): iH=icon0+3    
        if (TgenMdl=='GENROU')|(TgenMdl=='GENROE'): iH=icon0+4 
#   Get value from CONS array corresponding to the generator inertia                          
        ierr,H=psspy.dsrval('CON', iH)
        HS += H*machloadss
        Sg += machloadss
        Rg+=(machloadpmaxx-machloadpp)
        ierr, govMdl = psspy.mdlnam(ibus, genId, 'GOV')
        if govMdl == None : continue
        else : Rgov+=(machloadpmaxx-machloadpp)
Hgsys=HS/Sg
St=St+Sg
Htsys=HS/St    
Rt=Rt+Rg
fout=open(r"C:\Program Files\114\txtfile\inertia_value.txt",'w')
fout.write('MODEL: Load flow:     %s\n       Dynamic model: %s\n\n' % (SAV,SNP))
fout.write('-----------------------------------------------------------------------\n')
fout.write ("Gen_Inertia:   %10.3f\n" % (Hgsys))
fout.write ("Total_Inertia: %10.3f\n" % (Htsys))
fout.write ("Gen_S(Mbase):  %10.3f\n" % (Sg))
fout.write ("Total_S(Mbase):%10.3f\n" % (St))
fout.write ("Gen_R:         %10.3f\n" % (Rg))
fout.write ("Total_R:       %10.3f\n" % (Rt))
fout.write ("Gov_R:         %10.3f\n" % (Rgov))
fout.close()
def Gen_Inertia() :  
    return Hgsys
def Total_Inertia() : 
    return Htsys
def Gen_S() :
    return Sg
def Total_S() :
    return St
def Gen_R() :
    return Rg
def Total_R() : 
    return Rt
def Gov_R() :
    return Rgov