import os,sys
sys.path.append("modules")
import inertia_function
SAV=r"C:\Program Files\114\savfile\114p.sav"
SNP=r"C:\Program Files\114\snpfile\114p.snp"
print(inertia_function.Gen_Inertia( SAV, SNP))
print(inertia_function.Total_Inertia( SAV, SNP))
print(inertia_function.Gen_S( SAV, SNP))
print(inertia_function.Total_S( SAV, SNP))
print(inertia_function.Gen_R( SAV, SNP))
print(inertia_function.Total_R( SAV, SNP))
print(inertia_function.Gov_R( SAV, SNP))
print(inertia_function.Gov_R_modify( SAV, SNP))