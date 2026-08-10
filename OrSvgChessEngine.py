
import pyvips

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import chess
import chess.svg

import gettext

PLAYFILENAME = "play.png"

PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHTS_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOPS_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOKS_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEENS_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KINGS_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]


def evaluate(board):
    """
    Given a particular board, evaluates it and gives it a score.
    A higher score indicates it is better for white.
    A lower score indicates it is better for black.

    Args:
        board (chess.Board): A chess board.

    Returns:
        int: A score indicating the state of the board (higher is good for white, lower is good for black)
    """    

    boardvalue = 0
    
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    material = 100 * (wp - bp) + 300 * (wn - bn) + 300 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    
    pawn_sum = sum([PAWN_TABLE[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawn_sum = pawn_sum + sum([-PAWN_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
    knight_sum = sum([KNIGHTS_TABLE[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knight_sum = knight_sum + sum([-KNIGHTS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishop_sum = sum([BISHOPS_TABLE[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishop_sum = bishop_sum + sum([-BISHOPS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rook_sum = sum([ROOKS_TABLE[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
    rook_sum = rook_sum + sum([-ROOKS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
    queens_sum = sum([QUEENS_TABLE[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
    queens_sum = queens_sum + sum([-QUEENS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kings_sum = sum([KINGS_TABLE[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
    kings_sum = kings_sum + sum([-KINGS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])
    
    boardvalue = material + pawn_sum + knight_sum + bishop_sum + rook_sum + queens_sum + kings_sum
    
    return boardvalue


def determine_best_move(board, is_white=True, depth = 3):
    """Given a board, determines the best move.

    Args:
        board (chess.Board): A chess board.
        is_white (bool): Whether the particular move is for white or black.
        depth (int, optional): The number of moves looked ahead.

    Returns:
        chess.Move: The best predicated move.
    """
    if "depth" in st.session_state:
        depth = st.session_state.depth
    if "white" in st.session_state:
        is_white = False if st.session_state.white == chess.BLACK else True 

    
    best_move = -100000 if is_white else 100000
    best_final = None
    for move in board.legal_moves:
        board.push(move)
        value = minimax_helper(depth - 1, board, -10000, 10000, not is_white)
        board.pop()
        if (is_white and value > best_move) or (not is_white and value < best_move):
            best_move = value
            best_final = move
            
#    print("BEST FINAL", best_final)
    return best_final

def minimax_helper(depth, board, alpha, beta, is_maximizing):
    if depth <= 0 or board.is_game_over():
        return evaluate(board)

    if is_maximizing:
        best_move = -100000
        for move in board.legal_moves:
            board.push(move)
            value = minimax_helper(depth - 1, board, alpha, beta, False)
            board.pop()
            best_move = max(best_move, value)
            alpha = max(alpha, best_move)
            if beta <= alpha:
                break
        return best_move
    else:
        best_move = 100000
        for move in board.legal_moves:
            board.push(move)
            value = minimax_helper(depth - 1, board, alpha, beta, True)
            board.pop()
            best_move = min(best_move, value)
            beta = min(beta, best_move)
            if beta <= alpha:
                break
        return best_move


if "sellang" not in st.session_state:
    st.session_state.sellang ="en"

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

wb = ""
depth =""
if "depth" in st.session_state:
    depth = " " + _("Depth") + " " + str(st.session_state.depth)
if "white" in st.session_state:
    wb = _("White") if st.session_state.white == chess.WHITE else _("Black")
st.title(_("Play") + " " + _("chess") + " " + wb + depth)

board_one = chess.Board()
if "board" not in st.session_state:
    st.session_state.board = board_one

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
    for i, move in enumerate(st.session_state.history):
        text = ""
        if i % 2 == 0:
            text = f"{j}. {move}"
        else:
            text = f" {move}"
            j = j + 1            
        ls.append(text)
    st.markdown(ls)
#    print(st.session_state.history)

def addHistory(move, ai=True):
    if ai:
        st.session_state.history.append(f"AI: {move.uci()}")
    else:
        st.session_state.history.append(f"Human: {move.uci()}")
               
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

    
def get_ai_move(board, depth=20):
    bm = determine_best_move(board, True)

#    print("GET AI MOVE", bm)
    
    return bm

def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        st.iframe(svg_string)


def saveBoard(board):
    img = pyvips.Image.new_from_buffer(chess.svg.board(board).encode(), "")
    img.pngsave(PLAYFILENAME)


def updateBoard(board, save = True):
    bd = st.session_state.setboard
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
    bd = st.session_state.setboard

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
    bd = st.session_state.setboard
    
    if fr == to:
        return None
    (pfr, cfr) = bd[fr]
    (pto, cto) = bd[to]
    if cfr != st.session_state.white:
        return None
     
    move = chess.Move(fr, to)  
    cast = isMoveCastling(board, move)
    if cast:
        if st.session_state.white == chess.WHITE:
            if to == 6:
                bd[to - 1] = bd[to + 1]
                bd[to + 1] = (None, None)
            elif to == 2:
                bd[to + 1] = bd[to - 2]
                bd[to - 2] = (None, None)
        elif st.session_state.white == chess.BLACK:
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
    board = st.session_state.board    
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

    ai_move_uci = showStatus(get_ai_move, board, _("AI thinking ..."), None)
    showStatus(None, None, _("AI: " + str(ai_move_uci)))
    if ai_move_uci in board.legal_moves:
        ai_move = ai_move_uci
#        ai_move = chess.Move.from_uci(ai_move_uci)
        
        pr = chess.QUEEN
        prom = isMovePromotion(board, ai_move)
        if prom:
            pr = choosePromotion()
            ai_move = chess.Move(ai_move.from_square, ai_move.to_square, promotion=pr)
            bd = st.session_state.setboard
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
    if "white" not in st.session_state:
        sel = {"NONE":None, _("White"):chess.WHITE, _("Black"):chess.BLACK}
        bw = st.radio(_("Choose White or Black"), sel.keys(), horizontal=True)
        depth = st.slider(_("Depth"), 1, 4, 3)

        if sel[bw] in [chess.WHITE, chess.BLACK]:    
            
            if "setboard" not in st.session_state:
                bd = set_board(board, bw)    
                st.session_state.setboard = bd
                st.session_state.white = sel[bw]
                st.session_state.history = []
                st.session_state.depth = depth
        #        print(bd)
        
                if sel[bw] == chess.BLACK:
                    
                    ai_move_uci = showStatus(get_ai_move, board, _("AI thinking ..."))
#                    print("AI MOVE UCI", ai_move_uci)
                    showStatus(None, None, _("AI: " + str(ai_move_uci)))
                    if ai_move_uci in board.legal_moves:
                        ai_move = ai_move_uci
#                        ai_move = chess.Move.from_uci(ai_move_uci)
#                        ai_move = board.parse_san(ai_move_uci)
                        
                        pr = chess.QUEEN
                        prom = isMovePromotion(board, ai_move)
                        if prom:
                            pr = choosePromotion()
                            ai_move = chess.Move(ai_move.from_square, ai_move.to_square, promotion=pr)
                            bd = st.session_state.setboard
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
    
       
def main():    
    
    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
    
        try:                
            streamlit_image_coordinates(
                PLAYFILENAME,
                key="pil",
                click_and_drag=True,
                on_click=add_point
                )

            with open(PLAYFILENAME, "rb") as file:
                st.download_button(
                    label=_("Download"),
                    data=file,
                    file_name=PLAYFILENAME,
                    mime="image/png"
                )                                   
        except Exception as e:
            st.error(f"Failed:\n {e}")
#            print(f"Failed to coor:\n {e}")
            
        with col2:
            showHistory()

        
if __name__ == '__main__':
    selectBlackWhite(st.session_state.board)
