
import pyvips

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import chess
import chess.pgn

import gettext

GAMEPGNFILENAME = "gamepgn.png"
VIDEO_URL = "https://www.youtube.com/watch?v=1FLIthk5nag"


if "sellang" not in st.session_state:
    st.session_state.sellang ="en"

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

en_tenpr = _('''
In a rematch of six games (May 3-11, 1997) against Kasparov, Deep Blue prevailed with 3.5:2.5 points.
This marked the first time a computer had won a match under tournament conditions against the reigning world chess champion.
'''
)
de_tenpr = _('''
In einem Rematch aus sechs Partien (3. bis 11. Mai 1997) gegen Kasparov gewann Deep Blue mit 3,5:2,5 Punkten die Oberhand. 
Damit hatte zum ersten Mal ein Computer einen Wettkampf unter Turnierbedingungen gegen den amtierenden Schachweltmeister gewonnen.
'''
)
ru_tenpr = _('''
В матче-реванше из шести партий (3-11 мая 1997 г.) против Каспарова Deep Blue одержал победу со счетом 3,5:2,5. 
Это был первый случай, когда компьютер выиграл матч в турнирных условиях у действующего чемпиона мира по шахматам.
'''
)
ua_tenpr = _('''
У матчі-реванші з шести партій (3-11 травня 1997 року) проти Каспарова, Deep Blue переміг з рахунком 3,5:2,5 очка. 
Це був перший випадок, коли комп'ютер виграв матч в умовах турніру проти чинного чемпіона світу з шахів.
'''
)
tenpr = {"en":en_tenpr, "de":de_tenpr, "ru":ru_tenpr, "ua":ua_tenpr, }

en_champ = _('''
World Chess Championship
'''
)
de_champ = _('''
Schachweltmeisterschaft
'''
)
ru_champ = _('''
Чемпионат мира по шахматам
'''
)
ua_champ = _('''
Чемпіонат світу з шахів
'''
)
champ = {"en":en_champ, "de":de_champ, "ru":ru_champ, "ua":ua_champ, }

games = {
        "KasparovVsDeepBlue_6" : "",
        "KasparovVsDeepBlue_5" : "",
        "KasparovVsDeepBlue_4" : "",
        "KasparovVsDeepBlue_3" : "",
        "KasparovVsDeepBlue_2" : "",
        "KasparovVsDeepBlue_1" : "",
    }

st.title(_("Watch"))

def get_boardga():
    board_ga = chess.Board()
    return board_ga

if "boardga" not in st.session_state:
    st.session_state.boardga = get_boardga()

    
def showHistory():
    ls = []
    j = 1
    for i, move in enumerate(st.session_state.historyga):
        text = ""
        if i % 2 == 0:
            text = f"{j}. {move}"
        else:
            text = f" {move}"
            j = j + 1            
        ls.append(text)
    st.markdown(ls)
#    print(st.session_state.historyga)

def delHistory(move):
    h = st.session_state.historyga
    del h[st.session_state.indexga]
    
def addHistory(move):
    st.session_state.historyga.append(f"{move.uci()}")
              
def clearBoard(board):
    board.clear()
    bd = {x: (None, None) for x in range(64)} 
    return bd
      
def makeBoard(board, clr0 = chess.WHITE):
#    print("MAKE BOARD")
    bd = clearBoard(board)
    
    clr1 = chess.WHITE 
    clr2 = chess.BLACK 
    if clr0 == chess.BLACK:
        clr1 = chess.BLACK 
        clr2 = chess.WHITE
        
    for i in range(0, 64):
        if i > 7 and i < 16:
            bd[i] = (chess.PAWN, clr1)
            board.set_piece_at(i, chess.Piece(chess.PAWN, clr1))
        if i == 0 or i == 7:
            bd[i] = (chess.ROOK, clr1)
            board.set_piece_at(i, chess.Piece(chess.ROOK, clr1))
        if i == 1 or i == 6:
            bd[i] = (chess.KNIGHT, clr1)
            board.set_piece_at(i, chess.Piece(chess.KNIGHT, clr1))
        if i == 2 or i == 5:
            bd[i] = (chess.BISHOP, clr1)
            board.set_piece_at(i, chess.Piece(chess.BISHOP, clr1))
        if i == 3:
            bd[i] = (chess.QUEEN, clr1)
            board.set_piece_at(i, chess.Piece(chess.QUEEN, clr1))
        if i == 4:
            bd[i] = (chess.KING, clr1)
            board.set_piece_at(i, chess.Piece(chess.KING, clr1))
        if i > 47 and i < 56:
            bd[i] = (chess.PAWN, clr2)
            board.set_piece_at(i, chess.Piece(chess.PAWN, clr2))
        if i == 56 or i == 63:
            bd[i] = (chess.ROOK, clr2)
            board.set_piece_at(i, chess.Piece(chess.ROOK, clr2))
        if i == 57 or i == 62:
            bd[i] = (chess.KNIGHT, clr2)
            board.set_piece_at(i, chess.Piece(chess.KNIGHT, clr2))
        if i == 58 or i == 61:
            bd[i] = (chess.BISHOP, clr2)
            board.set_piece_at(i, chess.Piece(chess.BISHOP, clr2))
        if i == 59:
            bd[i] = (chess.QUEEN, clr2)
            board.set_piece_at(i, chess.Piece(chess.QUEEN, clr2))
        if i == 60:
            bd[i] = (chess.KING, clr2)
            board.set_piece_at(i, chess.Piece(chess.KING, clr2))
    return bd


def dummyMove(board):
    move = chess.Move.from_uci("e2e4")
    board.push(move)
    board.pop()

def saveBoard(board):
    img = pyvips.Image.new_from_buffer(chess.svg.board(board).encode(), options="")
    img.pngsave(GAMEPGNFILENAME)
 
    
def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        st.iframe(svg_string)

def popMove(board):
    moves = st.session_state.movesga
    idx = st.session_state.indexga
#    print("POP", moves[idx])
    board.pop()
    delHistory(moves[idx])
    st.session_state.actionga = -1
    saveBoard(board)

def pushMove(board):
    moves = st.session_state.movesga
    idx = st.session_state.indexga
    move = moves[idx]
#    print("PUSH", move)
    board.push(move)
    addHistory(move)
    st.session_state.actionga = +1
    saveBoard(board)
    
def stepGame(board, step=1):
#    st.logo("images/FourKnights.png")
    idx = st.session_state.indexga
    moves = st.session_state.movesga
    size = len(moves)
    act = st.session_state.actionga
#    print("IDX ACT SIZE", idx, act, size)

    
    if act == 0:
        if idx == 0 and step < 0:
            return            
        elif idx == size - 1 and step > 0:
            return
            
    if step < 0:
        if act >= 0:
            popMove(board)            
        elif act < 0:
            if idx > 0:
                st.session_state.indexga = idx - 1          
                popMove(board)
        if st.session_state.indexga < 0:
            st.session_state.indexga = 0
    elif step > 0:
        if act <= 0:
            pushMove(board)            
        elif act > 0:    
            if idx < size - 1:       
                st.session_state.indexga = idx + 1
                pushMove(board)            
        if st.session_state.indexga > size - 1:
            st.session_state.indexga = size - 1    

def initGame(board):
    set_board(board)
    
    st.session_state.indexga = 0
    st.session_state.actionga = 0
    st.session_state.historyga = []

    
def endGame(board):
    initGame(board)
    moves = st.session_state.movesga
    size = len(moves)

    for i in range(0, size):
        board.push(moves[i])
        addHistory(moves[i])
    
    st.session_state.actionga = 0
    st.session_state.indexga = size -1
    
    saveBoard(board)
    
    
#    for move in moves:
#        print("PUSH", move)
#        board.push(move)
#        fr_pc = board.piece_at(move.from_square)
#        to_pc = board.piece_at(move.to_square)
#        board.set_piece_at(move.to_square, fr_pc)
#       board.remove_piece_at(move.from_square)
       
    
def add_point():
    rv = st.session_state["pil"]
#    print(rv)

def set_board(board, side = chess.WHITE):    
    bd = makeBoard(board, side)    
    # Convert an SVG file to PNG using the default save options
    saveBoard(board)
    
    return bd   

def selectGame(game_sel):
    moves = None
    if "gamega" not in st.session_state or game_sel != st.session_state.gamega:
        print("SELECT GAME", game_sel)
        with open("games/"+game_sel+".pgn", "r") as file: 
            game = chess.pgn.read_game(file)
            moves = [move for move in game.mainline_moves()]
        
        st.session_state.headerga = game.headers["White"]+" vs "+game.headers["Black"]
        st.session_state.gamega = game_sel
        st.session_state.movesga = moves
        st.session_state.indexga = 0
        st.session_state.actionga = 0
        st.session_state.historyga = []
        
        initGame(st.session_state.boardga)

    return moves      
    
def main(board):
                                 
    st.write(tenpr[st.session_state.sellang])   

    game_sel = st.selectbox(label=" ", options=games.keys(), key=1)    
    selectGame(game_sel)
                
    st.header(st.session_state.headerga)
              
    if "setboardga" not in st.session_state:
        bd = set_board(board)    
        st.session_state.setboardga = bd

    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
    
        try:
                
            streamlit_image_coordinates(
                GAMEPGNFILENAME,
                key="pil",
                click_and_drag=True,
                on_click=add_point
                )

            with st.container(horizontal=True, horizontal_alignment="left"):
                bb = st.button("|<-")
                bl = st.button("<-")
                br = st.button("->")
                be = st.button("->|")
                if bb: initGame(board)
                if be: endGame(board)
                if bl: stepGame(board, -1)
                if br: stepGame(board)
                
                fname = "games/" + game_sel + ".pgn"
                with open(fname, "r") as file:
                    st.download_button(
                        label=_("Download"),
                        data=file,
                        file_name=game_sel + ".pgn",
                        mime="text/pgn"
                    )
                    
            st.video(VIDEO_URL)
            
            st.header(champ[st.session_state.sellang])

 #            st.page_link(f"", label="", icon="")
            st.page_link(f"https://en.wikipedia.org/wiki/World_Chess_Championship", label="World Chess Championship", icon="🌎")
            st.page_link(f"https://en.wikipedia.org/wiki/Gukesh_Dommaraju", label="Gukesh Dommaraju, India, 2024-2026", icon="🇮🇳")
            st.page_link(f"https://en.wikipedia.org/wiki/Ding_Liren", label="Ding Liren, China, 2023-2024", icon="🇨🇳")
            st.page_link(f"https://en.wikipedia.org/wiki/Magnus_Carlsen", label="Magnus Carlsen, Norway, 2013-2023", icon="🇳🇴")
            st.page_link(f"https://en.wikipedia.org/wiki/Viswanathan_Anand", label="Viswanathan Anand, India, 2007-2013", icon="🇮🇳")
            st.page_link(f"https://en.wikipedia.org/wiki/Vladimir_Kramnik", label="Vladimir Kramnik, Russia, 2006-2007", icon="🇷🇺")
            st.page_link(f"https://en.wikipedia.org/wiki/Veselin_Topalov", label="Veselin Topalov, Bulgaria, 2005-2006", icon="🇧🇬")
            st.page_link(f"https://en.wikipedia.org/wiki/Rustam_Kasimdzhanov", label="Rustam Kasimdzhanov, Uzbekistan, 2004-2005", icon="🇺🇿")
            st.page_link(f"https://en.wikipedia.org/wiki/Ruslan_Ponomariov", label="Ruslan Ponomariov, Ukraine, 2002-2004", icon="🇺🇦")
            st.page_link(f"https://en.wikipedia.org/wiki/Viswanathan_Anand", label="Viswanathan Anand, India, 2000-2002", icon="🇮🇳")
            st.page_link(f"https://en.wikipedia.org/wiki/Alexander_Khalifman", label="Alexander Khalifman, Russia, 1999-2000", icon="🇷🇺")
            st.page_link(f"https://en.wikipedia.org/wiki/Anatoly_Karpov", label="Anatoly Karpov, Russia, 1993-1999", icon="🇷🇺")
            st.page_link(f"https://en.wikipedia.org/wiki/Garry_Kasparov", label="Garry Kasparov, 🟥-🇷🇺 Soviet Union-Russia, 1985-1993", icon="🇷🇺")
            st.page_link(f"https://en.wikipedia.org/wiki/Anatoly_Karpov", label="Anatoly Karpov, Soviet Union, 1975-1985", icon="🟥")
            st.page_link(f"https://en.wikipedia.org/wiki/Bobby_Fischer", label="Bobby Fischer, United States, 1972-1975", icon="🇺🇸")
            st.page_link(f"https://en.wikipedia.org/wiki/Boris_Spassky", label="Boris Spassky, Soviet Union, 1969-1972", icon="🟥")
            st.page_link(f"https://en.wikipedia.org/wiki/Tigran_Petrosian", label="Tigran Petrosian, Soviet Union, 1963-1969", icon="🟥")
            st.page_link(f"https://en.wikipedia.org/wiki/Mikhail_Botvinnik", label="Mikhail Botvinnik, Soviet Union, 1961-1963", icon="🟥")
            st.page_link(f"https://en.wikipedia.org/wiki/Mikhail_Tal", label="Mikhail Tal, Soviet Union, 1960-1961", icon="🟥")
            st.page_link(f"https://en.wikipedia.org/wiki/Mikhail_Botvinnik", label="Mikhail Botvinnik, Soviet Union, 1958-1960", icon="🟥")
            st.page_link(f"https://en.wikipedia.org/wiki/Vasily_Smyslov", label="Vasily_Smyslov, Soviet Union, 1957-1958", icon="🟥")
            st.page_link(f"https://en.wikipedia.org/wiki/Mikhail_Botvinnik", label="Mikhail Botvinnik, Soviet Union, 1948-1957", icon="🟥")
            st.page_link(f"https://en.wikipedia.org/wiki/Alexander_Alekhine", label="Alexander Alekhine, 🇷🇺-🇫🇷 Russia-France, 1937-1946", icon="🇫🇷")
            st.page_link(f"https://en.wikipedia.org/wiki/Max_Euwe", label="Max Euwe, Netherlands, 1935-1937", icon="🇳🇱")
            st.page_link(f"https://en.wikipedia.org/wiki/Alexander_Alekhine", label="Alexander Alekhine, 🇷🇺-🇫🇷 Russia-France, 1927-1935", icon="🇫🇷")
            st.page_link(f"https://en.wikipedia.org/wiki/Jos%C3%A9_Ra%C3%BAl_Capablanca", label="Jose Raul Capablanca, Cuba, 1921-1927", icon="🇨🇺")
            st.page_link(f"https://en.wikipedia.org/wiki/Emanuel_Lasker", label="Emanuel Lasker, Germany, 1894-1921", icon="🇩🇪")
            st.page_link(f"https://en.wikipedia.org/wiki/Wilhelm_Steinitz", label="Wilhelm_Steinitz, 🇦🇹-🇭🇺 Austria-Hungary, United States, 1886–1894", icon="🇺🇸")
   
        except Exception as e:
            st.error(f"Failed:\n {e}")
            
    with col2:
        showHistory()


if __name__ == '__main__':
    main(st.session_state.boardga)
    
    