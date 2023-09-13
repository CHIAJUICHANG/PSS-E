import os,sys
PSSE_LOCATION = r"C:\Program Files\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION
import psspy
casefile=os.path.join(r"C:\Program Files\114\savfile\original file\117P-11007.sav")
progfile=os.path.join(r"C:\Program Files\114\txtfile\114p_shunt.txt")
psspy.psseinit(0)
_i=psspy.getdefaultint();_f=psspy.getdefaultreal();_s=psspy.getdefaultchar();
psspy.progress_output(2,progfile)

psspy.case(casefile)
ierr, shunts = psspy.afxshuntcount(-1,1)
ierr, carray = psspy.afxshuntchar(-1,1,'ID')
ierr, iarray = psspy.afxshuntint(-1,1,'NUMBER')
ierr, xarray = psspy.afxshuntcplx(-1,1,'SHUNTNOM')
carray=carray[0]
iarray=iarray[0]
xarray=xarray[0]
for iM in range(0,shunts):
    if xarray[iM].real < 0 :
        psspy.bus_chng_3(iarray[iM],[2,_i,_i,_i],[_f,_f,_f,_f,_f,_f,_f],_s)
        psspy.plant_data(iarray[iM],_i,[_f,_f])
        psspy.machine_data_2(iarray[iM],carray[iM],[_i,_i,_i,_i,_i,1],[xarray[iM].real*(-1),0,0,0,xarray[iM].real*(-1)/0.06,0,xarray[iM].real*(-1)/0.06,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
        psspy.shunt_chng(iarray[iM],carray[iM],0,[_f,_f])
ierr=psspy.fnsl([1,0,0,1,1,1,-1,0]) 
ierr=psspy.fnsl([0,0,0,1,0,0,0,0])
psspy.save(r"C:\Program Files\114\savfile\114p_shunt.sav")
