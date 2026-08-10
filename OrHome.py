
import streamlit as st
import gettext
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

st.title(_("About us"))

st.logo("images/FourKnights.png")

st.header(_("We are the Four Chess Knights club"))

#st.image("images/Chessboard.png")

st.write(_("Our mission is to foster children's interest in playing chess."))
st.write(_("We are a children's chess club based at a center for social and integration cooperation."))
st.header(_("Our students' achievements"))
st.write(" 🟢 " + _("Win") +  " 🟡 "   + _("Draw")+ " 🔴 " + _("Loss"))

# importing the module
#        '5' : ["", "", "", "", "", "", "", "", "", "", "", "", "" ],

# creating a DataFrame
dat = {_('Name') : ['Natusja', 'Sasha', 'Misha', 'Ljuba', 'Kiril', 'Matvej', 'Margo', 'Vanja', 'Teo', 'Ilja', 'Milena', 'Jasha', 'Avel'],
            '1' : ["",          "🟢",   "",         "🟡",   "",     "🟢",       "",     "",     "",     "",     "",     "🟢",       "" ],
            '2' : ["🔴",        "",     "🟢",       "",     "",     "",         "",     "🟢",   "",     "🔴",   "",     "",         "" ],
            '3' : ["",          "🔴",   "",         "🔴",   "",     "🔴",       "",     "🟡",   "",     "",     "",     "🟢",       "" ],
            '4' : ["🟡",        "",     "🟢",       "",     "",     "",         "",     "",     "",     "🟢",   "",     "",         "" ],
            '5' : ["",          "",     "",         "",     "",     "🟢",       "",     "🟢",   "",     "",     "🔴",   "🟢",       "🟢" ],
            '6' : ["🔴",        "",     "🟢",       "",     "🔴",   "",         "🟢",   "",     "",     "",     "🟢",   "🟢",       "" ],
            '7' : ["",          "",     "",         "",     "",     "🔴",       "",     "🟢",   "",     "",     "",     "",         "" ],
            '8' : ["",          "🔴",   "🟡",       "",     "🔴",   "",         "🔴",   "",     "",     "",     "",     "🟢",       "" ],
            '9' : ["",          "",     "",         "",     "",     "",         "",     "",     "",     "🟢",   "",     "",         "" ],
            '10' : ["",          "🟢",   "",         "🔴",   "",     "",         "",     "",     "🔴",   "",     "",     "",         "" ],
            '11': ["",          "",     "",         "",     "🟢",   "🔴",       "",     "",     "",     "",     "",     "🟢",       "🟢" ],
            '12': ["🔴",        "",     "🔴",       "",     "🔴",   "🔴",       "",     "🔴",   "",     "",     "🔴",   "",         "🔴" ],
            '13': ["",          "",     "",         "",     "🔴",   "",         "",     "",     "",     "",     "🔴",   "🟢",       "" ],
        }
        
df = pd.DataFrame(dat, index=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'])
st.dataframe(df)  

def calcItems(data, sym):
    score = []
    for i, row in data.iterrows():
        rv = 0
        for key in row.keys():
            if key in [_('Name')]:
                continue
            if row[key] == sym:
                rv = rv + 1
#            print("rv, key, row[key]", rv, key, row[key])
        if rv == 0:
            rv = 0.05          
        score.append(rv)
    return score 

def calcScores(data): 
    score = []
    for i, row in data.iterrows():
        rv = 0
        for key in row.keys():
            if key in [_('Name')]:
                continue
            if row[key] == "🟢":
                rv = rv + 1
            elif row[key] == "🟡":
                rv = rv + 0.5
#            print("rv, key, row[key]", rv, key, row[key])
        if rv == 0:
            rv = 0.05          
        score.append(rv)
    return score 

def makeBars(df):
    barWidth = 0.25
    fig, ax = plt.subplots(figsize =(12, 8)) 
    
    WIN = calcItems(df, "🟢") 
#    print("WIN", WIN)
    DRAW = calcItems(df, "🟡") 
#    print("DRAW", DRAW) 
    LOSS = calcItems(df,"🔴") 
#    print("LOSS", LOSS) 
    
    br1 = np.arange(len(WIN)) 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
    
    plt.bar(br1, WIN, color ='green', width = barWidth, 
            edgecolor ='grey', label = _('Win'))
    plt.bar(br2, DRAW, color ='yellow', width = barWidth, 
            edgecolor ='grey', label = _('Draw')) 
    plt.bar(br3, LOSS, color ='red', width = barWidth, 
            edgecolor ='grey', label = _('Loss'))
    
    plt.xlabel(_('Students'), fontweight ='bold', fontsize = 15) 
    plt.ylabel(_('Win') +  ' ' + _('Draw') + ' ' + _('Loss'), fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth for r in range(len(WIN))], dat[_('Name')])
    
    plt.legend()
    return fig

def makeOneBar(df):
    barWidth = 0.25
    fig, ax = plt.subplots(figsize =(12, 8)) 
    
    SCORES = calcScores(df) 
#    print("WIN", WIN)
    
    br1 = np.arange(len(SCORES)) 
    
    bars = plt.bar(br1, SCORES, color ='blue', width = barWidth, 
            edgecolor ='grey', label = _('Scores'))
    
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=12)

    plt.xlabel(_('Students'), fontweight ='bold', fontsize = 15) 
    plt.ylabel(_('Scores'), fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth for r in range(len(SCORES))], dat[_('Name')])
    
    plt.legend()
    return fig

fig = makeBars(df)
st.pyplot(fig)

fig = makeOneBar(df)
st.pyplot(fig)

