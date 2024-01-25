import sys
sys.path.append(r'lib')     # must run at FFR directory
sys.path.append(r'mdl/input')     # must run at FFR directory
from init_plot import *
from plot_input import *
_i, _f, _s = psspy.getdefaultint(), psspy.getdefaultreal(), psspy.getdefaultchar()
mbus = 3
flim = 59.5
k = 2
Kctl = 34*2
a = 50*np.arange(2,7)
psspy.case(ofile_sav)
psspy.rstr(ofile_snp)
psspy.addmodellibrary(ofile_dll)
chnfobj = dyntools.CHNF(ofile_out)
title, chanid, chandata = chnfobj.get_data()
print(chanid)

time = np.array(chandata['time'])
datalen = len(time)
endtime = time[-1]

# FREQ and BESS
# spd = np.array(chandata[chandata_from("SPD", chanid)[0]])
for ichan in chandata_from("FREQ", chanid):
    label, ibus, iId = chanbus(chanid[ichan],'Q ',1)
    freq = 60+60*np.array(chandata[ichan])
    if ibus==mbus: 
        ax[0].plot(time, freq, label='Frequency')
#    if ibus==mbus:
        # RoCoF_t = (freq[2:]-freq[:-2])/DELT/2
        # ax[2].plot(time[1:-1], RoCoF_t, label='RoCoF (central differences for derivative)')
    # else: ax[0].plot(time, freq, label=ibus)
if k!=0:
    ffreq = 60+60*np.array(chandata[chandata_from('FILTERED FREQ VAR(L)', chanid)[0]])
    ax[0].plot(time, ffreq,':', label='Filtered frequency')
    idx_nadir = np.argmin(ffreq)
    time_nadir = time[idx_nadir]
    delay = time[find_nearest(ffreq[0:200], delay_f)]
    f_nadir = min(ffreq)
    print('%2d nadir: %.3f,%.3f'%(ibus,round(f_nadir,3),round(time_nadir,3)))
    if f_nadir >= flim and f_nadir <flim+0.01: print('inside')
    # print(df[find_nearest(df[0:250], delay_f/60-1)]*60+60,delay)
ax[0].axhline(flim,color='g',ls='--')
# ax2.plot(time, spd*60+60, label='spd')
# ax[0].plot(time, ffreq, '--', label='filtered freq  VAR(L)')
# ax2.plot([1,3],[60,60-0.34*2],'--') # *1.5

# ROCOF
if k!=0:
    RoCoF_f = 60*np.array(chandata[chandata_from('FILTERED ROCOF', chanid)[0]])
    ax[2].plot(time, RoCoF_f, '-', label='RoCoF (Washout filter)')
    # ax[2].plot(time[RoCoF_f==min(RoCoF_f)],min(RoCoF_f),'o')
if k in [2,4]:
    RoCoFref = 60*np.array(chandata[chandata_from('ROCOFREF', chanid)[0]])
    ax[2].plot(time, RoCoFref,'--', label='$RoCoF_{ref}$')#VAR(L+2)
    # ax[2].plot(time[a], 60*RoCoFref[a],'o', label='$RoCoF_{ref}$')#VAR(L+2)
    for i in a:
        ax[0].plot([time[i],time[i]+(flim-ffreq[i])/RoCoFref[i]],[ffreq[i],flim],'--')
    # critical and limit
    print('critical:%.5f;limit:%.5f'%(min(RoCoF_f),RoCoFref[0]))
# ax[2].axhline(-0.2)
ax[2].set_ylim([-1, 1])
ax3=ax[2].twinx()
ax3.plot(time,ffreq, 'r:', label='Frequency')
ax3.set_ylabel('Frequency (Hz)')
ax3.legend(loc='upper right')

# Pest PMEC
ax[1].plot(time,Pest_GGOV1_r(ffreq/60-1),ls='--',label='$P_{est,1}$')
if k in [2,4]:
    chandata_from("PEST VAR(K+7)", chanid)
    PEST = np.array(chandata[chandata_from('PEST VAR(K+7)', chanid)[0]])
    ax[1].plot(time,PEST,'b-.',label='$P_{est,3}$')
    totPMECH = np.zeros(datalen)
    iT_Pest = np.arange(0,endtime-delay,0.1)
    for ichan in chandata_from("PMEC", chanid):
        label, ibus, iId = chanbus(chanid[ichan],'C ',1)
        ierr, S = psspy.macdat(ibus,iId,'MBASE')
        iPMECH = S*(np.array(chandata[ichan])-chandata[ichan][0])
        totPMECH = totPMECH + iPMECH

        # ierr, icon0 = psspy.mdlind(ibus, iId, 'GOV', 'CON') # get initial CON address (index)
        # ierr, R = psspy.dsrval('CON', icon0)
        # ierr, vmax = psspy.dsrval('CON', icon0+8)
        # ierr, Kturb = psspy.dsrval('CON', icon0+11)
        # ierr, wfnl = psspy.dsrval('CON', icon0+12)
        # ierr, Ropen = psspy.dsrval('CON', icon0+21)
        # ierr, P = psspy.macdat(ibus,iId,'P')
        # dPmax = S*Kturb*(vmax-wfnl)-P
        # RR = Kturb*Ropen
        # Pdroop = -Kturb*(flim/60-1)/R
        # iP_est = np.zeros(len(iT_Pest))
        # for i in range(len(iT_Pest)):
        #     iP_est[i] = min([S*RR*iT_Pest[i], S*Pdroop, dPmax])
        # print('(ibus,P,Pmax,MBASE)',ibus, round(P,3), round(dPmax+P,3), S)
    # T_Pest = np.arange(0,endtime-delay,0.1)
    # P_est = np.zeros(len(T_Pest))
    # for i in range(len(T_Pest)):
    #     P_est[i] = Pest_GGOV1(T_Pest[i], flim)
    # T_Pest = T_Pest + delay #delay # 10 2.75
    # ax[1].plot(T_Pest,P_est,ls=':',label='$P_{est,2}$ with %.3f s delay'%(delay-1))
    ax[1].plot(time, totPMECH, label='$PFR$')
    # ax[1].axhline(y=totPMECH[-1],ls='--')
    
    Tresp = np.array(chandata[chandata_from("TMAX", chanid)[0]])
    ax2.plot(time, Tresp,'r:', label='$T_{resp}$')
    print('Tresp: %.3f,%.3f'%(Tresp[0],Tresp[-1]))

totPELEC = np.zeros(datalen)
for ichan in chandata_from("POWR", chanid):
    label, ibus, iId = chanbus(chanid[ichan],'R ',1)
    iPELEC = 100*(np.array(chandata[ichan])-chandata[ichan][0])
    totPELEC = totPELEC+iPELEC
    if ibus==10:
        BESS = iPELEC
        ax1.plot(time, BESS,'r', label='BESS')
        ax[3].plot(time, BESS,'r', label='BESS')
        # V8 = np.array(chandata[chandata_from("L+8", chanid)[0]])
        # ax[3].plot(time, V8*60,'r:', label='V8')
        # BESS
        if k!=0:
            ERR = np.array(chandata[chandata_from("ERR", chanid)[0]])
            ax[3].plot(time, Kctl*ERR*60, label='ERR')
ax[3].plot(time,totPELEC,label='$\Delta P_{loss}$')
ax[3].set_ylim([-5, 70])

# voltage
# vol = np.array(chandata[chandata_from("VOLT", chanid)[0]])
# ang = np.array(chandata[chandata_from("ANG", chanid)[0]])
# ax[4].plot(time,ang)

# for i in [0,1,2,3]:
#     ax[i].axvline(time_nadir,ls='-.',label='$t_{nadir}$')

for _ax in ax:
    _ax.legend(loc='lower right')
    _ax.set_xlim([0, endtime])
ax1.legend(loc='upper right')
ax2.legend(loc='upper right')

print('MAX: %.3f'%max(BESS))
from sklearn.metrics import auc
print('computed AUC: {}'.format(round(auc(time,BESS),3))) #using sklearn.metrics.auc

plt.show()