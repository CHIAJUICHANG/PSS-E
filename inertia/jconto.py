import os,sys
PSSE_LOCATION=r"C:\PTI\PSSE33\PSSBIN"
sys.path.append(PSSE_LOCATION)
# import psse33
os.environ['path']=os.environ['path'] + ';' + PSSE_LOCATION

import psspy
# psspy.dyre_new([1,1,1,1],r"""C:\PSSE\114\114P.dyr""","","","")

psspy.case(r"C:\PSSE\114\114p.sav")
psspy.rstr(r"C:\PSSE\114\114p.snp")


def system_inertia(sid=-1,btflag=1,idfilter=''):
    '''Returns machine inertia.
    input: case and snp file in memory
    '''
    # select generators
    ierr, (busnums,bustypes)  = psspy.abusint(sid, btflag, string=['NUMBER','TYPE'])

    # get just plant buses    
    plantbuses = [busnum for busnum,bustype in zip(busnums,bustypes) if bustype in [2,3]]

    # Note there could be > 1 machines at a bus.
    # Bus number and ID define unique machine.
    ierr, (machbuses,) = psspy.amachint(sid, btflag, string=['NUMBER'])
    ierr, (machstatus,)= psspy.amachint(sid, btflag, string=['STATUS'])
    ierr, (machids,)   = psspy.amachchar(sid,btflag, string=['ID'])
    machines = zip(machbuses,machids,machstatus)
    machdyn_data = {}

    # machine index    
    for mach in machines:
        ierr, machidx = psspy.macind(mach[0], mach[1])
        machdyn_data[mach] = {'index': machidx}
    # model names    
    mdlstrs = ['GEN', 'COMP', 'STAB', 'EXC', 'GOV', 'TLC', 'MINXL', 'MAXXL']
    mdlqtys = ['CON']
    for mach in machines:
        for mdl in mdlstrs:
            ierr, mnam = psspy.mdlnam(mach[0], mach[1], mdl)
            if mnam:
                machdyn_data[mach][mdl.lower()] = {'name': mnam.strip()}
                for qty in mdlqtys:
                    ierr, ival = psspy.mdlind(mach[0], mach[1], mdl, qty)
                    machdyn_data[mach][mdl.lower()][qty.lower()] = ival

    # Inertia, CON index
    # GENCLS = J
    # GENDCO,GENROE,GENROU,GENTPJ1 = J+4
    # GENSAE,GENSAL = J+3
    # GENTRA = J+1

    # Get inertia
    synchmacs= []
    for mach in machines:
        if not mach[2]: continue
        if not machdyn_data[mach].has_key('gen'): continue
        genmdl = machdyn_data[mach]['gen']['name']
        genmdl = genmdl.strip()
        conidx = machdyn_data[mach]['gen']['con']
        if   genmdl in ['GENDCO', 'GENROE', 'GENROU', 'GENTPJ1']:
             hindx = conidx + 4
        elif genmdl in ['GENSAE', 'GENSAL']:
             hindx = conidx + 3
        elif genmdl == 'GENTRA':
             hindx = conidx + 1
        #elif   genmdl == 'GENCLS':   #
        #     hindx = conidx
        else:
             print ('Inertialess Machine model found:%s'%genmdl)
             continue
        ierr, rval = psspy.dsrval('CON', hindx)
        machdyn_data[mach]['gen']['inertia'] = rval
        synchmacs.append(mach) 

    sysinertia = 0.0
    scale= 0.001    # to get GW-sec.  If scale=1, Sys Inertia is in MW-sec
    print ("     Bus   ID\tMacInertia\tTotalInertia")
    for mac in synchmacs:
        busnum = mac[0]
        macid  = mac[1]
        macstat= mac[2]
        if idfilter:
           if macid.strip()[0] <> idfilter.strip(): continue
        if macstat:
           inertia= machdyn_data[mac]['gen']['inertia']
           ierr, macbase = psspy.macdat(busnum, macid, 'MBASE')
           macinertia  = inertia*macbase
           sysinertia += macinertia
           print '%8s,  %s,  %6.2f,  \t%6.2f'%(busnum,macid,macinertia*scale,sysinertia*scale)
    return sysinertia*scale

if __name__ == '__main__':
   # ==================================================================================
   import os, sys
   # about PSSe GUI
   try:
     psspy
     GUI = True
   except:
     GUI = False
     import psse33
     #import psse34
     import psspy
     psspy.psseinit(150000)
   
   loadedsav,loadedsnp = psspy.sfiles()
   if not loadedsav:
      savfile = r"C:\Program Files (x86)\PTI\PSSE33\EXAMPLE\savnw.sav"
      snpfile = r"C:\Program Files (x86)\PTI\PSSE33\EXAMPLE\savnw.snp"  
      psspy.case(savfile)
      psspy.rstr(snpfile)

   # define subsystem for Area of interest
   sid    = -1       # default= -1 = All buses, or enter 0-9 for a subsystem:
   basekv = []
   areas  = []
   buses  = []
   owners = []
   zones  = []
   if basekv: 
      usekv = 1
   else:
      usekv = 0    
   btflag  = 1       # default=1 online buses only, =2 all bus types
   idfilter= ''      # to select by gen types, enter char in macid (i.e.:idfilter='H')
   if sid > -1:    
      ierr = psspy.bsys(sid, 
                        usekv      , basekv, 
                        len(areas) , areas, 
                        len(buses) , buses,
                        len(owners), owners, 
                        len(zones) , zones)
   sysinertia = system_inertia(sid,btflag=btflag,idfilter=idfilter)
   #sysinertia = system_inertia()     #to use all defaults
   print "\n System Inertia: %6.2f GW-sec"%sysinertia