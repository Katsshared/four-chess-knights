
import pyvips

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import chess
import chess.svg

import gettext

PLAYAIFILENAME = "playai.png"




# this module implement's Tomasz Michniewski's Simplified Evaluation Function
# https://www.chessprogramming.org/Simplified_Evaluation_Function
# note that the board layouts have been flipped and the top left square is A1

# fmt: off
piece_value = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

pawnEvalWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
pawnEvalBlack = list(reversed(pawnEvalWhite))

knightEval = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishopEvalWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopEvalBlack = list(reversed(bishopEvalWhite))

rookEvalWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookEvalBlack = list(reversed(rookEvalWhite))

queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
kingEvalBlack = list(reversed(kingEvalWhite))

kingEvalEndGameWhite = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
kingEvalEndGameBlack = list(reversed(kingEvalEndGameWhite))
# fmt: on


def move_value(board: chess.Board, move: chess.Move, endgame: bool) -> float:
    """
    How good is a move?
    A promotion is great.
    A weaker piece taking a stronger piece is good.
    A stronger piece taking a weaker piece is bad.
    Also consider the position change via piece-square table.
    """
    if move.promotion is not None:
        return -float("inf") if board.turn == chess.BLACK else float("inf")

    _piece = board.piece_at(move.from_square)
    if _piece:
        _from_value = evaluate_piece(_piece, move.from_square, endgame)
        _to_value = evaluate_piece(_piece, move.to_square, endgame)
        position_change = _to_value - _from_value
    else:
        raise Exception(f"A piece was expected at {move.from_square}")

    capture_value = 0.0
    if board.is_capture(move):
        capture_value = evaluate_capture(board, move)

    current_move_value = capture_value + position_change
    if board.turn == chess.BLACK:
        current_move_value = -current_move_value

    return current_move_value


def evaluate_capture(board: chess.Board, move: chess.Move) -> float:
    """
    Given a capturing move, weight the trade being made.
    """
    if board.is_en_passant(move):
        return piece_value[chess.PAWN]
    _to = board.piece_at(move.to_square)
    _from = board.piece_at(move.from_square)
    if _to is None or _from is None:
        raise Exception(
            f"Pieces were expected at _both_ {move.to_square} and {move.from_square}"
        )
    return piece_value[_to.piece_type] - piece_value[_from.piece_type]


def evaluate_piece(piece: chess.Piece, square: chess.Square, end_game: bool) -> int:
    piece_type = piece.piece_type
    mapping = []
    if piece_type == chess.PAWN:
        mapping = pawnEvalWhite if piece.color == chess.WHITE else pawnEvalBlack
    if piece_type == chess.KNIGHT:
        mapping = knightEval
    if piece_type == chess.BISHOP:
        mapping = bishopEvalWhite if piece.color == chess.WHITE else bishopEvalBlack
    if piece_type == chess.ROOK:
        mapping = rookEvalWhite if piece.color == chess.WHITE else rookEvalBlack
    if piece_type == chess.QUEEN:
        mapping = queenEval
    if piece_type == chess.KING:
        # use end game piece-square tables if neither side has a queen
        if end_game:
            mapping = (
                kingEvalEndGameWhite
                if piece.color == chess.WHITE
                else kingEvalEndGameBlack
            )
        else:
            mapping = kingEvalWhite if piece.color == chess.WHITE else kingEvalBlack

    return mapping[square]


def evaluate_board(board: chess.Board) -> float:
    """
    Evaluates the full board and determines which player is in a most favorable position.
    The sign indicates the side:
        (+) for white
        (-) for black
    The magnitude, how big of an advantage that player has
    """
    total = 0
    end_game = check_end_game(board)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        value = piece_value[piece.piece_type] + evaluate_piece(piece, square, end_game)
        total += value if piece.color == chess.WHITE else -value

    return total


def check_end_game(board: chess.Board) -> bool:
    """
    Are we in the end game?
    Per Michniewski:
    - Both sides have no queens or
    - Every side which has a queen has additionally no other pieces or one minorpiece maximum.
    """
    queens = 0
    minors = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.QUEEN:
            queens += 1
        if piece and (
            piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT
        ):
            minors += 1

    if queens == 0 or (queens == 2 and minors <= 1):
        return True

    return False

from typing import Dict, List, Any

debug_info: Dict[str, Any] = {}


MATE_SCORE     = 1000000000
MATE_THRESHOLD =  999000000


def next_move(depth: int, board: chess.Board, debug=True) -> chess.Move:
    """
    What is the next best move?
    """
    debug_info.clear()
    debug_info["nodes"] = 0
#    t0 = time.time()

    move = minimax_root(depth, board)

#    debug_info["time"] = time.time() - t0
    if debug == True:
        print(f"info {debug_info}")
    return move


def get_ordered_moves(board: chess.Board) -> List[chess.Move]:
    """
    Get legal moves.
    Attempt to sort moves by best to worst.
    Use piece values (and positional gains/losses) to weight captures.
    """
    end_game = check_end_game(board)

    def orderer(move):
        return move_value(board, move, end_game)

    in_order = sorted(
        board.legal_moves, key=orderer, reverse=(board.turn == chess.WHITE)
    )
    return list(in_order)


def minimax_root(depth: int, board: chess.Board) -> chess.Move:
    """
    What is the highest value move per our evaluation function?
    """
    # White always wants to maximize (and black to minimize)
    # the board score according to evaluate_board()
    board = st.session_state.boardai
#    maximize = st.session_state.colorai == chess.WHITE
    maximize = board.turn == chess.WHITE
    best_move = -float("inf")
    if not maximize:
        best_move = float("inf")

    moves = get_ordered_moves(board)
    best_move_found = None
    if moves:
        best_move_found = moves[0]        

    for move in moves:
        board.push(move)
        # Checking if draw can be claimed at this level, because the threefold repetition check
        # can be expensive. This should help the bot avoid a draw if it's not favorable
        # https://python-chess.readthedocs.io/en/latest/core.html#chess.Board.can_claim_draw
        if board.can_claim_draw():
            value = 0.0
        else:
            value = minimax(depth - 1, board, -float("inf"), float("inf"), not maximize)
        board.pop()
        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move

    return best_move_found


def minimax(
    depth: int,
    board: chess.Board,
    alpha: float,
    beta: float,
    is_maximising_player: bool,
) -> float:
    """
    Core minimax logic.
    https://en.wikipedia.org/wiki/Minimax
    """
    debug_info["nodes"] += 1

    if board.is_checkmate():
        # The previous move resulted in checkmate
        return -MATE_SCORE if is_maximising_player else MATE_SCORE
    # When the game is over and it's not a checkmate it's a draw
    # In this case, don't evaluate. Just return a neutral result: zero
    elif board.is_game_over():
        return 0

    if depth == 0:
        return evaluate_board(board)

    if is_maximising_player:
        best_move = -float("inf")
        moves = get_ordered_moves(board)
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)
            # Each ply after a checkmate is slower, so they get ranked slightly less
            # We want the fastest mate!
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = max(
                best_move,
                curr_move,
            )
            board.pop()
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        best_move = float("inf")
        moves = get_ordered_moves(board)
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = min(
                best_move,
                curr_move,
            )
            board.pop()
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    

if "sellang" not in st.session_state:
    st.session_state.sellang ="en"

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 


def get_titleai():
    wb = ""
    depth =""
    if "depth" in st.session_state:
        depth = " " + _("Depth") + " " + str(st.session_state.depth)
    if "colorai" in st.session_state:
        wb = _("White") if st.session_state.colorai == chess.WHITE else _("Black")
    
    title = _("Play") + " " + _("chess") + " " + wb + depth

    return title

st.title(get_titleai())

def get_boardai():
    board_ai = chess.Board()
    return board_ai

board_ai = chess.Board()
if "boardai" not in st.session_state:
    st.session_state.boardai = get_boardai()

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
    for i, move in enumerate(st.session_state.historyai):
        text = ""
        if i % 2 == 0:
            text = f"{j}. {move}"
        else:
            text = f" {move}"
            j = j + 1            
        ls.append(text)
    st.markdown(ls)
#    print(st.session_state.historyai)

def addHistory(move, ai=True):
    if ai:
        st.session_state.historyai.append(f"AI: {move.uci()} ")
    else:
        st.session_state.historyai.append(f"Human: {move.uci()} ")
               
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
#    board = st.session_state.boardai
    bm = next_move(st.session_state.depth, board, False)

#    print("GET AI MOVE", bm)
    
    return bm

def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        st.iframe(svg_string)


def saveBoard(board):
    img = pyvips.Image.new_from_buffer(chess.svg.board(board).encode(), "")
    img.pngsave(PLAYAIFILENAME)


def updateBoard(board, save = True):
    bd = st.session_state.setboardai
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
    bd = st.session_state.setboardai

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
    bd = st.session_state.setboardai
    
    if fr == to:
        return None
    (pfr, cfr) = bd[fr]
    (pto, cto) = bd[to]
    if cfr != st.session_state.colorai:
        return None
     
    move = chess.Move(fr, to)  
    cast = isMoveCastling(board, move)
    if cast:
        if st.session_state.colorai == chess.WHITE:
            if to == 6:
                bd[to - 1] = bd[to + 1]
                bd[to + 1] = (None, None)
            elif to == 2:
                bd[to + 1] = bd[to - 2]
                bd[to - 2] = (None, None)
        elif st.session_state.colorai == chess.BLACK:
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
    board = st.session_state.boardai    
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
            bd = st.session_state.setboardai
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
    if "colorai" not in st.session_state:
        sel = {"NONE":None, _("White"):chess.WHITE, _("Black"):chess.BLACK}
        bw = st.radio(_("Choose White or Black"), sel.keys(), key = "ai", horizontal=True)
        depth = st.slider(_("Depth"), 1, 4, 3)

        if sel[bw] in [chess.WHITE, chess.BLACK]:    
            
            if "setboardai" not in st.session_state:
                bd = set_board(board, bw)    
                st.session_state.setboardai = bd
                st.session_state.colorai = sel[bw]
                st.session_state.historyai = []
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
                            bd = st.session_state.setboardai
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
                PLAYAIFILENAME,
                key="pil",
                click_and_drag=True,
                on_click=add_point
                )
            
            fname = "GameVsAI.txt"
            file = open(fname, 'w')
            file.writelines(st.session_state.historyai)
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
    selectBlackWhite(st.session_state.boardai)
