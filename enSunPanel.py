import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft, integrate
from varname import argname
import enModule
import enFunctions as ef
import enProject as fromAnalysis


##### THEORETICAL ESTIMATION OF POWER GENERATED BY MY PANELS FROM 16-25/12/22
# 
# meanPowerProjected = normalMeanPanPower*cos(θ)
#  where:
# - normalMeanPanPower = 1 kW/m^2 * 20 panels * 1,64 m^2 * 18,65% (efficiency)
#
# - cos(θ) = cos(β)*cos(Ψ – Ψs)*sin(χ) + sin(β)*cos(χ)
#  - β = elevation (from csv prod. by https://www.sunearthtools.com/dp/tools/pos_sun.php)
#  - Ψ = azimut (from csv prod. by https://www.sunearthtools.com/dp/tools/pos_sun.php)
#  - Ψs = azimut angle (10°) --> angle of panel orientation
#  - χ = tilt panels' angle (18°)

tab = pd.read_csv('december/posSun20dec.csv', encoding= 'unicode_escape')
elevation = tab['ora'].values
azimut = (tab['Elevazione'].values)-180 # Sud --> 0°
time1 = np.arange(0, 1440, 5)
time10 = np.arange(0, 14400, 5)

# degrees to radiants conversion
elevation = ef.degRad(elevation)
azimut = ef.degRad(azimut)
tilt = ef.degRad(18)
azimutAngle = ef.degRad(10)

# projection coefficient
cosTheta = np.cos(elevation)*np.cos(azimut-azimutAngle)*np.sin(tilt) + np.sin(elevation)*np.cos(tilt)
cosTheta = np.append(np.zeros(93),cosTheta)#=0 before sunshine(7:50-> 470min-> 470/5=94 index)
cosTheta = np.append(cosTheta,np.zeros(90))# and after sunset(16:30-> 990min-> 990/5=198 index->
# -> I want 288 salmples per day=> append 90 zeros)

# Normalized mean panels' power and Mean panels' power
normMeanPanPower = 20*1.64*18.65/100
meanPanPower = normMeanPanPower*cosTheta

if True: # one day theoretical plot
    plt.plot(time1/60, meanPanPower, '.')
    plt.title('Theorical panels power with 20dec2022\'s \n elevation and azimut')
    plt.ylabel('Panels power (kW)')
    plt.xlabel('hours')
    plt.xticks(np.arange(0, 25, 3))
    plt.text(0, 0.1, f'panPower = normMeanPanPower*cos(θ)\n normPanPower = {round(normMeanPanPower,4)}\n cos(θ) = cos(β)*cos(Ψ–Ψs)*sin(χ) + sin(β)*cos(χ)')
    plt.savefig('cosTheta.png')
    plt.show()

mPanPwr = np.array([]) # 10 days array for theorical data
for i in range(10):
    mPanPwr = np.append(mPanPwr, meanPanPower) 

## 10 days theoretical plot and some difference functions between theor. & sperimental data
if True: 
    fig, ax = plt.subplots(3,1, figsize=(15,13))
    ax[0].plot(time10/60, mPanPwr, '-', color='coral', label='theorical sunny day $(1kW/m^2)$', linewidth=3)
    ax[0].plot(time10/60, mPanPwr/2, '-', color='lightseagreen', label='theorical partly cloudy day $(0.5kW/m^2)$', linewidth=1.7)
    ax[0].plot(time10/60, mPanPwr/4, '-', color='darkgoldenrod', label='theorical cloudy day $(0.25kW/m^2)$')
    ax[0].set_ylabel('PanPower(kW)$= normPanPower*cos(\\theta)$')
    ax[0].set_xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    ax[0].set_xticks( ticks=np.arange(0,240,6), labels=np.resize(np.arange(0,24,6),4*10) )
    ax[0].legend()
    fig.suptitle('10 days of theorical panels power (16-25/12/2022) compared with sperimental one')

    ax[1].plot(time10/60, fromAnalysis.aSampPanel[4320:], '-', color='darkred', label='sperimental data')
    ax[1].legend()
    ax[1].plot(time10/60, mPanPwr, '-', color='coral', alpha=0.8)
    ax[1].plot(time10/60, mPanPwr/2, '-', color='lightseagreen', alpha=0.8)
    ax[1].plot(time10/60, mPanPwr/4, '-', color='darkgoldenrod', alpha=0.8)
    ax[1].set_ylabel('Panels Power(kW)')
    ax[1].set_xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    ax[1].set_xticks( ticks=np.arange(0,240,6), labels=np.resize(np.arange(0,24,6),4*10) )

    diff = mPanPwr - fromAnalysis.aSampPanel[4320:]
    diff2 = mPanPwr/2 - fromAnalysis.aSampPanel[4320:]
    diff4 = mPanPwr/4 - fromAnalysis.aSampPanel[4320:]
    ax[2].plot(time10/60, diff, '-', color='blueviolet', label='difference bw theor & sper')
    ax[2].plot(time10/60, diff2, '-', color='springgreen', label='difference bw theor/2 & sper')
    ax[2].plot(time10/60, diff4, '-', color='orange', label='difference bw theor/4 & sper')
    ax[2].legend()
    ax[2].set_ylabel('Panels Power(kW)')
    ax[2].set_xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    ax[2].set_xticks( ticks=np.arange(0,240,6), labels=np.resize(np.arange(0,24,6),4*10) )

    for y in range(3): 
        for i in range(11): # day separator 
            ax[y].axvline(x=i*24, color='lightgrey')
    plt.savefig('theoricalPlot.png')
    plt.show()


### FFT difference between theor. (mPanPwr/4 --> cloudy day) & sper. data
if True:
    diff4TheorSperDiffPan = np.concatenate((np.zeros(4320), diff4)) #add 4320 zeros to reuse the function
    ftDiffPan, miDiffPanFreq = ef.fft10Days(diff4TheorSperDiffPan) # ef.fft10Days already def
    ftmask = np.absolute(ftDiffPan)**2 < 12e3
    ftmask1 = np.absolute(ftDiffPan)**2 < 5e2
    ftDiffPanFiltr = ftDiffPan.copy()
    ftDiffPanFiltr[ftmask] = 0 # Inverse FFT with filtred coeff
    filtredDiffPan = fft.irfft(ftDiffPanFiltr, n=len(diff4))
    ftDiffPanFiltr1 = ftDiffPan.copy()
    ftDiffPanFiltr1[ftmask1] = 0 # Inverse FFT with filtred coeff
    filtredDiffPan1 = fft.irfft(ftDiffPanFiltr1, n=len(diff4))
    filtredOffset = fft.irfft(np.concatenate(([ftDiffPan[0]], np.zeros(len(ftDiffPan)-1))), n=len(diff4) ) # Inverse FFt with only offset
    
    plt.figure(figsize=(15,6))
    plt.plot(time10/60, diff4, '-', label='difference bw theor/4 & sper', c='gold', linewidth=3)
    plt.plot(time10/60, filtredDiffPan, color='darkviolet', label='Filtro $coeff>1,2\cdot 10^4$') # 7 most important freq
    plt.plot(time10/60, filtredDiffPan1, color='aqua', label='Filtro $coeff>1\cdot 10^5$') # some more freq
    plt.plot(time10/60, filtredOffset, color='darkorange', label=f'Offset = {round(0.001*np.real(ftDiffPan[0]),3)} kW') # offset (only freq[0])
    ef.daySeparatorLine('lightgrey')
    plt.legend()
    plt.title('16-25 December\'s difference plot and filtred plot')
    plt.ylabel('Power (kW)')
    plt.xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    plt.xticks( ticks = np.arange(0, 240, 6), labels = np.resize(np.arange(0, 24, 6),4*10) )
    plt.yticks(np.arange(min(diff4),max(diff4),1))
    #diff function integer
    iDiff = (round(integrate.simpson(diff4, time10), 2))/60 # divided by 60 cause i want the energy in kWh, not kWmin
    plt.text(0, 1, f'7 most important freq = {np.round(miDiffPanFreq,7)} Hz\n difference\'s integral = {iDiff} kWh') 
    plt.savefig('filtredDiff.png')
    plt.show()
