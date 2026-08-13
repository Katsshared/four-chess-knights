'''

st.page_link("http://www.google.com", label="Google", icon="🌎")
def page_1():
    st.title("Page 1")
    st.page_link("page_2.py", query_params={"utm_source": "page_1"})

pg = st.navigation([page_1, "page_2.py"])
pg.run()

'''
import pyvips

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import chess
import chess.svg

import gettext

PLAYLIFILENAME = "playli.png"

#
# lichess_cli_maia1.py
#
import requests
import json
import time
import OrKatTkn

def  get_token():
    return OrKatTkn.key2 + OrKatTkn.key1

def  get_headers():
    token = get_token()
    return {'Authorization': f'Bearer {token}'}

def listen_for_opponent_move(game_id, headers, board, previous_move_count):
    stream_url = f'https://lichess.org/api/board/game/stream/{game_id}'
    with requests.get(stream_url, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8'))
                if 'moves' in decoded_line:
                    moves = decoded_line['moves'].split()
                    
#                    print("MOVES, LEN", moves, len(moves))
                    opponent_move = chess.Move.from_uci(moves[-1])
                    return opponent_move, len(moves)

#                    if len(moves) > previous_move_count:
#                        last_move = moves[-1]
#                        opponent_move = chess.Move.from_uci(last_move)
#                        return board.san(opponent_move), len(moves)
            time.sleep(1)
    return None, previous_move_count

def resign_game_li(game_id, headers):
    resign_url = f'https://lichess.org/api/board/game/{game_id}/resign'
    try:
        response = requests.post(resign_url, headers=headers)
        return response.ok
    except Exception as e:
        print("Failed to resign:", e)
        return False

def challenge_ai():
    difficulty = st.session_state.difficulty 
    user_color = 'white' if st.session_state.colorli == chess.WHITE else 'black'
    payload = {'level': difficulty, 'color': user_color}

    try:
        response = requests.post('https://lichess.org/api/challenge/ai', headers=get_headers(), data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Failed to start game:", e)
        return None

    game_id = response.json()['id']
    
    return game_id




if "sellang" not in st.session_state:
    st.session_state.sellang ="en"

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

def get_titleli():
    wb = ""
    diff =""
    if "difficulty" in st.session_state:
        diff = " " + _("Difficulty") + " " + str(st.session_state.difficulty)
    else:
        diff = "(LICHESS)"
    if "colorli" in st.session_state:
        wb = _("White") if st.session_state.colorli == chess.WHITE else _("Black")
    
    title = _("Play") + " " + _("chess") + " " + wb + diff

    return title

st.title(get_titleli())

def get_boardli():
    board_li = chess.Board()
    return board_li

if "boardli" not in st.session_state:
    st.session_state.boardli = get_boardli()

#@st.dialog("Choose promotion", dismissible=True)
def choosePromotion():
    sel = { _("Queen"):chess.QUEEN, _("Knight"):chess.KNIGHT, _("Rook"):chess.ROOK, _("Bishop"):chess.BISHOP}
#    with st.popover(_("Choose promotion")):

    return chess.QUEEN

    pr = st.radio(_(""), sel.keys(), key ="my", horizontal=True)
    print(pr)

    rv = sel[pr]
    return rv
    
def showHistory():
    ls = []
    j = 1
    for i, move in enumerate(st.session_state.historyli):
        text = ""
        if i % 2 == 0:
            text = f"{j}. {move}"
        else:
            text = f" {move}"
            j = j + 1            
        ls.append(text)
    st.markdown(ls)
#    print(st.session_state.historyli)

def addHistory(move, ai=True):
    if ai:
        st.session_state.historyli.append(f"AI: {move.uci()}")
    else:
        st.session_state.historyli.append(f"Human: {move.uci()}")
               
def showStatus(func, board, msg, move = ""):
    with st.status("", expanded=False) as status:
        rv = None
        if func != None:
            rv = func(board)
            if move != None:
                status.update(label=move, state="complete", expanded=False)
        else:
            status.update(label=msg + " " + move, state="complete", expanded=False)
        return rv

    
def get_game_id():
    game_id = challenge_ai()
    if not game_id:
        print("No game started.")
        return None

    print(f"Game ID: {game_id}")
    print(f"Watch or play: https://lichess.org/{game_id}")
    print("Type your move in standard notation (e.g., e4, Nf3), 'show' to view the board, 'clock' for remaining time, 'audio' to toggle speech, or 'resign' to resign the game.")

    return game_id
    
def get_ai_move(board, depth=20):
    move_count = 0
    board = st.session_state.boardli
    game_id  = st.session_state.gameid       
    move, move_count = listen_for_opponent_move(game_id, get_headers(), board, move_count)
    
    cast = isMoveCastling(board, move)
    if cast:
        bd = st.session_state.setboardli 
        move_uci = move.uci()
        print("CASTLING", move_uci)    
#        fr = chess.parse_square(move_uci[0] + move_uci[1])
        to = chess.parse_square(move_uci[2] + move_uci[3])

        if st.session_state.colorli == chess.WHITE:
            if to == 6:
                bd[to - 1] = bd[to + 1]
                bd[to + 1] = (None, None)
#                board.remove_piece_at(to + 1)
            elif to == 2:
                bd[to + 1] = bd[to - 2]
                bd[to - 2] = (None, None)
#                board.remove_piece_at(to - 2)
        elif st.session_state.colorli == chess.BLACK:
            if to == 62:
                bd[to - 1] = bd[to + 1]
                bd[to + 1] = (None, None)
#                board.remove_piece_at(to + 1)
            elif to == 58:
                bd[to + 1] = bd[to - 2]
                bd[to - 2] = (None, None)
#                board.remove_piece_at(to - 2)

        board.push(move)
        updateBoard(board)   
        
    return move

def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        st.iframe(svg_string)


def saveBoard(board):
    img = pyvips.Image.new_from_buffer(chess.svg.board(board).encode(), "")
    img.pngsave(PLAYLIFILENAME)


def updateBoard(board, save = True):
    bd = st.session_state.setboardli
#    board.clear()
    for key in bd.keys():
        (pc, cl) = bd[key] 
        if (pc, cl) != (None, None):
            board.set_piece_at(key, chess.Piece(pc, cl))
    if save:        
        saveBoard(board)

              
def clearBoard(board):
    board.clear()
    bd = {x: (None, None) for x in range(64)} 
    return bd
      
def makeBoard(board, clr0 = chess.WHITE):
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

def coors2square(x, y):
    sq_size = 45
    br_size = 30
    col = round((x-br_size)/sq_size)
    row = round((y-br_size)/sq_size)
    sq = chess.square(col, 7 - row) 
#    print("row=", row, " col=", col, " sq=", sq, " ", chess.square_name(sq))
    return sq

def isMoveCastling(board, move):
    if move == None:
        return False
    if (board.piece_at(move.from_square).piece_type == chess.KING and
        move.uci() in ["e1g1", "e1c1", "e8g8", "e8c8"]): 
#        print("CASTLING")
        return True
    
    return False 
       
def isMovePromotion(board, move):
#    print("RANK", chess.square_rank(move.to_square))
    # Handle pawn promotion - give options
    if (board.piece_at(move.from_square).piece_type == chess.PAWN and 
        (chess.square_rank(move.to_square) == 7 or chess.square_rank(move.to_square) == 0)):
#        print("PROMOTION", move.uci())
        return True
    
    return False        
 
def makeUciMove(board, uci_move, prom = False):
    bd = st.session_state.setboardli

#    print("UCI MOVE", uci_move)
    
    fr = chess.parse_square(uci_move[0] + uci_move[1])
    to = chess.parse_square(uci_move[2] + uci_move[3])
    
#    print("fr= ", fr, "to= ", to)

    if prom == False:
        bd[to] = bd[fr]
        
    bd[fr] = (None, None)
    updateBoard(board)
       
def makeMove(board, x1, y1, x2, y2):
    fr = coors2square(x1, y1)
    to = coors2square(x2, y2)
    bd = st.session_state.setboardli
    
    if fr == to:
        return None
    (pfr, cfr) = bd[fr]
    (pto, cto) = bd[to]
    if cfr != st.session_state.colorli:
        return None
     
    move = chess.Move(fr, to)  
    cast = isMoveCastling(board, move)
    if cast:
        if st.session_state.colorli == chess.WHITE:
            if to == 6:
                bd[to - 1] = bd[to + 1]
                bd[to + 1] = (None, None)
            elif to == 2:
                bd[to + 1] = bd[to - 2]
                bd[to - 2] = (None, None)
        elif st.session_state.colorli == chess.BLACK:
            if to == 62:
                bd[to - 1] = bd[to + 1]
                bd[to + 1] = (None, None)
            elif to == 58:
                bd[to + 1] = bd[to - 2]
                bd[to - 2] = (None, None)

    pr = chess.QUEEN
    prom = isMovePromotion(board, move)
    if prom:
        pr = choosePromotion()
        move = chess.Move(move.from_square, move.to_square, promotion=pr)
    elif move not in board.legal_moves and not cast:
            return None
         
    board.push(move)
    addHistory(move, False)

    if prom:
        bd[to] = (pr, cfr)
    else:
        bd[to] = bd[fr]
        
    bd[fr] = (None, None)
    updateBoard(board)
    
    uci_move = move.uci()
    game_id = st.session_state.gameid
    move_url = f'https://lichess.org/api/board/game/{game_id}/move/{uci_move}'
    move_response = requests.post(move_url, headers=get_headers())
    if move_response.status_code != 200:
        print("Failed to send move:", move_response.text)

    return 1
    
def add_point():
    board = st.session_state.boardli    
    if board.is_game_over():
        return
    
    rv = st.session_state["pil"]
#    print("pil ", rv)
    off = 15
    for key in ["x1", "x2" , "y1", "y2"]:
        if rv[key] < off or rv[key] > rv["width"] - off or rv[key] > rv["height"] - off:
            return
    rv = makeMove(board, rv["x1"], rv["y1"], rv["x2"], rv["y2"])
    if rv == None:
        return
    
#    print("POS=", stockfi.get_fen_position())
#    print("BPOS=", board.fen())
    ai_move_uci =  get_ai_move(board)
#    ai_move_uci = showStatus(get_ai_move, board, _("AI thinking ..."), None)
#    showStatus(None, None, _("AI: " + str(ai_move_uci)))
    if (ai_move_uci in board.legal_moves) or isMoveCastling(board, ai_move_uci):
        ai_move = ai_move_uci
#        ai_move = chess.Move.from_uci(ai_move_uci)
        
        pr = chess.QUEEN
        prom = isMovePromotion(board, ai_move)
        if prom:
            pr = choosePromotion()
            ai_move = chess.Move(ai_move.from_square, ai_move.to_square, promotion=pr)
            bd = st.session_state.boardli
            pfr, cfr = bd[ai_move.from_square]
            bd[ai_move.to_square] = (pr, cfr)

        board.push(ai_move)
        makeUciMove(board, ai_move_uci.uci(), prom)
        addHistory(ai_move)

#        print("AI MOVE ", ai_move_uci)
        
    if board.is_game_over():
#        if board.is_game_over() and board.is_checkmate() and board.is_check():
        showStatus(None, None, _("GAME OVER!"))


    
def set_board(board, side = chess.WHITE):    
    bd = makeBoard(board, side)    
    # Convert an SVG file to PNG using the default save options
    saveBoard(board)
    
    return bd   
    
def selectBlackWhite(board):
    if "colorli" not in st.session_state:
        sel = {"NONE":None, _("White"):chess.WHITE, _("Black"):chess.BLACK}
        bw = st.radio(_("Choose White or Black"), sel.keys(), key="li", horizontal=True)
        diff = st.slider(_("Difficulty"), 1, 8, 1)

        if sel[bw] in [chess.WHITE, chess.BLACK]:    
            
            if "setboardli" not in st.session_state:
                bd = set_board(board, bw)    
                st.session_state.setboardli = bd
                st.session_state.colorli = sel[bw]
                st.session_state.historyli = []
                st.session_state.difficulty = diff
                st.session_state.gameid = challenge_ai()
        #        print(bd)

                if sel[bw] == chess.BLACK:
                    
                    ai_move_uci =  get_ai_move(board)
#                    ai_move_uci = showStatus(get_ai_move, board, _("AI thinking ..."))
#                    print("AI MOVE UCI", ai_move_uci)
#                    showStatus(None, None, _("AI: " + str(ai_move_uci)))
                    if ai_move_uci in board.legal_moves:
                        ai_move = ai_move_uci
#                        ai_move = chess.Move.from_uci(ai_move_uci)
#                        ai_move = board.parse_san(ai_move_uci)
                        
                        pr = chess.QUEEN
                        prom = isMovePromotion(board, ai_move)
                        if prom:
                            pr = choosePromotion()
                            ai_move = chess.Move(ai_move.from_square, ai_move.to_square, promotion=pr)
                            bd = st.session_state.boardli
                            pfr, cfr = bd[ai_move.from_square]
                            bd[ai_move.to_square] = (pr, cfr)

                        board.push(ai_move)
                        makeUciMove(board, ai_move_uci.uci(), prom)
                        addHistory(ai_move)
 
#                        print("FIRST AI MOVE ", ai_move_uci)
                            
                main() 
                st.rerun()                      
    else:
        main()

def navLichess(game_id):
    st.page_link(f"https://lichess.org/{game_id}", label="Lichess", icon="🌎")
#    pg = st.navigation([st.Page("https://lichess.org/{game_id}")])
#    pg.run()
    
    
       
def main():    
    
    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
    
        try:                
            streamlit_image_coordinates(
                PLAYLIFILENAME,
                key="pil",
                click_and_drag=True,
                on_click=add_point
                )
            with st.container(horizontal=True, horizontal_alignment="left"):
                game_id = st.session_state.gameid
                st.page_link(f"https://lichess.org/{game_id}", label="LICHESS", icon="🌎")

                with open(PLAYLIFILENAME, "rb") as file:
                    st.download_button(
                        label=_("Download"),
                        data=file,
                        file_name=PLAYLIFILENAME,
                        mime="image/png"
                    )
    
        except Exception as e:
            st.error(f"Failed:\n {e}")
            
        with col2:
            showHistory()

        
if __name__ == '__main__':
    selectBlackWhite(st.session_state.boardli)
