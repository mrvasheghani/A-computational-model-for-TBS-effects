# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 16:52:46 2022

@author: Test-PC
"""

###############################################################################
import math
import matplotlib.pyplot as plt
Data=[]
Stim_Times=[]
Time = range (1,12000,1)
###############################################################################
COUNT=0
start_time=10
for sss in range (0,10000,10000):
    for ss in range(0,200,200):
        for s in range(0,20,20):
            delay=start_time+s+ss+sss
            Stim_Times.append(delay)

###############################################################################
for tau_D2 in [5200,7200,9200,11200, 13200]:
    f = 0.917 ; tau_F = 94 ;  d1 = 0.416  ; d2 = 0.975 ; tau_D1 = 380 
    F0 = 1; D01 = 1; D02 = 1; t=0; tsyn = t ; variable  =[]
    for t in Time:
        F  = 1 + (F0-1) * math.exp(-(t - tsyn)/tau_F)
        D1 = 1 - (1-D01)* math.exp(-(t - tsyn)/tau_D1)
        D2 = 1 - (1-D02)* math.exp(-(t - tsyn)/tau_D2) 
        if t in Stim_Times :
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
###############################################################################
plt.figure()   
plt.rcParams['font.size'] = '10'
plt.plot(Time, Data[0], label = "Tau_D2=5200")
plt.plot(Time, Data[1], label = "Tau_D2=7200")
plt.plot(Time, Data[2], label = "Tau_D2=9200")
plt.plot(Time, Data[3], label = "Tau_D2=11200")
plt.plot(Time, Data[4], label = "Tau_D2=13200")
plt.legend()
plt.xlabel('Time (ms)')
plt.ylabel('synapse conductivity')
plt.title('STP sensitivity for Tau_D2')
plt.savefig('STP sensitivity for Tau_D2-Default parameters.png',dpi=300)
