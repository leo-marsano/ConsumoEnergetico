import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft, integrate
from varname import argname
import enModule
import enFunctions as ef

    
#### DECEMBER ENERGY CONSUMPTION ANALYSIS
aSample = np.empty(0)
for i in range(25):#number of days' sampled in 'december' directory
    aSample = np.append(aSample, ef.arraySamp(pd.read_csv('december/{0}-12'.format(i+1)) ))
aDay = ef.arrayDay(aSample)
print(len(aDay), 'days sampled with ', aDay[0].nSamp, ' samples')

aSampTime = np.array([s.time for s in aSample])
aSampHome = np.array([s.home for s in aSample])
aSampPanel = np.array([s.panels for s in aSample])
aSampPwall = np.array([s.powerwall for s in aSample])
aSampNet = np.array([s.net for s in aSample])
print('total samples: ', len(aSampPwall))


### Print & Plots of all days sampled (1-25 dec)
if False:## Not required: let it 'False'
    '''
    print(aSampTime,'\n',aSampHome,'\n',aSampPanel,'\n',aSampPwall,'\n',aSampNet)
    for i in range(len(aSample)):
        print(aSample[i])
    '''
    for nd in range(1,26):     #nd = day's number
        aTime = np.array([s.time for s in aDay[nd-1].aSamp])
        aHome = np.array([s.home for s in aDay[nd-1].aSamp])
        aPanel = np.array([s.panels for s in aDay[nd-1].aSamp])
        aPwall = np.array([s.powerwall for s in aDay[nd-1].aSamp])
        aNet = np.array([s.net for s in aDay[nd-1].aSamp])
        plt.figure(figsize=[12, 8])
        plt.plot(aTime/60, aPanel, '-', label='panels', c='gold', linewidth=5)
        plt.plot(aTime/60, aPwall, '-', label='powerwall', c='green', alpha=0.4, linewidth=3)
        plt.plot(aTime/60, aHome, '-', label='home', c='red', alpha=0.5)
        plt.plot(aTime/60, aNet, '-', label='net', c='blue', alpha=0.3)
        plt.legend()
        plt.title(f'{nd} December')
        plt.ylabel('Power (kW)')
        plt.xlabel('Time (hours)')
        plt.xticks(np.arange(min(aTime/60), max(aTime/60)+1, 1.0))
        plt.yticks(np.arange(-3, 6, 0.5))
        plt.savefig('ploTest.png')
        plt.show()

### Subplots for 16-25 december comparing
if True:
    fig, ax = plt.subplots(5 ,2 , figsize=(12, 15))
    y = 0
    for nd in range(16, 26):
        aTime = np.empty(0)
        aHome = np.empty(0)
        aPanel = np.empty(0)
        aPwall = np.empty(0)
        aNet = np.empty(0)
        aTime = np.array([s.time for s in aDay[nd-1].aSamp])
        aHome = np.array([s.home for s in aDay[nd-1].aSamp])
        aPanel = np.array([s.panels for s in aDay[nd-1].aSamp])
        aPwall = np.array([s.powerwall for s in aDay[nd-1].aSamp])
        aNet = np.array([s.net for s in aDay[nd-1].aSamp])
        #axes coordinates    
        x = nd-16
        if (x%2==0 and x>0):
            y += 1
            x = 0
        if (x%2==1):
            x = 1
                
        ax[y,x].plot(aTime/60, aPanel, '-', label='panels', c='gold', linewidth=5)
        ax[y,x].plot(aTime/60, aPwall, '-', label='powerwall', c='green', alpha=0.4, linewidth=3)
        ax[y,x].plot(aTime/60, aHome, '-', label='home', c='red', alpha=0.5)
        ax[y,x].plot(aTime/60, aNet, '-', label='net', c='blue', alpha=0.3)
        ax[y,x].tick_params(direction='in')
        ax[y,x].set_title(f'        {nd} Dec', y=1.0, loc='center', pad=-10)
        ax[y,x].set_ylabel('Power (kW)')
        if (y==4):
            ax[y,x].set_xlabel('Time (hours)')
        ax[y,x].set_xticks((np.arange(min(aTime/60), max(aTime/60)+1, 3.0)))
        ax[y,x].set_yticks(np.arange(-2, max(max(aHome), max(aNet)), 1.0))
    fig.suptitle('Powers from 16 to 25 December\'s plots')
    fig.legend(['panels', 'powerwall', 'home', 'net'], loc="upper right")
    plt.savefig('compareSubplot.png')
    plt.show()

    
# CONSIDERING ONLY 10 DAY
# built a proper time array for a 10 day span plot: index from 4320 onwards to
time10 = np.empty(len(aSampTime[4320:]), dtype = int) # consider only 16-25 Dec
time10[0] = 0
for i in range(len(aSampTime[4320:])-1):
    time10[i+1] = time10[i] + 5
#print(time10)

### Plot about 10 day span's energy consumption
if True: 
    plt.figure(figsize=[45, 5])
    plt.plot(time10/60, aSampPanel[4320:], '-', label='panels', c='gold', linewidth=5)
    plt.plot(time10/60, aSampPwall[4320:], '-', label='powerwall', c='green', alpha=0.4, linewidth=3)
    plt.plot(time10/60, aSampHome[4320:], '-', label='home', c='red', alpha=0.5)
    plt.plot(time10/60, aSampNet[4320:], '-', label='net', c='blue', alpha=0.3)

    ef.daySeparatorLine('lightgrey')
    plt.title('16-25 December\'s energy consumption')
    plt.ylabel('Power (kW)')
    plt.xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    plt.xticks( ticks = np.arange(0, 240, 6), labels = np.resize(np.arange(0, 24, 6),4*10) ) # loop ticks (one every 6 hours)
    plt.yticks(np.arange(-2,max(max(aSampHome[4320:]),max(aSampNet[4320:])),1)) # find the ticks' max between the 2 most energy-intensive category
    plt.legend()
    plt.savefig('energy10daySpan.png')
    plt.show()

    
### FFT, SPECTRUM PLOTS AND FILTRED PLOTS
if True:
    ftPanel, miPanelFreq = ef.fft10Days(aSampPanel)
    ftPwall, miPwallFreq = ef.fft10Days(aSampPwall)
    ftHome, miHomeFreq = ef.fft10Days(aSampHome)
    ftNet, miNetFreq = ef.fft10Days(aSampNet)
    
    # Mask 4 Panels
    ftmask = np.absolute(ftPanel)**2< 5e2
    ftmask1 = np.absolute(ftPanel)**2< 1e5
    ftmask2 = np.absolute(ftPanel)**2< 7e1
    ftmaskC = np.absolute(ftPanel)**2 < 27079
    filteredPanel, filteredPanel1, filteredPanel2, comparePanel = ef.ifft10Days(ftPanel, aSampPanel[4320:], ftmask, ftmask1, ftmask2, ftmaskC) # Inverse FFT with filtred coeff
    
    plt.subplots(figsize=(15,6))
    plt.plot(time10/60, aSampPanel[4320:], '-', label='panels', c='gold', linewidth=3)
    plt.plot(time10/60, filteredPanel2, color='salmon', label='Filtro $coeff>7\cdot 10^1$') # a lot of freq
    plt.plot(time10/60, filteredPanel1, color='aqua', label='Filtro $coeff>1\cdot 10^5$') # only 3 freq (red, orange, gold in spectrum plot)
    plt.plot(time10/60, filteredPanel, color='darkviolet', label='Filtro $coeff>5\cdot 10^2$') # some freq
    ef.daySeparatorLine('lightgrey')
    plt.legend()
    plt.title('16-25 December\'s panels plot and filtred plots')
    plt.ylabel('Power (kW)')
    plt.xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    plt.xticks( ticks = np.arange(0, 240, 6), labels = np.resize(np.arange(0, 24, 6),4*10) )
    plt.yticks(np.arange(-1,max(aSampPanel[4320:]),1))
    plt.savefig('filtredPanels.png')
    plt.show()

    # Mask 4 Pawerwall
    ftmask = np.absolute(ftPwall)**2< 5e3
    ftmask1 = np.absolute(ftPwall)**2< 2e4
    ftmask2 = np.absolute(ftPwall)**2< 7e1
    ftmaskC = np.absolute(ftPwall)**2 < 19152
    filteredPwall, filteredPwall1, filteredPwall2, comparePwall = ef.ifft10Days(ftPwall, aSampPanel[4320:], ftmask, ftmask1, ftmask2, ftmaskC) # Inverse FFT with filtred coeff
    
    plt.subplots(figsize=(15,6))
    plt.plot(time10/60, aSampPwall[4320:], '-', label='powerwall', c='gold', linewidth=3)
    plt.plot(time10/60, filteredPwall2, color='salmon', linewidth=0.5, label='Filtro $coeff>7\cdot 10^1$') # a lot of freq
    plt.plot(time10/60, filteredPwall1, color='aqua', label='Filtro $coeff>2\cdot 10^4$') # only 6 freq (red, orange, gold in spectrum plot + 3)
    plt.plot(time10/60, filteredPwall, color='darkviolet', label='Filtro $coeff>5\cdot 10^3$') # some freq
    ef.daySeparatorLine('lightgrey')
    plt.legend()
    plt.title('16-25 December\'s powerwall plot and filtred plots')
    plt.ylabel('Power (kW)')
    plt.xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    plt.xticks( ticks = np.arange(0, 240, 6), labels = np.resize(np.arange(0, 24, 6),4*10) )
    plt.yticks(np.arange(-2,max(aSampPwall[4320:]),1))
    plt.savefig('filtredPowerwall.png')
    plt.show()

    # Mask 4 Home
    ftmask = np.absolute(ftHome)**2< 5e3
    ftmask1 = np.absolute(ftHome)**2< 5e5
    ftmask2 = np.absolute(ftHome)**2< 7e1
    ftmaskC = np.absolute(ftHome)**2 < 607138
    filteredHome, filteredHome1, filteredHome2, compareHome = ef.ifft10Days(ftHome, aSampPanel[4320:], ftmask, ftmask1, ftmask2, ftmaskC) # Inverse FFT with filtred coeff
    
    plt.subplots(figsize=(15,6))
    plt.plot(time10/60, aSampHome[4320:], '-', label='home consumption', c='gold', linewidth=3)
    plt.plot(time10/60, filteredHome2, color='salmon', linewidth=0.5, label='Filtro $coeff>7\cdot 10^1$') # a lot of freq
    plt.plot(time10/60, filteredHome, color='darkviolet', label='Filtro $coeff>5\cdot 10^3$') # some freq
    plt.plot(time10/60, filteredHome1, color='aqua', label='Filtro $coeff>5\cdot 10^5$') # only 7 freq (red, orange, gold in spectrum plot + 4)
    ef.daySeparatorLine('lightgrey')
    plt.legend()
    plt.title('16-25 December\'s home plot and filtred plots')
    plt.ylabel('Power (kW)')
    plt.xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    plt.xticks( ticks = np.arange(0, 240, 6), labels = np.resize(np.arange(0, 24, 6),4*10) )
    plt.yticks(np.arange(-1,max(aSampHome[4320:]),1))
    plt.savefig('filtredHome.png')
    plt.show()

    # Mask 4 Net
    ftmask = np.absolute(ftNet)**2< 5e3
    ftmask1 = np.absolute(ftNet)**2< 5e5
    ftmask2 = np.absolute(ftNet)**2< 7e1
    ftmaskC = np.absolute(ftNet)**2 < 533381
    filteredNet, filteredNet1, filteredNet2, compareNet = ef.ifft10Days(ftNet, aSampPanel[4320:], ftmask, ftmask1, ftmask2, ftmaskC) # Inverse FFT with filtred coeff
    
    plt.subplots(figsize=(15,6))
    plt.plot(time10/60, aSampNet[4320:], '-', label='net absorption', c='gold', linewidth=3)
    plt.plot(time10/60, filteredNet2, color='salmon', linewidth=0.5, label='Filtro $coeff>7\cdot 10^1$') # a lot of freq
    plt.plot(time10/60, filteredNet, color='darkviolet', label='Filtro $coeff>5\cdot 10^3$') # some freq
    plt.plot(time10/60, filteredNet1, color='aqua', label='Filtro $coeff>5\cdot 10^5$') # only 10 freq (red, orange, gold in spectrum plot + 7)
    ef.daySeparatorLine('lightgrey')
    plt.legend()
    plt.title('16-25 December\'s net plot and filtred plot')
    plt.ylabel('Power (kW)')
    plt.xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    plt.xticks( ticks=np.arange(0, 240, 6), labels=np.resize(np.arange(0, 24, 6),4*10) )
    plt.yticks(np.arange(-1,max(aSampNet[4320:]),1))
    plt.savefig('filtredNet.png')
    plt.show()


    ## FREQUENCIES COMPARISON 
    fig, ax = plt.subplots(3,1, figsize=(12,13))
    ax[0].plot(time10/60, comparePanel, color='gold', label='Panels', linewidth=2.5)
    ax[0].plot(time10/60, comparePwall, color='green', alpha=0.4, label='Powerwall', linewidth=2.5)
    ax[0].plot(time10/60, compareHome, color='red', alpha=0.5, label='Home')
    ax[0].plot(time10/60, compareNet, color='blue', alpha=0.3, label='Net')
    ax[0].set_ylabel('Power (kW)')
    ax[0].set_xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    ax[0].set_xticks( ticks=np.arange(0,240,6), labels=np.resize(np.arange(0,24,6),4*10) )
    ax[0].set_yticks(np.arange(-2,max(aSampHome[4320:]),1))
    fig.suptitle('16-25 December\'s filtred plot with only the 7 most important freq for each category')
       
    ax[1].plot(time10/60, aSampHome[4320:], color='black', linewidth=2, label='real Home')
    ax[1].plot(time10/60, aSampNet[4320:]+aSampPanel[4320:]+aSampPwall[4320:], color='darkcyan',  linewidth=0.5, label='real Net+Panel+Pwall')
    ax[1].plot(time10/60, compareNet+compareHome+comparePanel, color='fuchsia',label='Net+Panel+Pwall')
    ax[1].plot(time10/60, compareHome, color='tomato', label='Home')
    fig.legend(['Panels','Powerwall','Home','Net','real Home','real Net+Panel+Pwall','Net+Panel+Pwall'], loc='upper right')#legend here 4 not include day separators
    for i in range(11):
        ax[0].axvline(x=i*24, color='lightgrey') # day separator
        ax[1].axvline(x=i*24, color='lightgrey') # day separator
    ax[1].set_ylabel('Power (kW)')
    ax[1].set_xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
    ax[1].set_xticks( ticks=np.arange(0,240,6), labels=np.resize(np.arange(0,24,6),4*10) )
    ax[1].set_yticks(np.arange(-2,max(aSampHome[4320:]),1))

    # build a matrix for table about 7 most significant freq for each category
    freq7 = np.zeros((4,7), dtype=float) 
    freq7[0,:], freq7[1,:], freq7[2,:], freq7[3,:] = miPanelFreq, miPwallFreq, miHomeFreq, miNetFreq
    freq7 = np.round(1e5*freq7, decimals=3)
    columns = ('1°freq $(1e5\cdot Hz)$','2°freq $(1e5\cdot Hz)$','3°freq $(1e5\cdot Hz)$','4°freq $(1e5\cdot Hz)$','5°freq $(1e5\cdot Hz)$','6°freq $(1e5\cdot Hz)$','7°freq $(1e5\cdot Hz)$')
    rows = ('Panelels', 'Powerwall', 'Home', 'Net')
    colors = ('gold', 'limegreen', 'tomato', 'cornflowerblue')
    ax[2].axis('tight')
    ax[2].axis('off')
    ax[2].table(cellText=freq7, rowLabels=rows, rowColours=colors, colLabels=columns, loc='center')
    plt.savefig('correlationTable.png')
    plt.show()


### POWERS' INTEGER
if True:
    iPanel = np.zeros(len(time10))
    iPwall = np.zeros(len(time10))
    iHome = np.zeros(len(time10))
    iNet = np.zeros(len(time10))
    for i in range(len(time10)):
        iPanel[i] = integrate.simpson(aSampPanel[4320:i+4321],time10[:i+1]/60) # divided by 60 cause i want the energy in kWh, not kWmin
        iPwall[i] = integrate.simpson(aSampPwall[4320:i+4321],time10[:i+1]/60)
        iHome[i] = integrate.simpson(aSampHome[4320:i+4321],time10[:i+1]/60)
        iNet[i] = integrate.simpson(aSampNet[4320:i+4321],time10[:i+1]/60)
    print(' Panels (kWh): ',round(iPanel[-1],2),'\n Pwall (kWh): ',round(iPwall[-1],2),'\n Home (kWh): ',round(iHome[-1],2),'\n Net (kWh): ',round(iNet[-1],2))
    aPowPanel, aPowPwall, aPowHome, aPowNet = ef.power4Day(iPanel), ef.power4Day(iPwall), ef.power4Day(iHome), ef.power4Day(iNet)
    
    fig, ax = plt.subplots(4,1, figsize=(12,8))
    fig.suptitle('16-25 December\'s energy plot for each category')       
    ax[0].plot(time10/60, iPanel, color='orange', label='Panels energy')
    ax[1].plot(time10/60, iPwall, color='darkgreen', label='Powerwall energy')
    ax[2].plot(time10/60, iHome, color='darkred', label='Home energy')
    ax[3].plot(time10/60, iNet, color='mediumblue', label='Net energy')
    ax[0].plot(time10/60, aSampPanel[4320:], color='gold', linewidth=2, label='Panels (kW)')
    ax[1].plot(time10/60, aSampPwall[4320:], color='green', alpha=0.4, label='Powerwall (kW)')
    ax[2].plot(time10/60, aSampHome[4320:], color='red', alpha=0.5, label='Home (kW)')
    ax[3].plot(time10/60, aSampNet[4320:], color='blue',  alpha=0.3, label='Net (kW)')
    ax[0].text(0, iPanel[-1]*18/23, f'Total panels power = {round(iPanel[-1],2)} kWh \n day by day power = {aPowPanel} kWh', fontsize=10, color='peru')
    ax[1].text(0, iPwall[-1]*11/12, f'Total powerwall power = {round(iPwall[-1],2)} kWh \n day by day power = {aPowPwall} kWh', fontsize=10, color='darkgreen')
    ax[2].text(0, iHome[-1]*18/23, f'Home power = {round(iHome[-1],2)} kWh \n day by day power = {aPowHome} kWh', fontsize=10, color='darkred')
    ax[3].text(0, iNet[-1]*18/23, f'Net power = {round(iNet[-1],2)} kWh \n day by day power = {aPowNet} kWh', fontsize=10, color='darkblue')
    fig.legend(['Panels energy','Panels (kW)','Powerwall energy','Powerwall (kW)','Home energy','Home (kW)','Net energy','Net (kW)'], loc='upper right')
    for y in range(4):
        ax[y].set_ylabel('Energy (kWh)')
        ax[y].set_xlabel('Time (hours from 00:00 of 16/12/22 to 23:55 of 25/12/22)')
        ax[y].set_xticks( ticks=np.arange(0,240,6), labels=np.resize(np.arange(0,24,6),4*10) )
        for i in range(11):
            ax[y].axvline(x=i*24, color='lightgrey') # day separator
    plt.savefig('absorptionPlot.png')
    plt.show()
    
    
    
##### OPTIONAL: ORIGIN OF HOME CONSUMPTION ENERGY SOURCES
    labels = ['Panels', 'Powerwall', 'Net']
    sizes = [iPanel[-1]+iPwall[-1], -iPwall[-1], iNet[-1]] # Pann=total renewable
    colors = ['gold', 'palegreen', 'dodgerblue']
    explode = (0, 0, 0.1)  # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal') # pie drawn as a circle
    plt.title('Origin of 10 days\' home consumption sources')
    plt.savefig('sourcesPie.png')
    plt.show()  
