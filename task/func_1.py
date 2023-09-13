import sys, os
PYTHONPATH = r'C:\Program Files\PTI\PSSE33\PSSBIN'
sys.path.append(PYTHONPATH)
os.environ['PATH'] += ';'+PYTHONPATH
import psspy
psspy.psseinit(0)

def areas_away1(POI):
    ierr, POI_area = psspy.busint(POI, 'AREA')
    jbus = 1
    final_areas = []
    ierr = psspy.initie(POI_area)
    while jbus != 0:
        ierr, ibus, jbus, ickt = psspy.nxttie()
        ierr, final_areas_reg = psspy.busint(jbus, 'AREA') 
        if final_areas_reg == None : break
        final_areas += [final_areas_reg]
    return final_areas

def areas_away2(POI, areas1):
    ierr, POI_area = psspy.busint(POI, 'AREA')
    final_areas = []
    areas11 = []
    for i in range(0,len(areas1)):
        jbus = 1                                #init value !=0
        ierr = psspy.initie(areas1[i])
        while jbus != 0:
            ierr, ibus, jbus, ickt = psspy.nxttie()
            ierr, areas11_reg = psspy.busint(jbus, 'AREA')
            if areas11_reg == None : break
            if (areas11_reg not in areas1) and (areas11_reg != POI_area):
                areas11 += [areas11_reg]
     
    ierr, iarray = psspy.aareaint(-1, string="NUMBER")
    total_areas = iarray[0]
    for i in range(0, len(total_areas)):
        if total_areas[i] in areas11:
            final_areas += [total_areas[i]]            
    areas1 = areas1 + final_areas
    return areas1, final_areas

def areas_away3(POI, areas1, areas2):
    final_areas = []
    areas11 = []
    areas22 = []
    ierr, POI_area = psspy.busint(POI, 'AREA')
    for i in range(0, len(areas2)):
        jbus = 1                              
        ierr = psspy.initie(areas2[i])
        while jbus != 0:
            ierr, ibus, jbus, ickt = psspy.nxttie()
            ierr, areas11_reg = psspy.busint(jbus, 'AREA')
            if areas11_reg == None : break
            areas11 += [areas11_reg]       
    for i in range(0, len(areas11)):
        if (areas11[i] not in areas1) and (areas11[i] != POI_area):
            areas22 += [areas11[i]]   
    ierr, iarray = psspy.aareaint(-1, string='NUMBER')
    total_areas = iarray[0]
    for m in range(0, len(total_areas)):
        if total_areas[m] in areas22:
            final_areas += [total_areas[i]]            
    areas1 = areas1 + final_areas
    return areas1, final_areas
