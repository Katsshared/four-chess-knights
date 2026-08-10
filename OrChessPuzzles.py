
import streamlit as st
import gettext

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

st.title(_("Chess puzzles"))

puzzles = {
        "NONE" : "",
        "ONE MOVE" : "",
        "TWO MOVES" : "",
        "ALL" : "",
        "0001w1" : "1. ♖a2a8",
        "0002w1" : "1. ♖a1a8",
        "0079b1" : "1. ♛d8h4",
        "0080b1" : "1. ♞d4f3",
        "0271w2" : "1. ♗d2g5 2. ♖d1d8",
        "0272w2" : "1. ♗d2a5 2. ♖d1d8",        
    }

puzzles2 = {
        "NONE" : "",
        "THREE MOVES" : "",
        "FOUR MOVES" : "",
        "ALL" : "",
        "0321w3" : "1. ♔a4b4 2. ♔b4b3 3. ♕c4f1",
        "0322w3" : "a) 1. ♙d7d8♗ ♚f7e8 2. ♖g5f5 ♚e8d8 3. ♖f5f8 "
                    "b) 1. ♙d7d8♗ ♚f7f8 2. ♔d6e6 ♚f8e8 3. ♖g5g8",
        "0323w3" : "1. ♘b4c6 2. ♔g1f2 3. ♕h5f3",
        "0324w3" : "a) 1. ♕c3c5 2. ♕c5e5 3. ♙e7e8♕ "
                    "b) 1. ♕c3c5 2. ♙e7e8♕ 3. ♕c5e5",
        "0701w4" : "1. ♙g2g3 2. ♔f6f7 3. ♙g7g8♕  4. ♕g8g6",
        "0702w4" : "a) 1. ♔e7f6 ♜b5b6 2. ♔f6f7 ♜b6f6 3. ♔f7f6 ♚h8h7 4. ♕g2g7 "
                    "b) 1. ♔e7f6 ♜b5b6 2. ♔f6f7 ♜b6b7 3. ♕g2b7 ♚h8h7 4. ♕g2h1",
        "0703w4" : "1. ♔a4b3 2. ♕c8d7 3. ♕d7c7 4. ♕c7b7",
}

puzzles3 = {
        "NONE" : "",
        "FIVE MOVES" : "",
        "SIX MOVES" : "",
        "ALL" : "",
        "0889w5" : "a) 1. ♕a3f8 ♚f1e1 2. ♕f8d6 ♚e1f2 3. ♕d6f4 ♚f2e1  4. ♕f4d4 ♚e1f1 5. ♕d4g1 "
                    "b) 1. ♕a3f8 ♚f1e1 2. ♕f8d6 ♚e1f1 3. ♕d6f4 ♚f2e1  4. ♕f4d4 ♚e1f1 5. ♕d4g1",        
        "0890w5" : "a) 1. ♕c3d2 ♚b1a1 2. ♕d2c1 ♞a2b1 3. ♔e1d2 ♟b3b2 4. ♕c1d1 ♚a1a2 5. ♕d1a4 "
                    "b) 1. ♕c3d2 ♚d1a1 2. ♕d2c1 ♞a2b1 3. ♔e1d2 ♚a1a2 4. ♕d2c3 ... 5. ♕c1b2",        
        "0937w5" : "a) 1. ♖f8a8 ♟b7b5 2. ♙c5b6 ♟d7d5 3. ♙b6b7 ♟d5d4 4. ♙b7b8♗ ♚g7g8 5. ♗b8e5 "
                    "b) 1. ♖f8a8 ♟d7d5 2. ♙c6d6 ♟b7b5 3. ♙d6d7 ♟b5b4 4. ♙d7d8♘ ♚g7g8 5. ♘d8e6",       
        "0938w6" : "a) 1. ♔g7f8 ♟d6d5 2. ♙e4d5 ♚g6f5 3. ♔f8f7 ♚f5e5 4. ♔f7g6 ♚e5d6 5. ♗g7h6 ♚d6e7 6. ♗h6f8 "
                    "b) 1. ♔g7f8 ♟d6d5 2. ♙e4d5 ♚g6f5 3. ♔f8f7 ♚f5e5 4. ♔f7g6 ♚e5d6 5. ♗g7h6 ♚d6e5 6. ♗h6f4",
        "0939w6" : "a) 1. ♗g5h4 ♜d4d1 2. ♗h4g3 ♜d1c1 3. ♗g3f4 ♜c1c2 4. ♗f4g5 ♝g4... 5. ♗g5d8 ♜c2c7 6. ♗d8c7 "
                    "b) 1. ♗g5h4 ♜d4d1 2. ♗h4g3 ♜d1c1 3. ♗g3f4 ♜c1c2 4. ♗f4g5 ♜c2c1 5. ♗g5d7 ♜c1c3 6. ♗d2c3",        
        "0940w6" : "1. ♖g2g6 ♝f6h8 2. ♖g6g7 ♝h8g7 3. ♕e3g1 ♜b2b1 4. ♕g1g7 ♜b1b2 5. ♕g7d4 ♚a1b1 6.♕d4d1 ",
    }
    
def renderDesc(flag, key, puzzles, show = False):
    if key not in [ "NONE", "ALL", "ONE MOVE", "TWO MOVES", 
                   "THREE MOVES", "FOUR MOVES", "FIVE MOVES", "SIX MOVES", ]:
        ending = " (" + key[0:4] + ")"
        if key[4] == "w":
            hd = _("White to mate in") + " " + key[5] + " " + _("moves") + ending
        elif key[4] == "b":
            hd = _("Black to mate in") + " " + key[5] + " " + _("moves") + ending

        st.header(hd)

        if show:
            st.header(puzzles[key]) 
        
        pd = ""
        if flag > 1:
            pd = str(flag)
        st.image("puzzles" + pd + "/" + key + ".png")              


def renderMoves(flag, mv, puzzles, show = False):
    for key in puzzles.keys():
        if len(key) == 6 and key[5] == mv:
            renderDesc(flag, key, puzzles, show)
    
    
def selectPuzzles(flag, puzzle_sel, puzzles, show = False):       
    if puzzle_sel == "NONE":
        pass
    elif puzzle_sel == "ALL":
        for key in puzzles.keys():
            renderDesc(flag, key, puzzles, show)
    elif puzzle_sel == "ONE MOVE":
        renderMoves(flag, "1", puzzles, show)
    elif puzzle_sel == "TWO MOVES":
        renderMoves(flag, "2", puzzles, show)
    elif puzzle_sel == "THREE MOVES":
        renderMoves(flag, "3", puzzles, show)
    elif puzzle_sel == "FOUR MOVES":
        renderMoves(flag, "4", puzzles, show)
    elif puzzle_sel == "FIVE MOVES":
        renderMoves(flag, "5", puzzles, show)
    elif puzzle_sel == "SIX MOVES":
        renderMoves(flag, "6", puzzles, show)
    else:
        renderDesc(flag, puzzle_sel, puzzles, show)
     
 
tab1, tab2, tab3 = st.tabs(["I-II", "III-IV", "V-VI",])
with tab1:
    puzzle_sel = st.selectbox(label=" ", options=puzzles.keys(), key=1)    
    agree = st.checkbox(label=_("Show solution"), key=12)

    selectPuzzles(1, puzzle_sel, puzzles, agree)
with tab2:
    puzzle_sel2 = st.selectbox(label=" ", options=puzzles2.keys(), key=2)    
    agree2 = st.checkbox(label=_("Show solution"), key=22)

    selectPuzzles(2, puzzle_sel2, puzzles2, agree2)
with tab3:
    puzzle_sel3 = st.selectbox(label=" ", options=puzzles3.keys(), key=3)    
    agree3 = st.checkbox(label=_("Show solution"), key=32)

    selectPuzzles(3, puzzle_sel3, puzzles3, agree3)
     

