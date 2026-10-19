
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import numpy as np
import math

import matplotlib.pyplot as plt

import neurokit2 as nk
import pandas as pd
import glob
import os


import gettext


localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.itaolang])
localizator.install() 
_ = localizator.gettext 

FIGPNGDIR = "images/"
FIGPNGFILENAME = FIGPNGDIR+st.session_state.PQRSTfig # "images/fig.png"
EKGIMPDIR = "imp/"
#EKGIMPDIR = "ekg/imp/"
BLOODFACTOR = 18.0

en_pqrst = _('''
The application based on neurokit2 package demonstrates the behavior of the PQRST complex as a whole.
The patients data were taken from PTB Diagnostic ECG Database (https://www.physionet.org/content/ptbdb/1.0.0/).
ECGs were recorded at sampling rate 1000 Hz. The PTB database records 15 simultaneously measured signals—12 conventional leads 
plus Frank X/Y/Z — and uses 1000 samples/sec with 16-bit resolution.

The application has the following options:

PQRST
                                                                                                                                                                                
Instead of usual PQRST peaks, the vertical half-lemniscates are used.
The height of half-lemniscate is equal to the height of usual PQRST peak.
The values of the PQRST peaks and percentage of peaks are shown.
It allows to see, that any change of one part of PQRST peak leads to the change of the whole PQRST complex.

BLOOD
                                                                                                                                                                                
The energy of blood makes the heart pulse. It is several times more than the total energy of one beat. The energy of blood is shown as Cassini oval.
If the form of curve has a form of two separated ovals, this could indicate an illness.
The illness tendency is displayed in percent.
The distance between navel and fossa jugularis is neсesary for calculation of oval.

SIGNAL

The usual ecg signals are shown.

'''
)

de_pqrst = _('''
Die auf dem Paket „neurokit2“ basierende Anwendung veranschaulicht das Verhalten des PQRST-Komplexes als Ganzes.
Die Patientendaten stammen aus der PTB Diagnostic ECG Database (https://www.physionet.org/content/ptbdb/1.0.0/).
Die EKGs wurden mit einer Abtastrate von 1000 Hz aufgezeichnet.
Die PTB-Datenbank erfasst 15 simultan gemessene Signale – 12 konventionelle Ableitungen sowie Frank-X/Y/Z – 
und verwendet eine Abtastrate von 1000 Abtastwerten pro Sekunde bei einer Auflösung von 16 Bit.

Die Anwendung hat folgende Optionen:

PQRST
                                                                                                                                                                                                                                                                                                                                                                 
Anstelle der üblichen PQRST-Zacken werden vertikale Halblemniskaten verwendet. 
Die Höhe der Halblemniskate entspricht dabei der Höhe der jeweiligen PQRST-Zacke. 
Angezeigt werden die Werte der PQRST-Zacken sowie Prozentsatz der Zacken. 
Dies macht deutlich, dass jede Veränderung eines Teils einer PQRST-Zacke zu einer Veränderung des gesamten PQRST-Komplexes führt.

BLOOD

Die Energie des Blutes lässt das Herz pulsieren. Sie ist ein Vielfaches der Gesamtenergie eines einzelnen Herzschlags. 
Die Energie des Blutes wird als Cassini-Oval dargestellt.
Wenn die Kurve die Form zweier getrennter Ovale aufweist, könnte dies auf eine Erkrankung hinweisen.
Die Krankheitstendenz wird in Prozent angegeben.
Der Abstand zwischen Bauchnabel und Fossa jugularis ist für die Berechnung des Ovals erforderlich.

SIGNAL

Die üblichen EKG-Signale werden angezeigt.

'''
)

ru_pqrst = _('''
Приложение, разработанное на основе пакета neurokit2, демонстрирует поведение комплекса PQRST в целом.
Данные пациентов были взяты из диагностической базы данных ЭКГ PTB (https://www.physionet.org/content/ptbdb/1.0.0/).
Запись ЭКГ производилась с частотой дискретизации 1000 Гц. В базе данных PTB регистрируются 15 одновременно измеряемых сигналов — 12 стандартных отведений 
плюс отведения X, Y и Z по методу Франка; 
частота дискретизации составляет 1000 отсчетов в секунду при 16-битном разрешении.

Приложение имеет следующие опции:

PQRST
                                                                                                                                                                                                                                                                                                                                                                 
Вместо привычных пиков PQRST используются вертикальные полулемнискаты; высота полулемниската соответствует высоте стандартного пика PQRST. 
Отображаются значения пиков PQRST и проценты пиков.  
Это позволяет наглядно увидеть, что изменение любой части пика PQRST влечет за собой изменение всего комплекса PQRST.


BLOOD

Энергия крови заставляет сердце пульсировать. Она в несколько раз превышает суммарную энергию одного сердечного сокращения. 
Энергия крови визуализируется в виде овала Кассини.
Если кривая имеет форму двух разделенных овалов, это может указывать на заболевание.
Тенденция к заболеванию покзываается в процентах.
Расстояние между пупком и яремной ямкой необходимо для расчета овала.

СИГНАЛ

Показаны стандартные сигналы ЭКГ.

'''
)

pqrst = {"en":en_pqrst, "de":de_pqrst, "ru":ru_pqrst, }

st.title(_("PQRST"))

def nextNumber():
    res = glob.glob(FIGPNGDIR + "fig*.png", recursive=False)
    res = sorted(res)

    prevcnt = 0
    for file in res:
        
        if file == "images/fig.png":
            continue
        
        nextcnt = int(file[10:-4])
        if prevcnt == 0:
            if nextcnt > 1:
                return prevcnt + 1
            
            prevcnt = nextcnt
            continue

        if prevcnt + 1 < nextcnt:
            return prevcnt + 1
        
        prevcnt += 1
     
    return prevcnt + 1

    

def figNumber():
    import shutil      
   
    fignumber = nextNumber()
#    print("FIGNUMBER", fignumber)
    srcname  = FIGPNGDIR+"fig.png"
    dstname = FIGPNGDIR+"fig"+str(fignumber)+".png"
    with open(srcname, "rb") as src, open(dstname, "xb") as dst:
        shutil.copyfileobj(src, dst)
        st.session_state.PQRSTfig = "fig"+str(fignumber)+".png"

if "PQRSTidx" not in st.session_state:
    st.session_state.PQRSTidx = 0
    figNumber()
if "PQRSTsigidx" not in st.session_state:
    st.session_state.PQRSTsigidx = 0
if "PQRSTpauseidx" not in st.session_state:
    st.session_state.PQRSTpauseidx = 0
if "PQRSTinit" not in st.session_state:
    st.session_state.PQRSTinit = True
if "PQRSTaveragedist" not in st.session_state:
    st.session_state.PQRSTaveragedist = 0
    
def msg(msg):
    placeholder = st.empty()
    with placeholder.container():
        st.write(msg)

def percentage(part, whole):
    if whole == 0:
        return 0
    return 100 * float(part)/float(whole)


def CassiniXY(x, y):
#(x**2 + y**2)**2 - 2*a**2*(x**2 - y**2) + a**4 - b**4 = 0
#a == b
#(x**2 + y**2)**2 = 2*a**2*(x**2 - y**2)
#a = np.sqrt((x**2 + y**2)**2 / 2*(x**2 - y**2))
    
#    valid = 2*(x**2 - y**2)
#    a = np.sqrt((x**2 + y**2)**2 / valid)
#    return np.abs(a)    

    return np.abs(x/np.sqrt(2))  
   

# plt.savefig("plot.png", format="png")
#https://mathcurve.com/courbes2d.gb/cassini/cassini.shtml
#https://stackoverflow.com/questions/71684763/plot-cassini-ovals-in-python-using-numpy-and-matplotlib
def CassiniSteinerShort(a, b, clr=None, vertical=True, half=False, upper=False, linestyle='-', show=True, N=1000000):

#    y = np.sqrt(np.abs(np.sqrt(b**4  + 4*a**2*x**2 ) - (a**2 + x**2)))
#    y = np.sqrt(np.abs(np.sqrt(b**4  + 4*a**2*x**2 ) - (a**2 + x**2)))
#    If a ≤ b ≤ a√2 the "ovals" look no more like circles. 
#    Here a is one, b goes from 1 to √2 (inclusively)               

#    print ("CassiniSteinerShort")
    if a == 0:
        a = 0.0001
        
    t = np.linspace(-a + np.sqrt(a**2 + b**2), a + np.sqrt(a**2 + b**2), N)
    if a >= b:
        t = np.linspace(a + np.sqrt(a**2 - b**2), a + np.sqrt(a**2 + b**2), N)
    x = (b**4 - t**4)/(4*a*(t**2))
    y = np.sqrt(np.abs(t**2 - ((x-a)**2)))
    
#        plt.scatter(x, y, c='red', s=2, zorder=2)
    if vertical == True:
        if upper == False:
            plt.plot(y, x, clr, ls=linestyle) # right part
            plt.plot(-y, x, clr, ls=linestyle) # left part
            if half == False:
                plt.plot(-y, -x, clr, ls=linestyle) # right part
                plt.plot(y, -x, clr, ls=linestyle) # left part
        else:
            plt.plot(y, -x, clr, ls=linestyle) # right part
            plt.plot(-y, -x, clr, ls=linestyle) # left part                        
            if half == False:
                plt.plot(-y, x, clr, ls=linestyle) # right part
                plt.plot(y, x, clr, ls=linestyle) # left part            
    else:
        plt.plot(x, y, clr, ls=linestyle) # left upper part
        plt.plot(x, -y, clr, ls=linestyle) # left lower part        
        if half == False:
            plt.plot(-x, y, clr, ls=linestyle) # right upper part
            plt.plot(-x, -y, clr, ls=linestyle) # right lower part
        
    
    if show == True:
        fig = plt.gcf()
        st.pyplot(fig)
        saveFig()
        st.image(FIGPNGFILENAME)
#        plt.show()


def square_lemniscate(a, half=True):
    S = a**2
    if half == True:
        S /= 2
    return S
 
def volume_lemniscate(a, half=True):
    sq = math.sqrt(2)
    V = 2 * ((math.pi * a**3) / 4) * (sq * math.log(sq + 1) - 2/3)
#    V = 2 * ((math.pi * val**3) / 4) * math.floor(sq * math.log(sq + 1) - 2/3)
    if half == True:
        V /= 2
    return V
 
def zero_NaN(peaks, val=0):
    for x in range(len(peaks)):
        if math.isnan(peaks[x]) == True:
            peaks[x] = val

def getSession():
    from streamlit.runtime import get_instance
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    
    
#    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
#    session_info = runtime._session_mgr.get_session_info(session_id)
#    if session_info is None:
#        raise RuntimeError("Couldn't get your Streamlit Session object.")
    print("SESSION ID", session_id)
#    st.write(session_info.session)
    st.write(session_id)
#    return session_info.session

def saveFig(): 
    plt.savefig(FIGPNGFILENAME, format="png")

def calcDist(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks):    
                
    zero_NaN(p_peaks)
    zero_NaN(q_peaks)
    zero_NaN(r_peaks)
    zero_NaN(s_peaks)
    zero_NaN(t_peaks)

    minLen = min(len(p_peaks), len(q_peaks)-1, len(r_peaks)-1, len(s_peaks)-1, len(t_peaks)-1)

    dist = 0
    minDist = 0
    maxDist = 0
    cnt = 0
    a = st.session_state.PQRSTdist / 2
    cnta = 0
    for idx in range(0, minLen):
        total_sum = np.abs(unfiltered_ecg[p_peaks[idx]]) + np.abs(unfiltered_ecg[q_peaks[idx]]) + np.abs(unfiltered_ecg[r_peaks[idx]]) + np.abs(unfiltered_ecg[s_peaks[idx]]) + np.abs(unfiltered_ecg[t_peaks[idx]])
        bloodc =  (BLOODFACTOR * total_sum) # total energy of blood circulation
    
#        a = st.session_state.PQRSTdist / 2
#    print("DIST", str(st.session_state.PQRSTdist))
        b = CassiniXY(bloodc, 0)
        if b < a:
            cnta += 1
        
        if minDist == 0:
            minDist = b
        if maxDist < b:
            maxDist = b
            
        dist += b
        cnt = idx + 1
         
    dist = (dist / cnt) * 2
    minDist *= 2
    maxDist *= 2
    st.session_state.PQRSTaveragedist = round(dist, 2)
    st.session_state.PQRSTmindist = round(minDist, 2)
    st.session_state.PQRSTmaxdist = round(maxDist, 2)
    st.session_state.PQRSTpercentdist = round(percentage(cnta, cnt), 2)

#    print("CALC DIST MIN MAX CNT CNTA", round(dist, 2), round(minDist, 2), round(maxDist, 2), cnt, cnta, str(round(percentage(cnta, cnt), 2)) + "%")
        
    return dist
    
#    https://discuss.streamlit.io/t/continuously-updating-image-content/86954/2
@st.fragment(run_every=1)
def draw_image(pause, algorithm_name, data_name, samplerate):
    if pause == 0:
        return None
    
    streamlit_image_coordinates(FIGPNGFILENAME, key="PQRST_01")
#    st.image(FIGPNGFILENAME)
    if st.session_state.PQRSTinit == True:
#        print("DO INIT TRUE")
        st.session_state.PQRSTidx = 0

        try:                
            r0, r1, r2, r3, r4, r5 = initComplex(pause, algorithm_name, data_name, samplerate)
            st.session_state.itaor0 = r0
            st.session_state.itaor1 = r1
            st.session_state.itaor2 = r2
            st.session_state.itaor3 = r3
            st.session_state.itaor4 = r4
            st.session_state.itaor5 = r5
            
#            calcDist(r0, r1, r2, r3, r4, r5)
             
            st.session_state.PQRSTinit = False

        except Exception as e:
            st.error(f"initComplex Failed:\n {e}")
    if st.session_state.PQRSTinit == False:
        updateComplex(st.session_state.itaor0, st.session_state.itaor1, st.session_state.itaor2, 
                          st.session_state.itaor3, st.session_state.itaor4, st.session_state.itaor5)
        saveFig()
        

def readData(data_name, csv=True):
    
    data_ekg = None
    if csv:
#        msg("Read CSV data" + data_name  + ' (neurokit2)')
        data_ekg = pd.read_csv(EKGIMPDIR+data_name+".csv")                         
    else:
#        msg('Retrieving data ' + data_name + ' (neurokit2)')
        data_ekg = nk.data(dataset=data_name)
    return data_ekg

def initComplex(pause, algorithm_name, data_name, samplerate):
    
    data = readData(data_name)
    ecg_signal = data["ECG"]
        
#    msg('Retrieving EKG peaks (neurokit2)')

    # Extract R-peaks locations
    sigs, rpeaks = nk.ecg_peaks(ecg_signal, method=algorithm_name, sampling_rate=samplerate)
                
#    msg('Delineating EKG (neurokit2)')

    # Delineate the ECG signal method = peak cwt dwt
    sigs, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=samplerate, method="peak")
    
    r0 = ecg_signal
    r1 = waves_peak['ECG_P_Peaks']
    r2 = waves_peak['ECG_Q_Peaks']
    r3 = rpeaks['ECG_R_Peaks']
    r4 = waves_peak['ECG_S_Peaks']
    r5 = waves_peak['ECG_T_Peaks']               
    
    minLen = min(len(r1), len(r2)-1, len(r3)-1, len(r4)-1, len(r5)-1)
#    minLen = min(len(waves_peak['ECG_P_Peaks']), len(waves_peak['ECG_Q_Peaks'])-1, len(rpeaks['ECG_R_Peaks'])-1, len(waves_peak['ECG_S_Peaks'])-1, len(waves_peak['ECG_T_Peaks'])-1)
    if st.session_state.PQRSTidx in range(0, minLen):
        if pause == 0:
#            print("PAUSE")
            return None, None, None, None, None, None
    
#    print("RETURN initComplex")
    return r0, r1, r2, r3, r4, r5
    
                       
def updateComplex(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks):
    idx = st.session_state.PQRSTsigidx
    if idx == 0:
#        msg('Plotting PQRST')
        update_PQRST(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks)        
    elif idx == 1:
#        msg('Plotting BLOOD')
        update_BLOOD(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks)        
    elif idx == 2:
#        msg('Plotting SIGNAL')
        update_SIGNAL(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks)        

               
def update_PQRST(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks):
    plt.clf()
            
    zero_NaN(p_peaks)
    zero_NaN(q_peaks)
    zero_NaN(r_peaks)
    zero_NaN(s_peaks)
    zero_NaN(t_peaks)
    
    minLen = min(len(p_peaks), len(q_peaks)-1, len(r_peaks)-1, len(s_peaks)-1, len(t_peaks)-1)
    if st.session_state.PQRSTidx >= minLen:
#        print('update limit reached idx=' + str(st.session_state.PQRSTidx))
        st.session_state.PQRSTidx = 0

    idx = st.session_state.PQRSTidx

    clrP = 'orange'
    clrQ = 'green'
    clrR = 'red'
    clrS = 'blue'
    clrT = 'brown'
    
    total_sum = np.abs(unfiltered_ecg[p_peaks[idx]]) + np.abs(unfiltered_ecg[q_peaks[idx]]) + np.abs(unfiltered_ecg[r_peaks[idx]]) + np.abs(unfiltered_ecg[s_peaks[idx]]) + np.abs(unfiltered_ecg[t_peaks[idx]])
    
    a = CassiniXY(unfiltered_ecg[p_peaks[idx]], 0)
    CassiniSteinerShort(a, a, clr=clrP, half=True, upper=True, show=False)
    a = CassiniXY(unfiltered_ecg[q_peaks[idx]], 0)
    CassiniSteinerShort(a, a, clr=clrQ, half=True, upper=False, show=False)
    a = CassiniXY(unfiltered_ecg[r_peaks[idx]], 0)
    CassiniSteinerShort(a, a, clr=clrR, half=True, upper=True, show=False)
    a = CassiniXY(unfiltered_ecg[s_peaks[idx]], 0)
    CassiniSteinerShort(a, a, clr=clrS, half=True, upper=False, show=False)
    a = CassiniXY(unfiltered_ecg[t_peaks[idx]], 0)
    CassiniSteinerShort(a, a, clr=clrT, half=True, upper=True, show=False)
    
    fs = 8
    x = 0.5
    y = 0.5
    
    perc_p = ' ' + str(abs(round(percentage(unfiltered_ecg[p_peaks[idx]], total_sum), 2))) +'% '
    perc_q = ' ' + str(abs(round(percentage(unfiltered_ecg[q_peaks[idx]], total_sum), 2))) +'% '
    perc_r = ' ' + str(abs(round(percentage(unfiltered_ecg[r_peaks[idx]], total_sum), 2))) +'% '
    perc_s = ' ' + str(abs(round(percentage(unfiltered_ecg[s_peaks[idx]], total_sum), 2))) +'% '
    perc_t = ' ' + str(abs(round(percentage(unfiltered_ecg[t_peaks[idx]], total_sum), 2))) +'% '

    label = 'P ' + str(unfiltered_ecg[p_peaks[idx]]) + perc_p 
    plt.plot(x, y, clrP, label=label)
    label = 'Q ' + str(unfiltered_ecg[q_peaks[idx]]) + perc_q 
    plt.plot(x, y, clrQ, label=label)
    label = 'R ' + str(unfiltered_ecg[r_peaks[idx]]) + perc_r
    plt.plot(x, y, clrR, label=label)
    label = 'S ' + str(unfiltered_ecg[s_peaks[idx]]) + perc_s
    plt.plot(x, y, clrS, label=label)
    label = 'T ' + str(unfiltered_ecg[t_peaks[idx]]) + perc_t
    plt.plot(x, y, clrT, label=label)        
    plt.legend(fontsize=str(fs), loc='lower right')
                    
    plt.title("PQRST plot " + str(st.session_state.PQRSTidx))
    
#    plt.pause(1)
    
    st.session_state.PQRSTidx += 1

def calcB(x, a):
    b = np.sqrt(np.abs(x**2 - a**2))
    return b

def plotCassini(peak, bloodc, clr, upper=True):
#    f = .5*np.sqrt(2)/bloodc
    dblf = 25 # display blood factor
    
    a = CassiniXY(peak, 0)
#    b = calcB(peak*f, a)
    b = a # calcB(peak*f, a)

    b *= dblf
    a *= dblf
    CassiniSteinerShort(a, b, clr=clr, half=True, upper=upper, show=False)
                   
def update_BLOOD(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks):
    plt.clf()
        
    zero_NaN(p_peaks)
    zero_NaN(q_peaks)
    zero_NaN(r_peaks)
    zero_NaN(s_peaks)
    zero_NaN(t_peaks)
    
    minLen = min(len(p_peaks), len(q_peaks)-1, len(r_peaks)-1, len(s_peaks)-1, len(t_peaks)-1)
    if st.session_state.PQRSTidx >= minLen:
#            print('update limit reached idx=' + str(idxs))
        st.session_state.PQRSTidx = 0

#        print('update idx=' + str(idxs))
    
    idx = st.session_state.PQRSTidx          
        
    clrP = 'orange'
    clrQ = 'green'
    clrR = 'pink'
    clrS = 'blue'
    clrT = 'brown'
    
    total_sum = np.abs(unfiltered_ecg[p_peaks[idx]]) + np.abs(unfiltered_ecg[q_peaks[idx]]) + np.abs(unfiltered_ecg[r_peaks[idx]]) + np.abs(unfiltered_ecg[s_peaks[idx]]) + np.abs(unfiltered_ecg[t_peaks[idx]])
    bloodc =  (BLOODFACTOR * total_sum) # total energy of blood circulation

    plotCassini(unfiltered_ecg[p_peaks[idx]], bloodc, clrP)
    plotCassini(unfiltered_ecg[q_peaks[idx]], bloodc, clrQ, False)
    plotCassini(unfiltered_ecg[r_peaks[idx]], bloodc, clrR)
    plotCassini(unfiltered_ecg[s_peaks[idx]], bloodc, clrS, False)
    plotCassini(unfiltered_ecg[t_peaks[idx]], bloodc, clrT)

    clrPQRST = 'white'
    clrBLOOD = 'red'
    
    ls='--'
    if idx % 4 == 0:
        ls='-'
    
    a = st.session_state.PQRSTdist / 2
#    print("DIST", str(st.session_state.PQRSTdist))
    b = calcB(bloodc, a)
#    print(str(idx) + ' a='+ str(a)  + ' b='+ str(b))
    CassiniSteinerShort(a, b, clr=clrBLOOD, vertical=True, half=False, upper=True, linestyle=ls, show=False)
    
    fs = 8
    x = 0.5
    y = 0.5
    
    if st.session_state.PQRSTaveragedist == 0:
        calcDist(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks)
               
    label = 'BLOOD ' + str(round(bloodc, 2))
    plt.plot(x, y, clrBLOOD, label=label)
    label = 'DIST ' + str(round(CassiniXY(bloodc, 0), 2) * 2) # + " " + str(st.session_state.PQRSTpercentdist) + "%"
    plt.plot(x, y, clrPQRST, label=label)
#    label = 'AVED ' + str(st.session_state.PQRSTaveragedist)
#    plt.plot(x, y, clrPQRST, label=label)
#    label = 'MIND ' + str(st.session_state.PQRSTmindist)
#    plt.plot(x, y, clrPQRST, label=label)
#    label = 'MAXD ' + str(st.session_state.PQRSTmaxdist)
#    plt.plot(x, y, clrPQRST, label=label)    
   
#    label = 'PQRST ' + str(total_sum)
#    plt.plot(x, y, clrPQRST, label=label)
    plt.legend(fontsize=str(fs), loc='lower right')
                    
    plt.title("BLOOD plot " + str(st.session_state.PQRSTidx) + " \n" + _("Illness")  + " " + str(st.session_state.PQRSTpercentdist) + "%")
    
#    plt.pause(1)
    
    st.session_state.PQRSTidx += 1
               
               
def update_SIGNAL(unfiltered_ecg, p_peaks, q_peaks, r_peaks, s_peaks, t_peaks):
    plt.clf()
            
    zero_NaN(p_peaks)
    zero_NaN(q_peaks)
    zero_NaN(r_peaks)
    zero_NaN(s_peaks)
    zero_NaN(t_peaks)
                    
    minLen = min(len(p_peaks), len(q_peaks)-1, len(r_peaks)-1, len(s_peaks)-1, len(t_peaks)-1)
    if st.session_state.PQRSTidx >= minLen:
#            print('update limit reached idx=' + str(idxs))
        st.session_state.PQRSTidx = 0

#        print('update idx=' + str(idxs))
            
    step = 1000

    upper_limit = len(unfiltered_ecg)
#        print('idxs[0]=' + str(idxs[0]) + " upper_limit=" + str(upper_limit))
                   
    if (st.session_state.PQRSTidx - 1) * step >= upper_limit:
#            print('upper limit reached idx=' + str(idxs))
        st.session_state.PQRSTidx = 0

#        print('upper idx=' + str(idxs))
    
    idx = st.session_state.PQRSTidx
    if idx > 1:
        y = unfiltered_ecg[(idx - 1) * step : idx * step]
        l = len(unfiltered_ecg[(idx - 1) * step : idx * step])
        if l < step:
#                print('l=' + str(l) + ' is less than 1000')
            x = np.linspace((idx - 1) * step, idx * step, l)
        else:
            x = np.linspace((idx - 1) * step, idx * step, step)
    else:
        y = unfiltered_ecg[0 : step]
#            l = len(unfiltered_ecg[0 : 1000])
        x = np.linspace(0, step, step)
    
#        xcoo = [n for n in range(len(y))]
#        plt.scatter(x, y, c='red', s=2, zorder=2)
    
    plt.plot(x, y)
                            
    plt.title("SIGNAL plot " + str(st.session_state.PQRSTidx))
    
#    plt.pause(1)
    
    st.session_state.PQRSTidx += 1

data_names = {
    'patient001_s0010_re_MyocardialInfarction': _("age") + ": 81 " + _("sex") + ": " + _("female") + " " + _("ECG") + " " + _("date") + ": 01/10/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient001_s0014lre_MyocardialInfarction': _("age") + ": 81 " + _("sex") + ": " + _("female") + " " + _("ECG") + " " + _("date") + ": 17/10/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient001_s0016lre_MyocardialInfarction': _("age") + ": 81 " + _("sex") + ": " + _("female") + " " + _("ECG") + " " + _("date") + ": 18/10/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient007_s0026lre_MyocardialInfarction': _("age") + ": 70 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 29/10/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient007_s0029lre_MyocardialInfarction': _("age") + ": 70 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 31/10/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient007_s0038lre_MyocardialInfarction': _("age") + ": 70 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 07/11/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient007_s0078lre_MyocardialInfarction': _("age") + ": 70 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 17/12/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient008_s0028lre_MyocardialInfarction': _("age") + ": 60 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 30/10/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient008_s0037lre_MyocardialInfarction': _("age") + ": 60 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 06/11/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient008_s0068lre_MyocardialInfarction': _("age") + ": 60 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 05/12/1990 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient037_s0112lre_MyocardialInfarction': _("age") + ": 50 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 24/01/1991 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient037_s0120lre_MyocardialInfarction': _("age") + ": 50 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 30/01/1991 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient104_s0306lre_HealthyControl': _("age") + ": 58 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 13/07/1992 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient159_s0390lre_Hypertrophy': _("age") + ": 73 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 07/01/1993 " + _("Reason for admission") + ": " + _("Hypertrophy"), 
    'patient180_s0374lre_HealthyControl': _("age") + ": 37 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 26/11/1992 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient180_s0475_re_HealthyControl': _("age") + ": 37 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 19/12/1996 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient180_s0476_re_HealthyControl': _("age") + ": 37 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 19/12/1996 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient180_s0477_re_HealthyControl': _("age") + ": 37 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 19/12/1996 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient180_s0490_re_HealthyControl': _("age") + ": 37 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 18/02/1997 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient180_s0545_re_HealthyControl': _("age") + ": 37 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 07/02/1996 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient248_s0481_re_HealthyControl': _("age") + ": 64 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 07/02/1996 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient251_s0486_re_HealthyControl': _("age") + ": 40 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 21/02/1997 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient251_s0503_re_HealthyControl': _("age") + ": 40 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 04/03/1997 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient251_s0506_re_HealthyControl': _("age") + ": 40 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 04/03/1997 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient264_s0500_re_HealthyControl': _("age") + ": 45 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 27/02/1997 " + _("Reason for admission") + ": " + _("Healthy control"), 
    'patient292_s0555_re_MyocardialInfarction': _("age") + ": 66 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 03/06/1997 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    'patient292_s0556_re_MyocardialInfarction': _("age") + ": 66 " + _("sex") + ": " + _("male") + " " + _("ECG") + " " + _("date") + ": 03/06/1997 " + _("Reason for admission") + ": " + _("Myocardial infarction"), 
    }

def listFiles(dl=False):
    
    res = glob.glob(EKGIMPDIR + "*.csv", recursive=False)
    startidx = len(EKGIMPDIR)
    res = sorted(res)
    ar = []

    for file in res:
        fname = file[startidx:-4].strip()
#        fname = file[8:-4].strip()
        if dl == False:  
            ar.append(fname)
        elif fname not in data_names.keys():  
#        print("FILE", file)      
            ar.append(fname)

    return ar           

def on_dist():
    st.session_state.PQRSTaveragedist = 0    
def on_change():
#    print("ON CHAGE")
#    st.session_state.PQRSTinit = False
    pass
def on_data():
#    print("ON DATA")
    st.session_state.PQRSTinit = True
    st.session_state.PQRSTaveragedist = 0
def on_rate():
#    print("ON RATE")
    st.session_state.PQRSTinit = True
    st.session_state.PQRSTaveragedist = 0

    
def main(): 
    algorithms = ('christov2004', 'elgendi2010', 
#                  'engzeemod2012', 
                  'gamboa2008', 'hamilton2002', 'kalidas2017', 
#                  'koka2022', 
                  'manikandan2012', 'martinez2004', 
#                  'nabian20', 
                  'neurokit',  'pantompkins1985', 
                  'promac', 'rodrigues2021', 'zong2003')
    
    ekg_datas = listFiles()
    if not ekg_datas:
        return
    
#    ekg_datas = ('bio_eventrelated_100hz', 
#                  'bio_resting_8min_100hz', 
#                  'bio_resting_5min_100hz')
    with st.container(horizontal=True, horizontal_alignment="left"):
        pause_sel = st.radio(_(" "), (_("Pause"), _("Run")), key = "itao_pause", horizontal=True, index=0)
        rate_sel = st.number_input(_("Sample rate"), on_change=on_rate, value=1000, placeholder=_("Sample rate"), min_value=100, max_value=3000, step=100) 
        dist_sel = st.number_input(_("Distance between navel and fossa jugularis"), value=41.0, placeholder=_("Distance between navel and fossa jugularis"), 
                                   on_change=on_dist, min_value=5.0, max_value=100.0, step=0.1) 
    with st.container(horizontal=True, horizontal_alignment="left"):
#        alg_sel =  'manikandan2012' # 'neurokit' 
        alg_sel = st.selectbox(label=_("Algorithm"), on_change=on_data, options=algorithms, key="itao_algs", index=10)    
        data_sel = st.selectbox(label=_("Data name"), on_change=on_data, options=ekg_datas, key="itao_datas")
        sig_sel = st.radio(_("Plot"), ("PQRST", "BLOOD", "SIGNAL"), on_change=on_change, key = "itao_sig", horizontal=True, index=0)
    if sig_sel== "PQRST":
        st.session_state.PQRSTsigidx = 0 
    if sig_sel== "BLOOD":
        st.session_state.PQRSTsigidx = 1 
    if sig_sel== "SIGNAL":
        st.session_state.PQRSTsigidx = 2
    
    def run_algorithm(): 
#        print("Selected algorithm: {}".format(alg_sel))
#        print("Data name {}".format(data_sel))
#        print("Sample rate {}".format(rate_sel))
        if "PRQSTdataname" not in st.session_state:
#            st.session_state.PQRSTinit = True
            st.session_state.PQRSTdataname = data_sel
            st.session_state.PRQSTrate = rate_sel
            st.session_state.PQRSTdist = dist_sel
#            st.session_state.PQRSTaveragedist = 0

        msg(_("Run") + " " + _("Algorithm") + " " +  alg_sel + ", " + _("Data") + " " + data_sel + ", " + _("Rate") + " " + str(rate_sel) + ", " + sig_sel)
        if data_sel in data_names.keys():
            msg(_("Patient") + " " + data_names[data_sel])

        draw_image(st.session_state.PQRSTpauseidx, alg_sel, data_sel, rate_sel)
        
        return None
        
    if pause_sel == _("Pause"):
        st.session_state.PQRSTpauseidx = 0
    elif pause_sel == _("Run"):
        st.session_state.PQRSTpauseidx = 1
        run_algorithm()
      
    st.write(pqrst[st.session_state.itaolang])

def imp_main():      
    uploaded_file = st.file_uploader(label=_("Upload"), key="itao_imp", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.to_csv(EKGIMPDIR+uploaded_file.name, index=False)
        msg(_("Success"))

def exp_main(): 
    data_names = listFiles()    
    if not data_names:
        return

    with st.container(horizontal=True, horizontal_alignment="left"):
        data_sel = st.selectbox(label=_("Data name"), options=data_names, key="itao_datas_exp")    
            
    def run_exp(dname): 
        df = pd.read_csv(EKGIMPDIR + dname + ".csv")
        csv = df.to_csv().encode("utf-8")
        
        st.download_button(
            label=_("Download") + " CSV",
            data=csv,
            file_name=dname+".csv",
            mime="text/csv",
            icon=":material/download:",
        )
    
    run_exp(data_sel)
        
def del_main(): 
    data_names = listFiles(True)
    if not data_names:
        return

    with st.container(horizontal=True, horizontal_alignment="left"):
        data_sel = st.selectbox(label=_("Data name"), options=data_names, key="itao_datas_del")        
            
    def run_del(dname): 
        os.unlink(EKGIMPDIR+dname+".csv")
        msg(_("Success"))
    
    db = st.button(label=_("Delete"))
    if db:
        run_del(data_sel)
    
              
if __name__ == '__main__':
    
    tab1, tab2, tab3, tab4 = st.tabs([_("PQRST"), _("Export"), _("Import"), _("Delete"), ])
    with tab1:
        main()
    with tab2:
        exp_main()
    with tab3:
        imp_main()
    with tab4:
        del_main()
     
            
