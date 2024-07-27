# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 19:41:38 2022

@author: Test-PC
"""

from netpyne import specs, sim
from joblib import Parallel, delayed
import multiprocessing
# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

L23e = {'secs': {}}

L23e['secs']['soma'] = {'geom': {}, 'mechs': {}}
L23e['secs']['soma']['geom'] = {'diam': 96, 'L': 96, 'Ra': 100, 'cm': 1, 'nseg' : 1}
L23e['secs']['soma']['mechs']['pas'] = {'e':-70,'g':0.0001} 
L23e['secs']['soma']['mechs']['hh2'] = {'gnabar': 0.05, 'gkbar': 0.005, 'vtraub':-55 }
L23e['secs']['soma']['mechs']['im'] = {'gkbar':7e-5} 

netParams.cellParams['PYR'] = L23e


## Population parameters
netParams.popParams['S'] = {'cellType': 'PYR', 'numCells': 1}
netParams.popParams['M'] = {'cellType': 'PYR', 'numCells': 1}

## Synaptic mechanism parameters
###############################################################################  Synaptic mechanism parameters
netParams.synMechParams['STD']   = {'mod': 'FDSExp2Syn'}                         # STD synaptic mechanism   
###############################################################################
delay_after_stim=111000
for t in (500-delay_after_stim,1000 ):
    delay=delay_after_stim+t
    Input_A='Plast_test'+ str(t)
    Target_A='Plast_test'+ str(t)+'->S'
    amplitude= 75 #np.random.uniform(1,1.3,1)
    netParams.stimSourceParams[Input_A] = {'type': 'IClamp',  'del': delay, 'dur': 0.1 , 'amp':amplitude}  
    netParams.stimTargetParams[Target_A] = {'source': Input_A, 'sec':'soma', 'loc': 0.5,'conds': {'pop':['S']}}        
###############################################################################
###############################################################################

STDPparams = {'STDPon':1, 'hebbwt': 0.001, 'antiwt':-0.001, 'wmax': 50, 'RLon': 0 ,'tauhebb': 10, 'RLwindhebb': 0, 'useRLexp': 0, 'softthresh': 0, 'verbose':0}
# Cell connectivity rules
netParams.connParams['S->M'] = {'preConds': {'pop': 'S'}, 'postConds': {'pop': ['M']},  #  S -> M
    'probability': 1,           # probability of connection
    'weight': 0.05,             # synaptic weight
    'delay': 1,                 # transmission delay (ms)
    'sec': 'soma',              # section to connect to
    'loc': 1.0,                 # location of synapse
    'plast': {'mech': 'STDP', 'params': STDPparams},
    'synMech': 'STD'}           # target synaptic mechanism
###############################################################################
# Simulation options
simConfig = specs.SimConfig()       # object of class SimConfig to store simulation configuration

simConfig.duration = 113*1e3        # Duration of the simulation, in ms  #72*1e3
simConfig.dt = 0.025                # Internal integration timestep to use
simConfig.verbose = True            # Show detailed messages
simConfig.saveCellConns = True
simConfig.recordTraces = {
                          'V_soma':  {'sec': 'soma', 'loc': 0.9, 'var':'v'},
                          'g_STD':   {'sec': 'soma', 'loc': 1.0, 'synMech': 'STD', 'var': 'g'}
                          }
simConfig.hParams = {'celsius': 37, 'v_init': -65.0, 'clamp_resist': 0.001}

simConfig.recordStep = 0.05         # Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'test'         # Set file output name
simConfig.savePickle = False        # Save params, network and sim output to pickle file

# simConfig.analysis['plotRaster'] = {'saveFig': True}                    # Plot a raster
simConfig.analysis['plotTraces'] = {'include': [0,1], 'saveFig': True}  # Plot recorded traces for this list of cells
# simConfig.analysis['plot2Dnet'] = {'saveFig': True}                     # plot 2D cell positions and connections
# simConfig.analysis['plotConn']={'includePre':'S','includePost':'M','feature':'weight', 'saveFig': True }

###############################################################################
###############################################################################

threshold=60.00     
for amplitude1 in range (99,160,4):
    def Simulation(amplitude2):
        simConfig.filename='imTBS-pre-'+str(amplitude1)+'post-'+str(amplitude2)
        start_time=1000
        for ttt in range (0,110000,15000):
            for tt in range(0,5000,200):
                for t in range(0,50,20):
                    delay=start_time+t+tt+ttt    
                    Input_PreSy='Input_PreSy'+ str(ttt)+ str(tt)+str(t) 
                    Input_PostSy='Input_PostSy'+ str(ttt)+ str(tt)+str(t)
                    Target_PreSy='Input_PreSy'+ str(ttt)+str(tt)+str(t)+'->S'
                    Target_PostSy='Input_PostSy'+ str(ttt)+str(tt)+str(t)+'->S'
        
                    netParams.stimSourceParams[Input_PreSy] =    {'type': 'IClamp',  'del': delay, 'dur': 0.1 , 'amp':threshold*amplitude1/100} 
                    netParams.stimSourceParams[Input_PostSy] = {'type': 'IClamp',  'del': delay, 'dur': 0.1 , 'amp':threshold*amplitude2/100}
         
                    netParams.stimTargetParams[Target_PreSy] = {'source': Input_PreSy, 'sec':'soma', 'loc': 0.5,'conds': {'pop':['S']}} 
                    netParams.stimTargetParams[Target_PostSy] = {'source': Input_PostSy, 'sec':'soma', 'loc': 0.5,'conds': {'pop':['M']}} 
        sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)
    num_cores = multiprocessing.cpu_count()-1
    
    ModelOutput=Parallel(n_jobs=num_cores)(delayed(Simulation)(amplitude2) for amplitude2 in range (40,150,4)) 
        


