      SUBROUTINE AGC(M,J,K,L)
      INCLUDE 'COMON4.INS'
      INTEGER   J,      K,       L,       N,      JJ,         KK,        II,      IVEL
      INTEGER NDM,      I,     NUM,   agcyc,   IEAAC, AGC_status,       reg,      IERR
      REAL     BF,     Kp,      Ki,      Kd,      Td,       AACt,      VINP,      VOUT,    tmp,   Pab
      REAL     df,     Yi,      Yd,      IN,     ACE,       DEL2,   Pregsys,       mul,  time1,  Ptmp
      LOGICAL NEW
      INTEGER          ::   IM(42), IBUS(42),   ID(42), IB(42), ST(42),  IH(42)
      REAL             :: Pmax(42), Preg(42),  AAC(42),  P(42),  R(42),   H(42)
      CHARACTER(len=20)::   GOVNAM
      AGC_status  = ICON(M)
      agcyc       = ICON(M+1)
      NDM         = ICON(M+2)
      BF          = CON(J)
      Kp          = CON(J+1)
      Ki          = CON(J+2)
      Kd          = CON(J+3)
      Td          = CON(J+4)
      POI         = CON(J+5+NDM*2)
      AACt        = 0.0
      Pab         = 0
      reg         = 2
      df          = 0.0
      Pmax(1)     = 240.5
      Pmax(2)     = 105.0
      Pmax(3)     = 105.0
      Pmax(4)     = 24.05
      Pmax(5)     = 24.05
      Pmax(6)     = 24.05
      Pmax(7)     = 24.05
      Pmax(8)     = 24.05
      DO 1 I = 1, NDM
      IBUS(I)  = ICON(M+1+2*I)
      ID(I)    = ICON(M+2+2*I)+48
      CALL GENCHK(IBUS(I),    CHAR(ID(I)),    IM(I), 'GENCHK cannot find the specified machine')
      CALL MACINT(IBUS(I),    CHAR(ID(I)), 'STATUS',  ST(I), IERR)
      IB(I)    = ABS(NUMTRM(IM(I)))
      df       = df+BSFREQ(IB(I))
      CALL MDLNAM(IBUS(I),    CHAR(ID(I)),    'GOV', GOVNAM, IERR)
      IF(.NOT.(GOVNAM.EQ.'HYGOV')) GO TO 32758
      CALL MDLIND(IBUS(I), CHAR(ID(I)),    'GOV',  'CON',  IVEL, IERR)
      R(I)  = CON(IVEL)
      CALL MDLIND(IBUS(I), CHAR(ID(I)),    'GOV',  'VAR', IH(I), IERR)
      GO TO 32759
32758 R(I)  = 0.0
      IH(I) = 0
32759 IF(.NOT.(GOVNAM.EQ.'WEHGOV')) GO TO 32757
      CALL MDLIND(IBUS(I), CHAR(ID(I)),    'GOV',  'CON',  IVEL, IERR)
      R(I)  = (CON(IVEL)+0.0007)
      CALL MDLIND(IBUS(I), CHAR(ID(I)),    'GOV',  'VAR', IH(I), IERR)
32757 IF(.NOT.(GOVNAM.EQ.'WPIDHY')) GO TO 32756
      CALL MDLIND(IBUS(I), CHAR(ID(I)),    'GOV',  'CON',  IVEL, IERR)
      R(I)  = (CON(IVEL+1))
      CALL MDLIND(IBUS(I), CHAR(ID(I)),    'GOV',  'VAR', IH(I), IERR)
32756 CONTINUE
1     CONTINUE
      df      = df*60.0/NDM
      ACE     = -10.0*BF*df
      VAR(L)  = ACE
      IF(.NOT.(df.GE.0.03)) GO TO 32754
      reg = 0
      GO TO 32755
32754 IF(.NOT.(df.LE.-0.03)) GO TO 32753
      reg = 1
      GO TO 32755
32753 reg = 2
32755 DO 10 I = 1, NDM
      IBUS(I)   = ICON(M+1+2*I)
      ID(I)     = ICON(M+2+2*I)+48
      P(I)      = PMECH(IM(I))*MBASE(IM(I))
      IF(.NOT.(reg.EQ.0)) GO TO 32751
      AAC(I) = MAX(-CON(J+I+4)*agcyc/60.0, -P(I))
      GO TO 32752
32751 AAC(I)    = MIN(CON(J+I+4)*agcyc/60.0, Pmax(I)-P(I))
32752 Ptmp = Pmax(I)-P(I)
      IF (Ptmp.LT.0)   Ptmp   = 0
      IF (AAC(I).LT.0) AAC(I) = 0
      IF (IM(I).EQ.0) RETURN
      IF (TIME.LT.1) H(I) = 1.0
      VAR(L+2+4*I-3)      = P(I)
      AACt                = AACt+AAC(I)
      Pab                 = Pab+Ptmp
      IF(.NOT.(reg.EQ.2)) GO TO 32750
      Pregsys = 0
      Preg(I) = 0
      AAC(I)  = 0
      AACt    = 0
32750 CONTINUE
10    CONTINUE
      VAR(L+36) = Pab
      IF(.NOT.(MODE.EQ.8)) GO TO 32749
      CON_DSCRPT(1) = 'STATE'
      CON_DSCRPT(2) = 'AGC cycle time'
      CON_DSCRPT(3) = 'NDM'
      RETURN
32749 IF (MODE.GT.4) GO TO 20
      IF(.NOT.(MIDTRM)) GO TO 32747
      IF(.NOT.(INSITR)) GO TO 32745
      IN = VAR(L)
      IF (KPAUSE.EQ.2) IN = (IN+STORMT(2*K-1))*0.50
      Yi = Ki*DELT/2.0*IN+STORE(K)
      Yd = (IN*Kd+STORE(K+1))/(1.0+2.0*Td/DELT)
      GO TO 32746
32745 IF(.NOT.(MODE.EQ.1)) GO TO 32744
      IN = VAR(L)
      STORE(K)   = 0.0
      STORE(K+1) = IN*Kd
      GO TO 32746
32744 IF(.NOT.(MODE.EQ.2)) GO TO 32743
      IF(.NOT.(KPAUSE.EQ.1)) GO TO 32741
      STORMT(2*K-1) = VAR(L)
      GO TO 32742
32741 IN = VAR(L)
      IF (KPAUSE.EQ.2) IN = (IN+STORMT(2*K-1))*0.50
32742 Yi         = Ki*DELT/2.0*IN+STORE(K)
      STORE(K)   = Yi+IN*Ki*DELT/2.0
      Yd         = (IN*Kd+STORE(K+1))/(1.0+2.0*Td/DELT)
      STORE(K+1) = IN*Kd-Yd*(1.0-2.0*Td/DELT)
32743 CONTINUE
32746 RETURN
      GO TO 32748
32747 IF(.NOT.(MODE.EQ.1)) GO TO 32739
      VOUT   = VAR(L+1)
      VINP   = PID_MODE1(Kp,Ki,Kd,Td,VOUT,K,K+1,IEAAC)
      GO TO 32740
32739 IF(.NOT.(MODE.EQ.2)) GO TO 32738
      VINP     = VAR(L)
      VOUT     = PID_MODE2(Kp, Ki, Kd, Td, VINP, K, K+1)
      GO TO 32740
32738 IF(.NOT.(MODE.EQ.3)) GO TO 32737
      VINP    = VAR(L)
      VOUT    = PID_MODE3(Kp, Ki, Kd, Td, VINP, K, K+1)
      Pregsys = VOUT
      tmp     = 0
      IF(.NOT.((MOD(INT((TIME)/0.001), agcyc) .LE. 0) .AND. (reg.NE.2)))
     1 GO TO 32736
      PRINT *,TIME
      DO 14 I = 1, NDM
      Preg(I) = Pregsys*AAC(I)/AACt
      IF(.NOT.((AGC_status .EQ. 1) .AND. (abs(Pregsys) .LT. abs(AACt))))
     1 GO TO 32735
      mul     = 1
      IF(.NOT.(reg.EQ.1 .AND. (PMECH(IM(I))*MBASE(IM(I))).LT.Pmax(I))) G
     1O TO 32734
      IF (R(I).EQ.0.0) GREF(IM(I)) = GREF(IM(I))+MIN(Preg(I), AAC(I))/MBASE(IM(I))
      IF(.NOT.(R(I).GT.0.0)) GO TO 32733
      IF (IH(I).GT.0) mul       = VAR(IH(I)+1)*SQRT(VAR(IH(I)+1))/1.2
      GREF(IM(I)) = GREF(IM(I))+MIN(Preg(I), AAC(I))/MBASE(IM(I))*mul*R(I)
32733 tmp = tmp+MIN(Preg(I), AAC(I))
      PRINT *,"state 1"
32734 IF(.NOT.(reg.EQ.0 .AND. (PMECH(IM(I))*MBASE(IM(I))).GT.0)) GO TO 3
     12732
      IF (R(I).EQ.0.0) GREF(IM(I)) = MAX(0.0, GREF(IM(I))+MAX(Preg(I),AAC(I))/MBASE(IM(I)))
      IF(.NOT.(R(I).GT.0.0)) GO TO 32731
      IF (IH(I).GT.0) mul       = VAR(IH(I)+1)*SQRT(VAR(IH(I)+1))/1.2
      GREF(IM(I)) = GREF(IM(I))+MAX(Preg(I), AAC(I))/MBASE(IM(I))*mul*R(I)
32731 tmp = tmp+MAX(Preg(I), AAC(I))
      PRINT *,"state 2"
32732 CONTINUE
32735 IF(.NOT.((AGC_status .EQ. 1) .AND. (abs(Pregsys) .GE. abs(AACt))))
     1 GO TO 32730
      IF(.NOT.(reg.EQ.1 .AND. (PMECH(IM(I))*MBASE(IM(I))).LT.Pmax(I))) G
     1O TO 32729
      IF (R(I).EQ.0.0) GREF(IM(I)) = GREF(IM(I))+AAC(I)/MBASE(IM(I))
      IF(.NOT.(R(I).GT.0.0)) GO TO 32728
      IF (IH(I).GT.0) mul       = VAR(IH(I)+1)*SQRT(VAR(IH(I)+1))/1.2
      GREF(IM(I)) = GREF(IM(I))+AAC(I)/MBASE(IM(I))*mul*R(I)
32728 tmp = tmp+AAC(I)
32729 IF(.NOT.(reg.EQ.0 .AND. (PMECH(IM(I))*MBASE(IM(I))).GT.0)) GO TO 3
     12727
      IF (R(I).EQ.0.0) GREF(IM(I)) = MAX(0.0, GREF(IM(I))+AAC(I)/MBASE(IM(I)))
      IF(.NOT.(R(I).GT.0.0)) GO TO 32726
      IF (IH(I).GT.0) mul       = VAR(IH(I)+1)*SQRT(VAR(IH(I)+1))/1.2
      GREF(IM(I)) = GREF(IM(I))+AAC(I)/MBASE(IM(I))*mul*R(I)
32726 tmp = tmp+AAC(I)
      PRINT *,"state 4"
32727 CONTINUE
32730 IF(.NOT.(TIME.GT.60 .AND. AAC(I).GT.0.1)) GO TO 32725
      PRINT *,I
      PRINT *,AAC(I)
32725 H(I)           = VAR (IH(I)+1)
      VAR(L+2+4*I-2) = Preg(I)
      VAR(L+2+4*I-1) = GREF(IM(I))
      VAR(L+2+4*I)   = AAC (I)
14    CONTINUE
      VAR(L+2)  = AACt
      VAR(L+35) = Pregsys
      IF (abs(Pregsys) .GE. abs(AACt)) PRINT *,"not enough"
32736 RETURN
      GO TO 32740
32737 IF(.NOT.(MODE.EQ.4)) GO TO 32724
      NINTEG = MAX(NINTEG,K+1)
32724 CONTINUE
32740 RETURN
32748 CONTINUE
20    IF (MODE.EQ.6) GO TO 21
      IF(.NOT.(MODE.EQ.5)) GO TO 32723
      CALL DOCUHD(*30)
      GO TO 31
32723 NEW  = .FALSE.
      DEL2 = 2.*DELT
      ASSIGN 32721 TO I32722
      GO TO 32722
32721 IF(.NOT.(NEW)) RETURN
31    JJ = J+7
      KK = K+1
      WRITE(IPRT, 100) M, M+2*NDM, J, J+4+NDM, K, K+1, L, L+2+2*NDM
      WRITE(IPRT, 101) ICON(M), ICON(M+1), ICON(M+2)
      WRITE(IPRT, 103)
      DO 15 II = 1, NDM
      WRITE(IPRT, 104) IBUS(II), BUSNAM(IB(II)), CHAR(ID(II)), abs(AAC(II)), ST(II)
15    CONTINUE
      DO 16 II = 0, NDM/5-1, 1
      NUM   = NDM-II*5
      IF (NUM .GE. 5) NUM = 5
      WRITE(IPRT, 102)((CHAR(N/10+48), CHAR(MOD(N,10)+48), CHAR(N/10+48), CHAR(MOD(N,10)+48)), N=II*5+1, II*5+5),
     &(ICON(M+2+II*10+N), N=1, NUM*2)
16    CONTINUE
      WRITE(IPRT, 105)(CON(J+N), N=0, 4)
      DO 17 II = 0, NDM/10-1,1
      NUM = NDM-II*10
      IF (NUM .GE. 10) NUM = 10
      WRITE(IPRT, 106)((CHAR(N/10+48), CHAR(MOD(N, 10)+48)), N=II*10+1, II*10+10), (CON(N), N=J+II*10+5, J+II*10+NUM+4)
17    CONTINUE
30    RETURN
21    WRITE(IPRT, 117) 0, 0, 8, 0, 2*NDM+3, 5+NDM, 2, 3+2*NDM, ICON(M), ICON(M+1), ICON(M+2)
      DO 18 II = 0, NDM/10,1
      NUM   = NDM*2-II*20
      IF (NUM .GE. 20) NUM = 20
      WRITE(IPRT, 118)(ICON(M+2+II*20+N), N=1 ,NUM)
18    CONTINUE
      WRITE(IPRT, 119) (CON(J+N), N=0, 4)
      DO 19 II = 0, NDM/10, 1
      NUM   = NDM-II*10
      IF (NUM .GE. 10) NUM = 10
      WRITE(IPRT, 120)(CON(J+II*10+4+N),N=1,NUM)
19    CONTINUE
      WRITE(IPRT, '(A)') '/'
      RETURN
100   FORMAT(//1X, '** AGC ** ICONS      CONS      STATES      VARS'/, 6X, 4(I6,'-',I4))
101   FORMAT(/5X, 'AGC  agcyc NDM  '/, 4X, I4, I7, I4)
102   FORMAT(/5X, 5('GEN', A, A, '|ID', A, A, '|')/, 4X, 5(I6, I5))
103   FORMAT(/5X, 'BUS NO.   BUS NAME  ID AAC  Status')
104   FORMAT(/5X, I7, 3X, A13, 6X, A4, 2X, F9.3, 3X, I2)
105   FORMAT(/8X, 'BF      Kp      Ki      Kd      Td'/, 2X, 5F8.3)
106   FORMAT(/6X, 10('AAC', A, A, ' |')/, 4X,10F7.2)
107   FORMAT(//' BUS', I7, '  MACHINE ', A, ':')
108   FORMAT(' BF=', F15.4)
109   FORMAT(' Kp=', F15.4)
110   FORMAT(' Ki=', F15.4)
111   FORMAT(' Kd=', F15.4)
112   FORMAT(' Td=', F15.4)
116   FORMAT(' AGC AT BUS', I7, ' MACHINE ', A, ' INITIALIZED OUT OF LIMITS')
117   FORMAT(I3, ' ''USRMDL''', 2X, I3, ' ''AGC''', 1X, 9I5)
118   FORMAT(10(I5, I3))
119   FORMAT(5(F8.3))
120   FORMAT(10(F8.3))
32722 CONTINUE
      IF(NEW) GO TO 32720
      NEW  = .TRUE.
      CALL DOCUHD(*30)
32720 GO TO I32722
      END
