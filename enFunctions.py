import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft, integrate
from varname import argname
import enModule

# FUNCTIONS MADE FOR ENERGY CONSUMPTION ANALYSIS USED IN 'enProject.py' and 'enSunPanel.py'

def arraySamp(tab): # return an array of Sample object def in enModule
    aa = np.empty(0)
    time = tab['Data ora']
    home = tab['Casa (kW)'].values
    panel = tab['Fotovoltaico (kW)'].values
    pwall = tab['Powerwall (kW)'].values
    net = tab['Rete (kW)'].values
    for i in range(len(time)):
        aa = np.append(aa, np.array([enModule.Sample(time[i], home[i], panel[i], pwall[i], net[i]) ])) # time + 4 categories sampled
    return aa

def arrayDay(aSamp): # return an array of day sampled (Month object) def in enModule
    aDay = np.array( [enModule.Month()] )
    threshold = 288 #Samples' number per day
    freq = 5 #min
    for i in range(len(aSamp)):
        aDay[-1].addSamp(aSamp[i])        
        if ( ((aSamp[i].time/freq) == (threshold-1)) & (i != (len(aSamp)-1)) ):
            aDay = np.append(aDay, enModule.Month())
    return aDay

def daySeparatorLine(color):#make day separator lines for 10-days' plots
    labeLine = 'day separator'
    for i in range(11):
        plt.axvline(x=i*24, color=color, label=labeLine)
        labeLine = "_nolegend_" #not repeat day separator line's label

def fft10Days(aSampX): # make spectral power plots of a category sampled and return Fourier coefficient and the 7 freq with larger spectrum power
    ftX = fft.rfft(aSampX[4320:])
    dt = 60*5 # sample spacing = 5 minutes
    nq = 0.5
    ftXF = nq*fft.rfftfreq(ftX.size, dt)

    figg,axx = plt.subplots(1, 2, figsize = (10,5))
    # power spectrum on frequencies
    axx[0].plot(ftXF[:len(ftX)//2], np.absolute(ftX[:len(ftX)//2])**2, 'o', markersize=4, label='spectrum($\\nu$)')

    # index of frequencies with the largest spectral power
    listmax = list(np.absolute(ftX[:len(ftX)//2])**2)

    aPot = np.absolute(ftX[:len(ftX)//2])**2
    potSort = -np.sort(-aPot)#array of power sorted (decreasing order)
    potInd = np.array([], dtype=int)
    for p in potSort:
        potInd = np.append(potInd, listmax.index(p)) #array of sorted index
    
    name = argname('aSampX') #name of category analyzed
    print(f'{name} most important freq:\n index: ', potInd[0:7], '\n freq: ',ftXF[potInd[0:7]], '\n')
    axx[0].axvline(ftXF[potInd[0]], color='red', label='1° freq')
    axx[0].axvline(ftXF[potInd[1]], color='orange', label='2° freq')
    axx[0].axvline(ftXF[potInd[2]], color='gold', label='3° freq')
    axx[0].set_xlabel('Frequencies $(Hz)$')
    axx[0].set_ylabel('$|c_k|^2$')
    axx[0].set_yscale('log')
    axx[0].legend(fontsize='small', loc=3) #lower left
    #insertion of the 3 most important freq
    ins = axx[0].inset_axes([0.64, 0.58, 0.3,0.36])
    ins.axvline(ftXF[potInd[0]], color='red', linewidth=2)
    ins.axvline(ftXF[potInd[1]], color='orange', linewidth=2)
    ins.axvline(ftXF[potInd[2]], color='gold', linewidth=2)
    ins.plot(ftXF[:len(ftX)//2], np.absolute(ftX[:len(ftX)//2])**2, 'o', markersize=4)
    ins.set_xlim(-0.0000025,0.000025)
    ins.set_yscale('log')

    #power spectrum on periods and noise identification
    offset = 0.1 #offset of pink noise
    if (name[5]=='N') or (name[5]=='H'):
        offset = 1
    axx[1].plot(1/ftXF[1:len(ftX)//2], np.absolute(ftX[1:len(ftX)//2])**2, 'o', markersize=4, label='spectrum($T$)')
    axx[1].plot(1/ftXF[1:len(ftX)//2], (1/ftXF[1:len(ftX)//2])*offset, '-', c='hotpink', label='pink noise $\propto(1/f)$') #pink noise =>increase as T
    axx[1].plot(1/ftXF[1:len(ftX)//2], ((1/ftXF[1:len(ftX)//2])**2)*0.00001, '-', c='brown', label='brown noise $\propto(1/f^2)$') #brown noise => increase as T^2
    axx[1].set_xlabel('Periods $(s)$')
    axx[1].set_ylabel(r'$|c_k|^2$')
    axx[1].set_xscale('log')
    axx[1].set_yscale('log')
    axx[1].legend()

    x = (f'{name}')[5:]
    figg.suptitle(f'{x} Power spectrum on frequencies $\\nu$ and periods $T$', fontsize = 15)
    plt.savefig(f'spectrumTest{x}.png')
    plt.show()

    return ftX, ftXF[potInd[0:7]]

# return 4 ifft of a category filtred with masks passed as parameters
def ifft10Days(ftX, aPanel, ftmask, ftmask1, ftmask2, ftmaskC): 
    ftXFiltred = ftX.copy()
    ftXFiltred[ftmask] = 0
    ftXFiltred1 = ftX.copy()
    ftXFiltred1[ftmask1] = 0
    ftXFiltred2 = ftX.copy()
    ftXFiltred2[ftmask2] = 0
    ftXFiltredC = ftX.copy()
    ftXFiltredC[ftmaskC] = 0
    # Inverse FFT with filtred coeff
    filteredX  = fft.irfft(ftXFiltred,  n=len(aPanel))
    filteredX1 = fft.irfft(ftXFiltred1, n=len(aPanel))
    filteredX2 = fft.irfft(ftXFiltred2, n=len(aPanel))
    compareX = fft.irfft(ftXFiltredC, n=len(aPanel))
    return filteredX, filteredX1, filteredX2, compareX


def power4Day(iX): #return an array of daily power absorption starting from the power progress of 10 days for a category
    aPowerX = np.zeros(10)
    for a in range(1, 11):
        aPowerX[a-1] = round((iX[(a*288)-1]-iX[((a-1)*288)]),2)
    return aPowerX

def degRad(deg): #return the radiant value of the degrees angle in input
    return (deg*np.pi/180)
