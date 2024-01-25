import sys
sys.path.append(r'lib')
sys.path.append(r'mdl/input')     # must run at FFR directory
from init_simu import *
from snap_input import *
flim = 59.5
# 0: freq; 1: RoCoF; 2: RoCoF ref; 3: PI-RoCoF; 4: PI-RoCoF ref 
k = 1
Kctl = np.array([32,76,115,32,47])
chngsize = 40 #42 # largest contingency
# sfile_out = os.path.join(dir, 'out', 'mdl_FFR2_%d.out'%(Kctl[k]))
if k in [1,2]: Kp, Ki = 1, 0
else: Kp, Ki = 1, 0.2
_i, _f, _s = psspy.getdefaultint(), psspy.getdefaultreal(), psspy.getdefaultchar()
psspy.case(ofile_sav)
psspy.rstr(ofile_snp)
# psspy.dynamics_solution_param_2(integar1=50,realar1=0.5, realar3=DELT)#, realar4=4*DELT)

# find critical and limit
# C = 1.5
# ierr, icon0 = psspy.mdlind(1, '1', 'GEN', 'CON') # G1
# ierr, H = psspy.dsrval('CON', icon0+3)
# psspy.change_con(icon0+3, H*C) # 9.55
# ierr, icon0 = psspy.mdlind(2, '1', 'GEN', 'CON') # G2
# ierr, H = psspy.dsrval('CON', icon0+4)
# psspy.change_con(icon0+4, H*C) # 3.33
# ierr, icon0 = psspy.mdlind(3, '1', 'GEN', 'CON') # G3
# ierr, H = psspy.dsrval('CON', icon0+4)
# psspy.change_con(icon0+4, H*C) # 5.00
# print('Hsys: %.3f'%Hsys(Sid = -1, c = 0))

# load damping
# D = 1
# for i in [5,6,8]:
#     psspy.change_ldmod_con(i,r"""1""",r"""IEELBL""",7, D)
# damp = D * (125+90+100) * (flim-60)/60
# print(damp)

ierr, ivar0 = psspy.windmind(10, '1', 'WAUX', 'VAR')
ierr, ichan = psspy.var_channel([ichan, ivar0+8],"L+8"), ichan + 1
if k==0: psspy.change_con(icon0+26, Kctl[k]) # Kctl
else:
    psspy.addmodellibrary(ofile_dll)
    psspy.change_icon(iicon0_I+1, ivar0+2)
    if k in [1,3]: psspy.change_icon(iicon0_I+2, 0)     # REF
    ref_ls = [[0,flim/60.0-1],                          # flim
              [1,0.05],[2,0.15], [3,0.05],              # Tf, TRoCoF, TFFR
              [4,Kp], [5,Ki],                           # KP, KI
              [6,Kctl[k]],[15,chngsize*1.1],           # Kctl, Pset 1.1
              [16,0.0],                       # trigger frequency (close when using actual PFR)
              [19,0],[20,1]]
    for x in ref_ls:
        psspy.change_con(icon0_J+x[0], x[1])
    chan_nam = ['FILTERED FREQ  VAR(L)','FILTERED ROCOF VAR(L+1)',
                'tmax VAR(L+2)','ROCOFREF VAR(L+3)','ERR VAR(L+4)', 
                '5','6','Pest VAR(K+7)']
    for i in [0,1,2,3,4,7]:
        ierr, ichan = psspy.var_channel([ichan, ivar0_L+i], chan_nam[i]), ichan + 1
# BESS
ierr, icon0 = psspy.windmind(10, '1', 'WGEN', 'CON')
psspy.change_con(icon0+10, 0.95) # overvoltage
psspy.change_con(icon0+13, 0.1) # Acc origin 0.7 not influence at all
# ierr, iicon0 = psspy.windmind(10, '1', 'WELEC', 'ICON')
# psspy.change_icon(iicon0+2, 0) # voltage control
# psspy.change_icon(iicon0+5, 1) # P priority
ierr, iicon0 = psspy.windmind(10, '1', 'WAUX', 'ICON')
psspy.change_icon(iicon0+6, 1) # frequency control
ierr, icon0 = psspy.windmind(10, '1', 'WAUX', 'CON')
BESS_con = [[18,0],[19,0],[25,1],[26,1]] # fdb,fdb,Ddn,Dup
for x in BESS_con:
    psspy.change_con(icon0+x[0], x[1]) # fdb
# ierr, istate0 = psspy.windmind(10, '1', 'WAUX', 'STATE')
# ierr, ichan = psspy.state_channel([ichan, istate0+5], r"""K+5"""), ichan + 1

# BESS
ierr, ichan = psspy.bus_frequency_channel([ichan, 3]), ichan + 1  # freqeuncy from voltage
ierr, ichan = psspy.bus_frequency_channel([ichan, 10]), ichan + 1  # freqeuncy from voltage
# ierr, ichan = psspy.machine_array_channel([ichan, 7, 10], '1', ""), ichan + 1  # spd
ierr, ichan = psspy.machine_array_channel([ichan, 2, 10], '1', ""), ichan + 1  # pelec
# ierr, ichan = psspy.voltage_and_angle_channel([ichan, -1, -1, 10], ["",""]), ichan + 2  # voltage and angle
# conventional
if k in [1,2,4]:
    for i in [1,2,3]:
        ierr, ichan = psspy.machine_array_channel([ichan, 6, i], '1', ""), ichan + 1  # pmech
        ierr, ichan = psspy.machine_array_channel([ichan, 2, i], '1', ""), ichan + 1  # pelec
        # ierr, ichan = psspy.machine_array_channel([ichan, 14, i], '1', ""), ichan + 1  # gref

ierr = psspy.strt_2([0, 0], sfile_out)
if ierr == 0: os.system("Code mdl/plot_1.py")
else: os.system("Code report/progress.txt")

psspy.run(0, 1, n, n, 0)
psspy.set_netfrq(1)
# disturbance
# load variation constant power
# psspy.load_chng_5(5, '1', realar1=125+10) # 5 is fine 10 2.75
# psspy.run(0, 4, n, n, 0)
psspy.load_chng_5(5, '1', realar1=125+chngsize)
psspy.run(0, 10, n, n, 0)