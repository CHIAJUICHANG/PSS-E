import os,sys
PSSE_LOCATION=r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import psspy  
psspy.psseinit(0)
ierr = psspy.progress_output(2,r"C:\Program Files\114\txtfile\inertia_function_prog.txt",0)
#----------------------------------------------------------------
def Gen_Inertia( SAV, SNP) :
    psspy.case(SAV)  
    ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
    ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
    psspy.rstr(SNP) 
    Sid=-1     
    Flag=1     
    ierr, Nmach=psspy.amachcount(Sid, Flag)                 
    ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER')       
    ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')         
    ierr, machloads = psspy.amachreal(Sid, Flag,string='MBASE')
    iMbus=iMbus[0]
    cMids=cMids[0]
    machloads=machloads[0]
    Hgsys=0 
    HS=0  
    Sg=0  
    for iM in range(0,Nmach):
        ibus=iMbus[iM]
        genId=cMids[iM]
        machloadss=machloads[iM]
        iH=0        
        ierr, icon0 = psspy.mdlind(ibus, genId, 'GEN', 'CON') 
        ierr, TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')     
        if TgenMdl == None : 
            continue
        else :
            TgenMdl=TgenMdl.strip()                    
            if TgenMdl=='GENCLS': iH=icon0                         
            if (TgenMdl=='GENSAL')|(TgenMdl=='GENSAE'): iH=icon0+3    
            if (TgenMdl=='GENROU')|(TgenMdl=='GENROE'): iH=icon0+4                          
            ierr,H=psspy.dsrval('CON', iH)
            HS += H*machloadss
            Sg += machloadss
            Hgsys=HS/Sg
    return Hgsys
#----------------------------------------------------------------
def Total_Inertia( SAV, SNP) :
    psspy.case(SAV)
    ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
    ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
    psspy.rstr(SNP) 
    Sid=-1     
    Flag=1     
    ierr, Nmach=psspy.amachcount(Sid, Flag)                 
    ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER')       
    ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')         
    ierr, machloads = psspy.amachreal(Sid, Flag,string='MBASE')
    iMbus=iMbus[0]
    cMids=cMids[0]
    machloads=machloads[0]
    Hgsys=0
    Htsys=0 
    HS=0  
    Sg=0  
    St=0
    for iM in range(0,Nmach):
        ibus=iMbus[iM]
        genId=cMids[iM]
        machloadss=machloads[iM]
        iH=0        
        ierr, icon0 = psspy.mdlind(ibus, genId, 'GEN', 'CON') 
        ierr, TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')     
        if TgenMdl == None : 
            St += machloadss
        else :
            TgenMdl=TgenMdl.strip()                    
            if TgenMdl=='GENCLS': iH=icon0                         
            if (TgenMdl=='GENSAL')|(TgenMdl=='GENSAE'): iH=icon0+3    
            if (TgenMdl=='GENROU')|(TgenMdl=='GENROE'): iH=icon0+4                          
            ierr,H=psspy.dsrval('CON', iH)
            HS += H*machloadss
            Sg += machloadss
    St += Sg
    Htsys=HS/St
    return Htsys
#----------------------------------------------------------------
def Gen_S( SAV, SNP) :
    psspy.case(SAV)
    ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
    ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
    psspy.rstr(SNP) 
    Sid=-1     
    Flag=1     
    ierr, Nmach=psspy.amachcount(Sid, Flag)                 
    ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER')       
    ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')         
    ierr, machloads = psspy.amachreal(Sid, Flag,string='MBASE')
    iMbus=iMbus[0]
    cMids=cMids[0]
    machloads=machloads[0] 
    Sg=0  
    for iM in range(0,Nmach):
        ibus=iMbus[iM]
        genId=cMids[iM]
        machloadss=machloads[iM]      
        ierr, TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')     
        if TgenMdl == None : 
            continue
        else :
            Sg += machloadss
    return Sg
#----------------------------------------------------------------
def Total_S( SAV, SNP) :
    psspy.case(SAV)
    ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
    ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
    psspy.rstr(SNP) 
    Sid=-1     
    Flag=1     
    ierr, Nmach=psspy.amachcount(Sid, Flag)                        
    ierr, machloads = psspy.amachreal(Sid, Flag,string='MBASE')
    machloads=machloads[0] 
    St=0  
    for iM in range(0,Nmach):
        machloadss=machloads[iM]         
        St += machloadss
    return St
#----------------------------------------------------------------
def Gen_R( SAV, SNP) :
    psspy.case(SAV)
    ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
    ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
    psspy.rstr(SNP) 
    Sid=-1     
    Flag=1     
    ierr, Nmach=psspy.amachcount(Sid, Flag)                 
    ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER')       
    ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')         
    ierr, machloadp = psspy.amachreal(Sid, Flag,string='PGEN')
    ierr, machloadpmax = psspy.amachreal(Sid, Flag,string='PMAX')
    iMbus=iMbus[0]
    cMids=cMids[0]
    machloadp=machloadp[0]
    machloadpmax=machloadpmax[0]
    Rg=0 
    for iM in range(0,Nmach):
        ibus=iMbus[iM]
        genId=cMids[iM]
        machloadpp=machloadp[iM]
        machloadpmaxx=machloadpmax[iM]
        ierr, TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')     
        if TgenMdl == None : 
            continue
        else :
            Rg+=(machloadpmaxx-machloadpp)
    return Rg
#----------------------------------------------------------------
def Total_R( SAV, SNP) :
    psspy.case(SAV)
    ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
    ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
    psspy.rstr(SNP) 
    Sid=-1     
    Flag=1     
    ierr, Nmach=psspy.amachcount(Sid, Flag)                 
    ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER')       
    ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')         
    ierr, machloadp = psspy.amachreal(Sid, Flag,string='PGEN')
    ierr, machloadpmax = psspy.amachreal(Sid, Flag,string='PMAX')
    iMbus=iMbus[0]
    cMids=cMids[0]
    machloadp=machloadp[0]
    machloadpmax=machloadpmax[0]
    Rg=0 
    Rt=0
    for iM in range(0,Nmach):
        ibus=iMbus[iM]
        genId=cMids[iM]
        machloadpp=machloadp[iM]
        machloadpmaxx=machloadpmax[iM]
        ierr, TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')     
        if TgenMdl == None : 
            Rt += (machloadpmaxx-machloadpp)
        else :
            Rg += (machloadpmaxx-machloadpp)
    Rt=Rt+Rg
    return Rt
#----------------------------------------------------------------
def Gov_R( SAV, SNP) :
    psspy.case(SAV)
    ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
    ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
    psspy.rstr(SNP) 
    Sid=-1     
    Flag=1     
    ierr, Nmach=psspy.amachcount(Sid, Flag)                 
    ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER')       
    ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')         
    ierr, machloadp = psspy.amachreal(Sid, Flag,string='PGEN')
    ierr, machloadpmax = psspy.amachreal(Sid, Flag,string='PMAX')
    iMbus=iMbus[0]
    cMids=cMids[0]
    machloadp=machloadp[0]
    machloadpmax=machloadpmax[0]
    Rgov=0
    for iM in range(0,Nmach):
        ibus=iMbus[iM]
        genId=cMids[iM]
        machloadpp=machloadp[iM]
        machloadpmaxx=machloadpmax[iM]
        ierr, TgenMdl = psspy.mdlnam(ibus, genId, 'GEN')     
        if TgenMdl == None : continue
        else :
            ierr, govMdl = psspy.mdlnam(ibus, genId, 'GOV')
            if govMdl == None : continue
            else : Rgov+=(machloadpmaxx-machloadpp)
    return Rgov
#----------------------------------------------------------------
def Gov_R_modify( SAV, SNP) :
    psspy.case(SAV)
    ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
    ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
    psspy.rstr(SNP) 
    Sid=-1     
    Flag=1     
    ierr, Nmach=psspy.amachcount(Sid, Flag)                 
    ierr, iMbus = psspy.amachint(Sid, Flag, 'NUMBER')       
    ierr, cMids = psspy.amachchar(Sid, Flag, 'ID')         
    ierr, machloadp = psspy.amachreal(Sid, Flag,string='PGEN')
    ierr, machloads = psspy.amachreal(Sid, Flag,string='MBASE')
    ierr, machloadpmax = psspy.amachreal(Sid, Flag,string='PMAX')
    iMbus=iMbus[0]
    cMids=cMids[0]
    machloadp=machloadp[0]
    machloads=machloads[0]
    machloadpmax=machloadpmax[0]
    fout=open(r"C:\Program Files\114\txtfile\inertia_function_R_Gov.txt",'w')
    fout.write('MODEL: Load flow:     %s\n       Dynamic model: %s\n\n' % (SAV,SNP))
    fout.write('   BUS    NAME              GOVERNOR     R     PMAX     PGEN\n-------------------------------------------------------------------------------------\n')
    At=0
    P3=0
    Pmax=0
    Gmax=0
    qnl=0
    Rgov=0
    Rt=0
    for iM in range(0,Nmach): 
        ibus=iMbus[iM]
        genId=cMids[iM]
        machloadpp=machloadp[iM]
        machloadss=machloads[iM]
        machloadpmaxx=machloadpmax[iM]
        ierr,busN=psspy.notona(ibus)
        ierr, govMdl = psspy.mdlnam(ibus, genId, 'GOV')
        if govMdl == None :
            govMdl="None"
            Pmax=machloadpmaxx
            Rgov = machloadpmaxx-machloadpp
            Rt+=Rgov
        else :
            govMdl=govMdl.strip()
            ierr, icon0 = psspy.mdlind(ibus, genId, 'GOV', 'CON')
            if govMdl == 'GAST': 
                ierr,At=psspy.dsrval('CON', icon0+4)
                Pmax=At*machloadss
                Rgov=Pmax-machloadpp
                Rt+=Rgov
            elif govMdl == 'HYGOV' : 
                ierr,At=psspy.dsrval('CON', icon0+9)
                ierr,Gmax=psspy.dsrval('CON', icon0+6)
                ierr,qnl=psspy.dsrval('CON', icon0+11)
                Pmax=At*(Gmax-qnl)*machloadss
                Rgov=Pmax-machloadpp
                Rt+=Rgov
            elif govMdl == 'WPIDHY':
                ierr,Pmax=psspy.dsrval('CON', icon0+12)
                ierr,P3=psspy.dsrval('CON', icon0+20)
                Pmax=min(Pmax,P3)*machloadss
                Rgov=Pmax-machloadpp
                Rt+=Rgov
            else :
                Pmax=machloadpmaxx
                Rgov = machloadpmaxx-machloadpp
                Rt+=Rgov
        fout.write ('%6d  %12s  %7s  %7.3f  %7.3f  %7.3f\n' % (ibus,busN,govMdl,Rgov,Pmax,machloadpp))
    fout.close()
    return Rt