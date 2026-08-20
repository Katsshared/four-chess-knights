
import pyvips

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw


import chess
import chess.svg

import stockfish as stf

import gettext
import sys
#st.status("PLATFORM "+ sys.platform)

print("PLATFORM "+ sys.platform)
if sys.platform == "win32":
    STOCKFISHAPP = 'C:/Data/SW/Stockfish/stockfish-windows-x86-64-avx2.exe'
elif sys.platform == "linux":
    STOCKFISHAPP = './stockfish-ubuntu-x86-64-avx2'

PLAYSTFILENAME = "playst.png"

if "sellang" not in st.session_state:
    st.session_state.sellang ="en"

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 


def get_titlest():
    wb = ""
    depth =""
    if "depthst" in st.session_state:
        depth = " " + _("Depth") + " " + str(st.session_state.depthst)
    if "colorst" in st.session_state:
        wb = _("White") if st.session_state.colorst == chess.WHITE else _("Black")
    
    title = _("Play") + " " + _("chess") + " " + wb + depth

    return title

st.title(get_titlest())

def get_boardst():
    board_st = chess.Board()
    return board_st

if "boardst" not in st.session_state:
    st.session_state.boardst = get_boardst()

stockfi = stf.Stockfish(path=STOCKFISHAPP)

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
    for i, move in enumerate(st.session_state.historyst):
        text = ""
        if i % 2 == 0:
            text = f"{j}. {move}"
        else:
            text = f" {move}"
            j = j + 1            
        ls.append(text)
    st.markdown(ls)
#    print(st.session_state.historyst)

def addHistory(move, ai=True):
    if ai:
        st.session_state.historyst.append(f"AI: {move.uci()} ")
    else:
        st.session_state.historyst.append(f"Human: {move.uci()} ")
               
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

def setFenStockfish(board):
    stockfi.set_fen_position(board.fen())
#    print("FEN=", stockfi.get_fen_position())

    
def get_ai_move(board):
    setFenStockfish(board)
    stockfi.set_depth(st.session_state.depthst)
    print("Depth", st.session_state.depthst)
    bm = stockfi.get_best_move()
#    print("BEST MOVE", bm)
    
    return bm

def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        st.iframe(svg_string)


def saveBoard(board):
    img = pyvips.Image.new_from_buffer(chess.svg.board(board).encode(), "")
    img.pngsave(PLAYSTFILENAME)


def updateBoard(board, save = True):
    bd = st.session_state.setboardst
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
    bd = st.session_state.setboardst

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
    bd = st.session_state.setboardst
    
    if fr == to:
        return None
    (pfr, cfr) = bd[fr]
    (pto, cto) = bd[to]
    if cfr != st.session_state.colorst:
        return None
     
    move = chess.Move(fr, to)  
    cast = isMoveCastling(board, move)
    if cast:
        if st.session_state.colorst == chess.WHITE:
            if to == 6:
                bd[to - 1] = bd[to + 1]
                bd[to + 1] = (None, None)
            elif to == 2:
                bd[to + 1] = bd[to - 2]
                bd[to - 2] = (None, None)
        elif st.session_state.colorst == chess.BLACK:
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
    return 1
    
def add_point():
    board = st.session_state.boardst    
    if board.is_game_over():
        return
    
    rv = st.session_state["pil"]
    print("pil ", rv)
    off = 15
    for key in ["x1", "x2" , "y1", "y2"]:
        if rv[key] < off or rv[key] > rv["width"] - off or rv[key] > rv["height"] - off:
            return
    rv = makeMove(board, rv["x1"], rv["y1"], rv["x2"], rv["y2"])
    if rv == None:
        return
    
#    print("POS=", stockfi.get_fen_position())
#    print("BPOS=", board.fen())

#    setFenStockfish(board)
    ai_move_uci = get_ai_move(board)
#    ai_move_uci = showStatus(get_ai_move, board, _("AI thinking ..."), None)
#    showStatus(None, None, _("AI: " + str(ai_move_uci)))
    if stockfi.is_move_legal(ai_move_uci):
        ai_move = chess.Move.from_uci(ai_move_uci)
        
        pr = chess.QUEEN
        prom = isMovePromotion(board, ai_move)
        if prom:
            pr = choosePromotion()
            ai_move = chess.Move(ai_move.from_square, ai_move.to_square, promotion=pr)
            bd = st.session_state.setboardst
            pfr, cfr = bd[ai_move.from_square]
            bd[ai_move.to_square] = (pr, cfr)

        board.push(ai_move)
        makeUciMove(board, ai_move_uci, prom)
        addHistory(ai_move)

#        print("AI MOVE ", ai_move_uci)

    if board.is_game_over():
        showStatus(None, None, _("GAME OVER!"))

    
def set_board(board, side = chess.WHITE):    
    bd = makeBoard(board, side)    
    # Convert an SVG file to PNG using the default save options
    saveBoard(board)
    
    return bd   
    
def selectBlackWhite(board):
    if "colorst" not in st.session_state:
        sel = {"NONE":None, _("White"):chess.WHITE, _("Black"):chess.BLACK}
        bw = st.radio(_("Choose White or Black"), sel.keys(), key = "st", horizontal=True)
        depth = st.slider(_("Depth"), 1, 20, 1)

        if sel[bw] in [chess.WHITE, chess.BLACK]:    
            
            if "setboardst" not in st.session_state:
                bd = set_board(board, bw)    
                st.session_state.setboardst = bd
                st.session_state.colorst = sel[bw]
                st.session_state.historyst = []
                st.session_state.depthst = depth
        #        print(bd)
        
                if sel[bw] == chess.BLACK:
        #            setFenStockfish(board)
                    ai_move_uci = get_ai_move(board)
#                    showStatus(None, None, _("AI: " + str(ai_mo
#                    ai_move_uci = showStatus(get_ai_move, board, _("AI thinking ..."))
#                    showStatus(None, None, _("AI: " + str(ai_move_uci)))
                    if stockfi.is_move_legal(ai_move_uci):
                        ai_move = chess.Move.from_uci(ai_move_uci)
                       
                        pr = chess.QUEEN
                        prom = isMovePromotion(board, ai_move)
                        if prom:
                            pr = choosePromotion()
                            ai_move = chess.Move(ai_move.from_square, ai_move.to_square, promotion=pr)
                            bd = st.session_state.setboardst
                            pfr, cfr = bd[ai_move.from_square]
                            bd[ai_move.to_square] = (pr, cfr)

                        board.push(ai_move)
                        makeUciMove(board, ai_move_uci, prom)
                        addHistory(ai_move)
 
#                        print("FIRST AI MOVE ", ai_move_uci)
                            
                main() 
                st.rerun()                      
    else:
        main()
    
       
def main():    
#    human_color = st.session_state.colorst
#    print(f"You are playing as {'White' if human_color == chess.WHITE else 'Black'}")

    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
    
        try:                
            streamlit_image_coordinates(
                PLAYSTFILENAME,
                key="pil",
                click_and_drag=True,
                on_click=add_point
                )

            fname = "GameVsStockfish.txt"
            file = open(fname, 'w')
            file.writelines(st.session_state.historyst)
            file.close()
            
            with open(fname, "r") as file:
                st.download_button(
                    label=_("Download"),
                    data=file,
                    file_name=fname,
                    mime="text/txt"
                )                                   
        except Exception as e:
            st.error(f"Failed:\n {e}")
#            print(f"Failed to coor:\n {e}")
            
        with col2:
            showHistory()

        
if __name__ == '__main__':
    selectBlackWhite(st.session_state.boardst)
