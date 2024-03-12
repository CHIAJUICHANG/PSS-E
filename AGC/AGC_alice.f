C
C[AGC]         2018/01/10      AUTOMATIC GENERATION CONTROL MODEL
C
C  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
C  *  Designer: Sheng-Hui Lee garylee@uch.edu.tw                             *
C  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
      SUBROUTINE AGC(M,J,K,L)
C
C     PARAMETER
C     M: Integar
C     J: Real
C     K: state
C     L: variable
C
C        USE DYNAMICS, ONLY:  NUMTRM,   EFD,
C     *                          CON,   VAR,
C     *                        STATE,DSTATE,  STORE
C
$INSERT COMON4.INS

      INTEGER   J,      K,       L,       N,      JJ,        KK,        II,      IVEL
      INTEGER NDM,      I,     NUM,   agcyc,   IEAAC,AGC_status,       reg,      IERR
      REAL     BF,     Kp,      Ki,      Kd,      Td,      AACt,      VINP,      VOUT,  tmp
      REAL     df,     Yi,      Yd,      IN,     ACE,      DEL2,   Pregsys,       mul
      LOGICAL NEW
      INTEGER::    IM(42),IBUS(42),   ID(42), IB(42), ST(42),  IH(42)
      REAL::     Pmax(42),Preg(42),  AAC(42),  P(42), R(42),    H(42)
      CHARACTER(len=20):: GOVNAM,   GNAME  
      
      AGC_status=ICON(M)
      agcyc=ICON(M+1) ! cycle time of AGC
      NDM=ICON(M+2) ! number of units join AGC
      BF=CON(J) ! MW/0.1 Hz
      Kp=CON(J+1)
      Ki=CON(J+2)
      Kd=CON(J+3)
      Td=CON(J+4)
      AACt=0.0 ! ramp rate
      reg=2 ! 2 nothing 1 regulation up 0 down
      df=0.0

      DO 1 I = 1, NDM
      .  IBUS(I)=ICON(M+1+2*I)
      .  ID(I)=ICON(M+2*I+2)+48 ! 48 is ascii '0'
      .  CALL GENCHK (IBUS(I), CHAR(ID(I)), IM(I), 'GENCHK cannot find the specified machine')
      .  CALL MACINT(IBUS(I),CHAR(ID(I)), 'STATUS', ST(I), IERR)
      .  IB(I)=ABS(NUMTRM(IM(I)))
      .  df=df+BSFREQ(IB(I))
      .  CALL MDLNAM(IBUS(I),CHAR(ID(I)),'GOV', GOVNAM, IERR)
      .  GNAME = 'HYGOV'
      .  WHEN (GOVNAM.EQ.GNAME)
      .  .  CALL MDLIND(IBUS(I),CHAR(ID(I)),'GOV','CON',IVEL,IERR)
      .  .  R(I)=CON(IVEL)
      .  .  CALL MDLIND(IBUS(I),CHAR(ID(I)),'GOV','VAR',IH(I),IERR)
      .  ...FIN
      .  ELSE
      .  .  R(I)=0.0
      .  .  IH(I)=0
      .  ...FIN
      .  IF (GOVNAM.EQ.'WEHGOV')
      .  .  CALL MDLIND(IBUS(I),CHAR(ID(I)),'GOV','CON',IVEL,IERR)
      .  .  R(I)=(CON(IVEL)+0.0007)
      .  ...FIN
1     ...CONTINUE
      df=(BSFREQ(1910)+BSFREQ(2480)+BSFREQ(2650))*60.0/3.0
!      df=df*60.0/NDM

      CONDITIONAL
      .  (df.GE.0.03)
      .  .  reg=0 ! regulation down
      .  ...FIN
      .  (df.LE.-0.03)
      .  .  reg=1 ! regulation up
      .  ...FIN
      .  (OTHERWISE)
      .  .  reg=2
      .  ...FIN
      ...FIN

      DO 10 I = 1, NDM
      .  IBUS(I)=ICON(M+1+2*I)
      .  ID(I)=ICON(M+2*I+2)+48
      .  P(I)=PMECH(IM(I))*MBASE(IM(I))
!     .  .  P(I)=GREF(IM(I))*MBASE(IM(I))
      .  WHEN (reg.EQ.0) ! down
      .  .  AAC(I)=MAX(-CON(J+I+4)*agcyc/60000.0,-P(I))
      .  ...FIN
      .  ELSE ! up
      .  .  CALL MACDAT(IBUS(I),CHAR(ID(I)),'PMAX',Pmax(I),IEAAC)
!      .  .  CALL MACDAT(IBUS(I),CHAR(ID(I)),'MBASE',Pmax(I),IEAAC)
!      .  .  AAC(I)=MIN(CON(J+I+4)*agcyc/60000.0,MBASE(IM(I))-P(I))
      .  .  AAC(I)=MIN(CON(J+I+4)*agcyc/60000.0,Pmax(I)-P(I))
      .  ...FIN
      .  IF (IM(I).EQ.0) RETURN
      .  IF(TIME.LT.1) H(I)=1.0
      .  AACt=AACt+AAC(I)
10    ...CONTINUE
      ACE=-10.0*BF*df
      VAR(L)=ACE
C
C     MODE 8 - ASSIGN DESCRIPTIONS FOR DATA EDITOR
C
      IF (MODE.EQ.8)
      .  CON_DSCRPT(1) = 'STAT'
      .  CON_DSCRPT(2) = 'AGC cycle time'
      .  CON_DSCRPT(3) = 'NDM'
      ...RETURN                   ! GET DATA DESCRIPTIONS
      ...FIN
      IF (MODE.GT.4) GO TO 20
C
C     MODEL IMPLEMENTED FOR MSTR/MRUN (EXTENDED TERM SIMULATION)
C
      WHEN (MIDTRM)
      .  CONDITIONAL
      .  .  (INSITR)
      .  .  .  IN=VAR(L)
      .  .  .  IF (KPAUSE.EQ.2) IN=(IN+STORMT(2*K-1))*0.50
      .  .  .  Yi=Ki*DELT/2.0*IN+STORE(K)
      .  .  .  Yd=(IN*Kd+STORE(K+1))/(1.0+2.0*Td/DELT)
      .  .  ...FIN
      .  .  (MODE.EQ.1)
      .  .  .  IN=VAR(L)
      .  .  .  STORE(K)=0.0
      .  .  .  STORE(K+1)=IN*Kd
      .  .  ...FIN
C
C     MODE 2 - CALCULATE DERIVATIVES
C      
      .  .  (MODE.EQ.2)
      .  .  .  WHEN (KPAUSE.EQ.1)
      .  .  .  .  STORMT(2*K-1)=VAR(L)
      .  .  .  ...FIN
      .  .  .  ELSE
      .  .  .  .  IN=VAR(L)
      .  .  .  .  IF (KPAUSE.EQ.2) IN=(IN+STORMT(2*K-1))*0.50
      .  .  .  ...FIN
      .  .  .  Yi=Ki*DELT/2.0*IN+STORE(K)
      .  .  .  STORE(K)=Yi+IN*Ki*DELT/2.0
      .  .  .  Yd=(IN*Kd+STORE(K+1))/(1.0+2.0*Td/DELT)
      .  .  .  STORE(K+1)=IN*Kd-Yd*(1.0-2.0*Td/DELT)
      .  .  ...FIN
C
C     MODE 3 - SET EFD
C
      .  ...FIN
      .  RETURN 
      ...FIN
C
C     MODEL IMPLEMENTED FOR STR/RUN (STATE SPACE)
C
      ELSE
      .  CONDITIONAL
      .  .  (MODE.EQ.1)
      .  .  .  VOUT = 0.0
      .  .  .  VINP = PID_MODE1(Kp,Ki,Kd,Td,VOUT,K,K+1,IEAAC) 
      .  .  .  VAR(L)=VINP
      .  .  ...FIN               
C
C     MODE 2 - CALCULATE DERIVATIVES
C
      .  .  (MODE.EQ.2)
      .  .  .  VINP = VAR(L)
      .  .  .  VOUT = PID_MODE2(Kp,Ki,Kd,Td,VINP,K,K+1)
      .  .  .  VAR(L+1)=VOUT
      .  .  ...FIN       
C
C     MODE 3 - SET EFD
C
      .  .  (MODE.EQ.3)
      .  .  .  VINP = VAR(L+1)
      .  .  .  VOUT = PID_MODE3(Kp,Ki,Kd,Td,VINP,K,K+1)
      .  .  .  VAR(L)=VOUT
      .  .  .  Pregsys=VOUT
      .  .  .  tmp=0
      .  .  .  IF (MOD(INT((TIME)/0.001),agcyc) .LE. INT(DELT/0.001) .AND. reg.NE.2)      
      .  .  .  .  DO 14 I = 1, NDM
      .  .  .  .  .  IF ((AGC_status .EQ. 1) .AND. (abs(Pregsys) .LT. abs(AACt)))
      .  .  .  .  .  .  Preg(I)=Pregsys*AAC(I)/AACt
      .  .  .  .  .  .  mul=1
      .  .  .  .  .  .  IF (reg.EQ.1 .AND. (PMECH(IM(I))*MBASE(IM(I))).LT.Pmax(I)) ! up
!      .  .  .  .  .  .  .  GREF(IM(I))=PMECH(IM(I))+MIN(Preg(I),AAC(I))/MBASE(IM(I)) *H(I)/VAR(IH(I)+1)/VAR(IH(I)+1)
      .  .  .  .  .  .  .  IF (R(I).EQ.0.0) GREF(IM(I))=GREF(IM(I))+MIN(Preg(I),AAC(I))/MBASE(IM(I))
      .  .  .  .  .  .  .  IF (R(I).GT.0.0)
      .  .  .  .  .  .  .  .  IF (IH(I).GT.0) mul=VAR(IH(I)+1)*SQRT(VAR(IH(I)+1))/1.2
!      .  .  .  .  .  .  .  .  GREF(IM(I))=GREF(IM(I))+MIN(Preg(I),AAC(I))/MBASE(IM(I))/1.2/SQRT(VAR(IH(I)+1))*R(I)
      .  .  .  .  .  .  .  .  GREF(IM(I))=GREF(IM(I))+MIN(Preg(I),AAC(I))/MBASE(IM(I))*mul*R(I)
      .  .  .  .  .  .  .  ...FIN
      .  .  .  .  .  .  .  tmp=tmp+MIN(Preg(I),AAC(I))
      .  .  .  .  .  .  ...FIN
      .  .  .  .  .  .  IF (reg.EQ.0 .AND. (PMECH(IM(I))*MBASE(IM(I))).GT.0) ! down
!      .  .  .  .  .  .  .  GREF(IM(I))=MAX(0.0,PMECH(IM(I))+MAX(Preg(I),AAC(I))/MBASE(IM(I))) *H(I)/VAR(IH(I)+1)
      .  .  .  .  .  .  .  IF (R(I).EQ.0.0) GREF(IM(I))=MAX(0.0,GREF(IM(I))+MAX(Preg(I),AAC(I))/MBASE(IM(I)))
      .  .  .  .  .  .  .  IF (R(I).GT.0.0)
      .  .  .  .  .  .  .  .  IF (IH(I).GT.0) mul=VAR(IH(I)+1)*SQRT(VAR(IH(I)+1))/1.2
!      .  .  .  .  .  .  .  .  GREF(IM(I))=GREF(IM(I))+MAX(Preg(I),AAC(I))/MBASE(IM(I))/1.2/SQRT(VAR(IH(I)+1))*R(I)
      .  .  .  .  .  .  .  .  GREF(IM(I))=GREF(IM(I))+MAX(Preg(I),AAC(I))/MBASE(IM(I))*mul*R(I)
      .  .  .  .  .  .  ...FIN
      .  .  .  .  .  .  .  tmp=tmp+MAX(Preg(I),AAC(I))
      .  .  .  .  .  .  ...FIN
      .  .  .  .  .  ...FIN
      .  .  .  .  .  IF ((AGC_status .EQ. 1) .AND. (abs(Pregsys) .GE. abs(AACt)))
      .  .  .  .  .  .  IF (reg.EQ.1 .AND. (PMECH(IM(I))*MBASE(IM(I))).LT.Pmax(I)) ! up
!      .  .  .  .  .  .  .  GREF(IM(I))=PMECH(IM(I))+AAC(I)/MBASE(IM(I))
      .  .  .  .  .  .  .  IF (R(I).EQ.0.0) GREF(IM(I))=GREF(IM(I))+AAC(I)/MBASE(IM(I))
      .  .  .  .  .  .  .  IF (R(I).GT.0.0)
      .  .  .  .  .  .  .  .  IF (IH(I).GT.0) mul=VAR(IH(I)+1)*SQRT(VAR(IH(I)+1))/1.2
!      .  .  .  .  .  .  .  .  GREF(IM(I))=GREF(IM(I))+AAC(I)/MBASE(IM(I))/1.2/SQRT(VAR(IH(I)+1))*R(I)
      .  .  .  .  .  .  .  .  GREF(IM(I))=GREF(IM(I))+AAC(I)/MBASE(IM(I))*mul*R(I)
      .  .  .  .  .  .  ...FIN
      .  .  .  .  .  .  .  tmp=tmp+AAC(I)
      .  .  .  .  .  .  ...FIN
      .  .  .  .  .  .  IF (reg.EQ.0 .AND. (PMECH(IM(I))*MBASE(IM(I))).GT.0) ! down
!      .  .  .  .  .  .  .  GREF(IM(I))=MAX(0.0,PMECH(IM(I))+AAC(I)/MBASE(IM(I)))
      .  .  .  .  .  .  .  IF (R(I).EQ.0.0) GREF(IM(I))=MAX(0.0,GREF(IM(I))+AAC(I)/MBASE(IM(I)))
      .  .  .  .  .  .  .  IF (R(I).GT.0.0)
      .  .  .  .  .  .  .  .  IF (IH(I).GT.0) mul=VAR(IH(I)+1)*SQRT(VAR(IH(I)+1))/1.2
!      .  .  .  .  .  .  .  .  GREF(IM(I))=(MAX(0.08*R(I)*SQRT(VAR(IH(I)+1)),GREF(IM(I))+AAC(I)/MBASE(IM(I))/1.2/SQRT(VAR(IH(I)+1))*R(I)))
      .  .  .  .  .  .  .  .  GREF(IM(I))=GREF(IM(I))+AAC(I)/MBASE(IM(I))*mul*R(I)
      .  .  .  .  .  .  ...FIN
      .  .  .  .  .  .  .  tmp=tmp+AAC(I)
      .  .  .  .  .  .  ...FIN
      .  .  .  .  .  ...FIN
      .  .  .  .  .  H(I)=VAR(IH(I)+1)
14    .  .  .  .  ...CONTINUE
      .  .  .  .  VAR(L+2)=AACt
      .  .  .  ...FIN
      .  .  .  RETURN 
      .  .  ...FIN   
C
C     MODE 4 -SET NINTEG
C
      .  .  (MODE.EQ.4)
      .  .  .  NINTEG=MAX(NINTEG,K+1)
      .  .  ...FIN                   
      .  ...FIN
      .  RETURN                 
      ...FIN
C
C     MODE > 4
C
20    IF (MODE.EQ.6) GO TO 21
C
C     MODE 5 OR 7 - ACTIVITY DOCU
C
      IF (MODE.EQ.5)
      .  CALL DOCUHD(*30)
      .  GO TO 31
      ...FIN
C
C     DATA CHECKING CODE (upper and lower bound)
C
      NEW=.FALSE.
      DEL2=2.*DELT ! ?
      PRINT-HEADING
C
C     (DATA CHECKING PERFORMED FOR ALL CONS)
C
      UNLESS (NEW) RETURN
C
C     DATA TABULATION CODE
C
31    JJ=J+7
      KK=K+1
      WRITE(IPRT,100) M,M+2*NDM,J,J+4+NDM,K,K+1,L,L+2+NDM ! IPRT unit number
      WRITE(IPRT,101) ICON(M),ICON(M+1),ICON(M+2)
      WRITE(IPRT,103)
      DO 15 II = 1,NDM
      .  WRITE(IPRT,104) IBUS(II),BUSNAM(IB(II)),CHAR(ID(II)),abs(AAC(II)),ST(II)
15    ...CONTINUE                  
      DO 16 II = 0,NDM/5-1,1
      .  NUM=NDM-II*5
      .  IF (NUM .GE. 5) NUM=5
      .  WRITE(IPRT,102)((CHAR(N/10+48),CHAR(MOD(N,10)+48),CHAR(N/10+48),CHAR(MOD(N,10)+48)),N=II*5+1,II*5+5),
     &(ICON(M+2+II*10+N),N=1,NUM*2)

16    ...CONTINUE      
      WRITE(IPRT,105) (CON(J+N),N=0,4)

      DO 17 II = 0,NDM/10-1,1
      .  NUM=NDM-II*10
      .  IF (NUM .GE. 10) NUM=10
      .  WRITE(IPRT,106) ((CHAR(N/10+48),CHAR(MOD(N,10)+48)),N=II*10+1,II*10+10),(CON(N),N=J+II*10+5,J+II*10+NUM+4)
17    ...CONTINUE
30    RETURN
C
C     MODE 6 - ACTIVITY DYDA
C
21    WRITE(IPRT,117) 0,0,8,0,2*NDM+3,5+NDM,2,3+NDM,ICON(M),ICON(M+1),ICON(M+2)
      DO 18 II = 0,NDM/10,1
      .  NUM=NDM*2-II*20
      .  IF (NUM .GE. 20) NUM=20
      .  WRITE(IPRT,118) (ICON(M+2+II*20+N),N=1,NUM)
18    ...CONTINUE
      WRITE(IPRT,119) (CON(J+N),N=0,4)
      DO 19 II = 0,NDM/10,1
      .  NUM=NDM-II*10
      .  IF (NUM .GE. 10) NUM=10
      .  WRITE(IPRT,120) (CON(J+II*10+4+N),N=1,NUM)
19    ...CONTINUE
      WRITE(IPRT,'(A)') '/' 
      RETURN
100   FORMAT(//1X,'** AGC ** ICONS      CONS      STATES      VARS'/, 6X,4(I6,'-',I4))
101   FORMAT(/5X,'AGC  agcyc NDM  '/,4X,I4,I7,I4)
102   FORMAT(/5X,5('GEN',A,A,'|ID',A,A,'|')/,4X,5(I6,I5))
103   FORMAT(/5X, 'BUS NO.   BUS NAME  ID AAC  Status')
104   FORMAT(/5X,I7,3X,A13,6X,A4,2X,F9.3,3X,I2)
105   FORMAT(/8X,'BF      Kp      Ki      Kd      Td'/,2X,5F8.3)
106   FORMAT(/6X,10('AAC',A,A,' |')/,4X,10F7.2)     
107   FORMAT(//' BUS',I7,'  MACHINE ',A,':')
C
C     DOCU CHECKING MESSAGES
C
108   FORMAT(' BF=',F15.4)
109   FORMAT(' Kp=',F15.4)
110   FORMAT(' Ki=',F15.4)
111   FORMAT(' Kd=',F15.4)
112   FORMAT(' Td=',F15.4)
116   FORMAT(' AGC AT BUS',I7,' MACHINE ',A,       ' INITIALIZED OUT OF LIMITS')
C
C     a code portion for DYDA record
C
117   FORMAT(I3,' ''USRMDL''',2X,I3,' ''AGC''',1X,9I5)
118   FORMAT(10(I5,I3))
119   FORMAT(5(F8.3))
120   FORMAT(10(F8.3))
      TO PRINT-HEADING ! internal procedure
      .  UNLESS (NEW)
      .  .  NEW=.TRUE.
      .  .  CALL DOCUHD(*30)
      .  ...FIN
      ...FIN
      END
(FLECS Version 22.60 - PTI)
----------------------------------------
