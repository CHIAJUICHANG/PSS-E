import sys, os
PYTHONPATH = r'C:\Program Files\PTI\PSSE33\PSSBIN'
sys.path.append(PYTHONPATH)   
os.environ['PATH'] += ';'+PYTHONPATH
from tkSimpleDialog import askinteger
from tkSimpleDialog import askstring
from Tkinter import Tk
from itertools import chain
import psspy
from psspy import _i, _f
from func_1 import *
import csv

test0 = os.path.join(r"C:\Program Files\114\txtfile\task_1\test0.txt")
test1 = os.path.join(r"C:\Program Files\114\txtfile\task_1\test1.txt")
progress = os.path.join(r"C:\Program Files\114\txtfile\task_1\progress.txt")
report = os.path.join(r"C:\Program Files\114\txtfile\task_1\report.txt")
incr = os.path.join(r"C:\Program Files\114\csvfile\Increase.csv")
decr = os.path.join(r"C:\Program Files\114\csvfile\Decrease.csv")
psspy.psseinit(0)
psspy.progress_output(2,progress)
psspy.report_output(2,report)
psspy.case(r'C:\Program Files\114\savfile\task_1.sav')

#   Part 1:
#   INCREASING GENERATION WITHIN SPECIFIED BUS LEVELS OF POI
#   Inputs:
#       test=1: from editible file -> OUTPUT0, OUTPUT1 , OUTPUT2
#       test=0: OUTPUT3, inp
#       check=1: OUTPUT, OUTPUT1
#       check=0: OUTPUT2
#       away_areas: number of areas away
#       lev: number of levels to be traversed
#       poi: point of interconnection
#       

root = Tk()
root.update()
test = askinteger("Opertaion Mode",
                  "If you are running program for first time press 0, if you are running program to implement changes made presss 1", initialvalue=0)

if test == 0:
    # in-service buses, not plant buses
    ierr, iarray = psspy.agenbusint(-1, 3, 'NUMBER')  
    # both interior subsystem branches and tie branches, all non-transformer branches and two-winding transformers
    ierr, iarray_from = psspy.abrnint(-1, 1, 3, 4, 1, 'FROMNUMBER')
    ierr, iarray_to = psspy.abrnint(-1, 1, 3, 4, 1, 'TONUMBER')
    iarray_from = iarray_from[0]
    iarray_to = iarray_to[0]
    len_from = len(iarray_from)                 # number of branches
    sys.stdout = open(test0, 'w')
    poi = askinteger('Input', 'Enter Point of Interconnection', initialvalue=10)
    lev = askinteger(
        'Input', 'Enter bus levels within which you want to traverse', initialvalue=5)
    print('point of interconnection : '+ str(poi) + '\n')
    print('level : '+ str(lev) + '\n')

    # output j_bus
    j_bus = [0]*len_from                        # traverse buses
    j_bus[0] = poi                              # fisrt element is poi
    flag = [0]*len_from*2
    i, j, k, w = 0, 0, 0, 0
    lbn, lbl = 1, 0                             #level bus now, level bus last
    lbc = 1                                     #level bus count
    while i < lev:
        while j < lbc:
            while k < len_from:
                if iarray_from[k] == j_bus[j]:  # if from bus is j_bus[i] save to bus
                    flag[w] = iarray_to[k]
                    w = w+1
                if iarray_to[k] == j_bus[j]:    # if to bus is j_bus[i] save from bus
                    flag[w] = iarray_from[k]
                    w = w+1
                if flag[w-1] not in j_bus:      # save flag if not in j_bus
                    j_bus[lbn] = flag[w-1]
                    lbn = lbn+1
                k = k+1
            k = 0
            j = j+1
        lbc = lbn-lbl+j-1
        lbl = lbn-1
        i = i+1

    #output blue
    blue = []
    for i in range(0, lbn) :
        ierr, ival = psspy.busint(j_bus[i], 'TYPE')
        if ival == 2 : blue += [j_bus[i]]       # blue is generation bus

    #blue + id              
    id_qun = 0                                  
    ierr, Nmach=psspy.amachcount(-1,4)          
    ierr, cMids = psspy.amachchar(-1,4, 'ID')
    ierr, iMbus = psspy.amachint(-1,4, 'NUMBER')
    iMbus=iMbus[0]
    cMids=cMids[0]
    for i in range(0,len(blue)) :               
        id = []
        for j in range(0,Nmach) :
            if blue[i] == iMbus[j] :
                id += [cMids[j]]
            if (j == Nmach) and (id == 'none') :
                print('Bus No found Machine')
                id = ['nnnnne']  
        blue[i] = [blue[i]]+id
    print('**********************************\n')
    print('found blue\n') 
    
    # Pushing these generator P limits to Max P, output inv_gen
    inc_gen = 0                                # total increase
    for i in range(0,len(blue)) :
        for qun in range(1,len(blue[i])) :
            ierr, maxval = psspy.macdat(blue[i][0], blue[i][qun], 'PMAX')
            ierr, gen_val = psspy.macdat(blue[i][0], blue[i][qun], 'P')
            inc_gen += maxval-gen_val
            ierr = psspy.machine_data_2(blue[i][0], blue[i][qun], [1, _i, _i, _i, _i, _i], [
                maxval, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
    print('**********************************\n')
    print('Pushing these generator P limits to Max P' + '\n')
    print('Net increase in Generation is : '+ str(inc_gen) + '\n')
    csvfile = open(incr, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['Bus','Id','Pgen','Qgen','Pmax','Qmax','Pmin','Qmin','MBASE'])
    for i in range(0,len(blue)) :
        for qun in range(1,len(blue[i])) :
            ierr, Qmax_listi = psspy.macdat(blue[i][0], blue[i][qun], 'QMAX')
            ierr, Pmax_listi = psspy.macdat(blue[i][0], blue[i][qun], 'PMAX')
            ierr, Qmin_listi = psspy.macdat(blue[i][0], blue[i][qun], 'QMIN')
            ierr, Pmin_listi = psspy.macdat(blue[i][0], blue[i][qun], 'PMIN')
            ierr, Pgen_listi = psspy.macdat(blue[i][0], blue[i][qun], 'P')
            ierr, Qgen_listi = psspy.macdat(blue[i][0], blue[i][qun], 'Q')
            ierr, MVA_listi = psspy.macdat(blue[i][0], blue[i][qun], 'MBASE')
            writer.writerow([blue[i][0], blue[i][qun], Pgen_listi, Qgen_listi, Pmax_listi, Qmax_listi, Pmin_listi, Qmin_listi, MVA_listi])
    csvfile.close()
    print('**********************************\n')
    print('New parameters is in increase.csv\n')
    print('**********************************\n')
    
    #output areas1, areas2
    ierr, iarray = psspy.aareaint(-1, string="NUMBER")
    total_areas = iarray[0]
    away_areas = askinteger(
        "Input", "Enter how many areas away you want to decrease generation", initialvalue=1, maxvalue=len(total_areas)-1, minvalue=1)
    check = askinteger(
        "Input", "If you want to edit data yourself press '1' else '0'", initialvalue=0)
    print('areas away  : '+ str(away_areas)+'\n')
    print('**********************************\n')
    ierr, bus = psspy.abusint(-1, string='NUMBER')
    bus = bus[0]
    first_area = areas_away1(poi)
    areas1, areas2 = areas_away2(poi, first_area)
    for i in range(0, away_areas-1):
        areas1, areas2 = areas_away3(poi, areas1, areas2)

    # ouput alareas
    ierr, POI_area = psspy.busint(poi, 'AREA')
    ierr, allareas = psspy.aareaint(-1, 2, 'NUMBER')
    alareas = allareas[0]
    list.remove(alareas, POI_area)
    for i in range(0,len(areas1)) :
        if areas1[i]  in alareas:
            alareas.remove(areas1[i])
    for i in range(0,len(areas2)) :
        if areas2[i] not in alareas:
            alareas += [areas2[i]]
    # if len(alareas) < away_areas :
    #     for i in range(0,len(areas1)) :
    #         if areas1[i] not in alareas:
    #             alareas += [areas1[i]]
    if len(alareas) < away_areas : print("Not Enough Area")
    print('found area : '+str(alareas)+'\n')
    print('**********************************\n')

    # output gen_bus 
    ierr, iarea = psspy.abusint(-1, string='AREA')
    iarea = iarea[0]
    gen_bus = []
    for i in range(0,len(iarea)) :
        ierr, itype = psspy.busint(bus[i], 'TYPE')
        if (iarea[i] in alareas) and (itype == 2) : gen_bus += [bus[i]]            
    for i in range(0,len(gen_bus)) :
        id = []
        for j in range(0,Nmach) :
            if gen_bus[i] == iMbus[j] : id += [cMids[j]]
            if (j == Nmach) and (id == 'none') :
                print('Bus No found Machine')
                id = ['nnnnne']  
        gen_bus[i] = [gen_bus[i]]+id
    print('found inside area '+str(alareas)+' bus\n')
    print('**********************************\n')

    if check == 0:                                      # must after test=0
        print('Start automatic decrease\n')
        if len(gen_bus) > 0:                            # number of generation bus  > 0
            dec = inc_gen/len(gen_bus)
            while 1:
                pgap = 0          
                for i in range(0,len(gen_bus)) :
                    for qun in range(1,len(gen_bus[i])) :
                        ierr, pminval = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'PMIN')
                        ierr, pval = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'P')
                        if pminval == pval: pgap += dec
                            # print(
                                # 'Generator at bus %s is already working on its minimum power' % (gen_bus[i]))
                        elif pval-dec < pminval:
                            pgap = pgap+(dec-(pval-pminval))
                            ierr = psspy.machine_data_2(gen_bus[i][0], gen_bus[i][qun], [
                                                    _i, _i, _i, _i, _i, _i],[pminval, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                        elif pval-dec > pminval:
                            ierr = psspy.machine_data_2(gen_bus[i][0], gen_bus[i][qun],[
                                                    _i, _i, _i, _i, _i, _i],[pval-dec, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                if pgap < 1: break                      #allowable error
                if dec == pgap/len(gen_bus):
                    print("Not Enough Power\n")
                    print(pgap)
                    break
                dec = pgap/len(gen_bus)
        else:
            print('No Generator Bus Within Specified Areas\n')
        csvfile = open(decr, 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(['Bus','Id','Pgen','Qgen','Pmax','Qmax','Pmin','Qmin','MBASE'])
        for i in range(0,len(gen_bus)) :
            for qun in range(1,len(gen_bus[i])) :
                ierr, Qmax_listd = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'QMAX')
                ierr, Pmax_listd = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'PMAX')
                ierr, Qmin_listd = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'QMIN')
                ierr, Pmin_listd = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'PMIN')
                ierr, Pgen_listd = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'P')
                ierr, Qgen_listd = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'Q')
                ierr, MVA_listd = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'MBASE')
                writer.writerow([gen_bus[i][0], gen_bus[i][qun], Pgen_listd, Qgen_listd, Pmax_listd, Qmax_listd, Pmin_listd, Qmin_listd, MVA_listd])
        csvfile.close()
        print('New parameters is in decrease.csv\n')
        ierr = psspy.fnsl([_i, _i, _i, _i, _i, _i, _i, _i])
        print('Solving by Newton Raphson Method\n')   
        ierr = psspy.pout(0, 1)
        print('Finish!!!')
        psspy.save(r"""C:\Program Files\114\savfile\task_change.sav""")
        sys.stdout.close()
        os.startfile(test0)

    if check == 1:
        print('Start manual Decrease\n')
        csvfile = open(decr, 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(['Bus','Id','Pgen','Qgen','Pmax','Qmax','Pmin','Qmin','MBASE'])
        for i in range(0,len(gen_bus)) :
            for qun in range(1,len(gen_bus[i])) :
                ierr, Qmax_listm = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'QMAX')
                ierr, Pmax_listm = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'PMAX')
                ierr, Qmin_listm = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'QMIN')
                ierr, Pmin_listm = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'PMIN')
                ierr, Pgen_listm = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'P')
                ierr, Qgen_listm = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'Q')
                ierr, MVA_listm = psspy.macdat(gen_bus[i][0], gen_bus[i][qun], 'MBASE')
                writer.writerow([gen_bus[i][0], gen_bus[i][qun], Pgen_listm, Qgen_listm, Pmax_listm, Qmax_listm, Pmin_listm, Qmin_listm, MVA_listm])
        csvfile.close()
        os.startfile(decr)
        print('New parameters is in decrease.csv\n')
        done = askstring(
            "Change", "Change done ?", initialvalue='done')
        data = list(csv.reader(open(decr)))
        data = list(chain.from_iterable(data))
        for i in range(1,len(data)/9) :
            bus_num = int(data[i*9])
            id_num = data[i*9+1]
            Pgen = float(data[i*9+2])
            Qgen = float(data[i*9+3])
            Pmax = float(data[i*9+4])
            Qmax = float(data[i*9+5])
            Pmin = float(data[i*9+6])
            Qmin = float(data[i*9+7])
            MVA = float(data[i*9+8])
            ierr = psspy.machine_data_2(bus_num, id_num, [1, _i, _i, _i, _i, _i], [
                Pgen, Qgen, Qmax, Qmin, Pmax, Pmin, MVA, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
        ierr = psspy.fnsl([_i, _i, _i, _i, _i, _i, _i, _i])
        print('Solving by Newton Raphson Method\n')
        ierr = psspy.pout(0, 1)
        print('Finish!!!')
        psspy.save(r"""C:\Program Files\114\savfile\task_change.sav""")
        sys.stdout.close()
        os.startfile(test0)
    
if test == 1:
    data = list(csv.reader(open(incr)))               # open 'incr.csv'
    data = list(chain.from_iterable(data))
    sys.stdout = open(test1, 'w')
    for i in range(1,len(data)/9) :
        bus_num = int(data[i*9])
        id_num = data[i*9+1]
        Pgen = float(data[i*9+2])
        Qgen = float(data[i*9+3])
        Pmax = float(data[i*9+4])
        Qmax = float(data[i*9+5])
        Pmin = float(data[i*9+6])
        Qmin = float(data[i*9+7])
        MVA = float(data[i*9+8])
        ierr = psspy.machine_data_2(bus_num, id_num, [1, _i, _i, _i, _i, _i], [
            Pgen, Qgen, Qmax, Qmin, Pmax, Pmin, MVA, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
    print('Generation was increased on following buses \n')
    print('**********************************\n')
    data = list(csv.reader(open(decr)))
    data = list(chain.from_iterable(data))
    for i in range(1,len(data)/9) :
        bus_num = int(data[i*9])
        id_num = data[i*9+1]
        Pgen = float(data[i*9+2])
        Qgen = float(data[i*9+3])
        Pmax = float(data[i*9+4])
        Qmax = float(data[i*9+5])
        Pmin = float(data[i*9+6])
        Qmin = float(data[i*9+7])
        MVA = float(data[i*9+8])
        ierr = psspy.machine_data_2(bus_num, id_num, [1, _i, _i, _i, _i, _i], [
            Pgen, Qgen, Qmax, Qmin, Pmax, Pmin, MVA, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
    print('Now implementing decrese of power as user has suggested in editable file\n')
    print('**********************************\n')
    ierr = psspy.fnsl([_i, _i, _i, _i, _i, _i, _i, _i])  
    print('performing Newton Raphson load flow analysis\n')
    ierr = psspy.pout(0, 1)                     # power flow solution
    print('Finish!!!')
    psspy.save(r"C:\Program Files\114\savfile\task_change.sav")
    sys.stdout.close()                          # close OUTPUT0
    os.startfile(test1)