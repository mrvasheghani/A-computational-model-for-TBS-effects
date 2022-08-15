# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 16:52:46 2022

@author: Test-PC
"""
###############################################################################  Defult parameters

import math
import matplotlib.pyplot as plt
Data=[]
Stim_Times_iTBS=[]
Stim_Times_cTBS=[]
Stim_Times_50Hz=[]
Time = range (1,22000,1)
###############################################################################
COUNT=0
start_time=2
for sss in range (0,10000,10000):
    for ss in range(0,40000,200):
        for s in range(0,50,20):
            delay=start_time+s+ss+sss
            Stim_Times_cTBS.append(delay)

###############################################################################
for tau_D1 in [380]:
    f = 0.917 ; tau_F = 94 ;  d1 = 0.416  ; d2 = 0.975 ; tau_D2 = 9200 
    F0 = 1; D01 = 1; D02 = 1; t=0; tsyn = t ; variable  =[]
    for t in Time:
        F  = 1 + (F0-1) * math.exp(-(t - tsyn)/tau_F)
        D1 = 1 - (1-D01)* math.exp(-(t - tsyn)/tau_D1)
        D2 = 1 - (1-D02)* math.exp(-(t - tsyn)/tau_D2) 
        if t in Stim_Times_cTBS :
            tsyn=t
            F0=F
            D01=D1
            D02=D2
            F0=F0+f
            D01=D01*d1
            D02=D02*d2
        A=F*D1*D2
        variable.append(A)
    Data.append(variable)
# #############################################################################
###############################################################################
COUNT=0
start_time=5
for sss in range (0,200000,10000):
    for ss in range(0,2000,200):
        for s in range(0,50,20):
            delay=start_time+s+ss+sss
            Stim_Times_iTBS.append(delay)

###############################################################################
for tau_D1 in [380]:
    f = 0.917 ; tau_F = 94 ;  d1 = 0.416  ; d2 = 0.975 ; tau_D2 = 9200 
    F0 = 1; D01 = 1; D02 = 1; t=0; tsyn = t ; variable  =[]
    for t in Time:
        F  = 1 + (F0-1) * math.exp(-(t - tsyn)/tau_F)
        D1 = 1 - (1-D01)* math.exp(-(t - tsyn)/tau_D1)
        D2 = 1 - (1-D02)* math.exp(-(t - tsyn)/tau_D2) 
        if t in Stim_Times_iTBS :
            tsyn=t
            F0=F
            D01=D1
            D02=D2
            F0=F0+f
            D01=D01*d1
            D02=D02*d2
        A=F*D1*D2
        variable.append(A)
    Data.append(variable)

###############################################################################
plt.figure()   
plt.rcParams['font.size'] = '10'
# plt.plot(Time, Data[2], label = "50 Hz", linewidth=1,color='red')
# plt.plot(Time, Data[2], label = "50 Hz", linewidth=1,color='red')
plt.plot(Time, Data[0], label = "cTBS",linewidth=1) #, color='red')
plt.plot(Time, Data[1], label = "iTBS",linewidth=1) #, color='blue')
plt.ylim([0, 1.05])
plt.legend()
plt.legend(loc='upper right')
plt.xlabel('Time (ms)')
plt.ylabel('synapse conductivity')
plt.title('STP dynamic for cTBS and iTBS')
plt.savefig('STP dynamic for cTBS and iTBS.png',dpi=300)