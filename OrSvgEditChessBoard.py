
import pyvips

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import chess
import chess.svg

import gettext

#import sys
#st.status("PLATFORM "+ sys.platform)

PUZZLEFILENAME = "puzzle.png"

if "sellang" not in st.session_state:
    st.session_state.sellang ="en"

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

st.title(_("Chess editor"))

board_edit = chess.Board()
if "board_edit" not in st.session_state:
    st.session_state.board_edit = board_edit

def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        st.iframe(svg_string)


def saveBoard(board):
    img = pyvips.Image.new_from_buffer(chess.svg.board(board).encode(), "")
    img.pngsave(PUZZLEFILENAME)


def updateBoard(board, save = True):
    bd = st.session_state["setboard_edit"]
    board.clear()
    for key in bd.keys():
        (pc, cl) = bd[key] 
        if (pc, cl) != (None, None):
            board.set_piece_at(key, chess.Piece(pc, cl))
        else:
            board.remove_piece_at(key)
    if save:        
        saveBoard(board)

              
def clearBoard(board):
    board.clear()
    bd = {x: (None, None) for x in range(64)} 
    return bd
      
def makeBoard(board):
    bd = clearBoard(board)   
    for i in range(0, 64):
        if i > 7 and i < 16:
            bd[i] = (chess.PAWN, chess.WHITE)
            board.set_piece_at(i, chess.Piece(chess.PAWN, chess.WHITE))
        if i == 0 or i == 7:
            bd[i] = (chess.ROOK, chess.WHITE)
            board.set_piece_at(i, chess.Piece(chess.ROOK, chess.WHITE))
        if i == 1 or i == 6:
            bd[i] = (chess.KNIGHT, chess.WHITE)
            board.set_piece_at(i, chess.Piece(chess.KNIGHT, chess.WHITE))
        if i == 2 or i == 5:
            bd[i] = (chess.BISHOP, chess.WHITE)
            board.set_piece_at(i, chess.Piece(chess.BISHOP, chess.WHITE))
        if i == 3:
            bd[i] = (chess.QUEEN, chess.WHITE)
            board.set_piece_at(i, chess.Piece(chess.QUEEN, chess.WHITE))
        if i == 4:
            bd[i] = (chess.KING, chess.WHITE)
            board.set_piece_at(i, chess.Piece(chess.KING, chess.WHITE))
        if i > 47 and i < 56:
            bd[i] = (chess.PAWN, chess.BLACK)
            board.set_piece_at(i, chess.Piece(chess.PAWN, chess.BLACK))
        if i == 56 or i == 63:
            bd[i] = (chess.ROOK, chess.BLACK)
            board.set_piece_at(i, chess.Piece(chess.ROOK, chess.BLACK))
        if i == 57 or i == 62:
            bd[i] = (chess.KNIGHT, chess.BLACK)
            board.set_piece_at(i, chess.Piece(chess.KNIGHT, chess.BLACK))
        if i == 58 or i == 61:
            bd[i] = (chess.BISHOP, chess.BLACK)
            board.set_piece_at(i, chess.Piece(chess.BISHOP, chess.BLACK))
        if i == 59:
            bd[i] = (chess.QUEEN, chess.BLACK)
            board.set_piece_at(i, chess.Piece(chess.QUEEN, chess.BLACK))
        if i == 60:
            bd[i] = (chess.KING, chess.BLACK)
            board.set_piece_at(i, chess.Piece(chess.KING, chess.BLACK))
    return bd

def coors2square(x, y):
    sq_size = 45
    br_size = 30
    col = round((x-br_size)/sq_size)
    row = round((y-br_size)/sq_size)
    sq = chess.square(col, 7 - row) 
    print("row=", row, " col=", col, " sq=", sq, " ", chess.square_name(sq))
    return sq

def makeMove(board, x1, y1, x2, y2):
    fr = coors2square(x1, y1)
    to = coors2square(x2, y2)
    bd = st.session_state["setboard_edit"]
#    (pfr, cfr) = bd[fr]
#    (pto, cto) = bd[to]
#    board.set_piece_at(to, chess.Piece(pto, cto))
#    board.remove_piece_at(fr)
    bd[to] = bd[fr]
    bd[fr] = (None, None)
#    (pfr, cfr) = bd[fr]
#    board.set_piece_at(to, chess.Piece(pfr, cfr))
#   board.remove_piece_at(fr)
    if fr == to:
        bd[to] = (None, None)
#        board.remove_piece_at(to)
 
    updateBoard(board)
    
def add_point():
    board = st.session_state.board_edit
    rv = st.session_state["pil"]
    print("pil ", rv)
    off = 15
    for key in ["x1", "x2" , "y1", "y2"]:
        if rv[key] < off or rv[key] > rv["width"] - off or rv[key] > rv["height"] - off:
            return
    makeMove(board, rv["x1"], rv["y1"], rv["x2"], rv["y2"])
    
def set_board(board):    

#    board.clear()
    bd = makeBoard(board)
#    render_svg(chess.svg.board(board))
    
    # Convert an SVG file to PNG using the default save options
    saveBoard(board)
    
    return bd            
    
def stfish(board):    

    if "setboard_edit" not in st.session_state:
        bd = set_board(board)
        st.session_state["setboard_edit"] = bd
        
    try:                
        streamlit_image_coordinates(
            PUZZLEFILENAME,
            key="pil",
            click_and_drag=True,
            on_click=add_point
            )

        with open(PUZZLEFILENAME, "rb") as file:
            st.download_button(
                label=_("Download"),
                data=file,
                file_name=PUZZLEFILENAME,
                mime="image/png"
            )                           
    except Exception as e:
        st.error(f"Failed\n {e}")
        print(f"Failed to coor:\n {e}")
        
if __name__ == '__main__':
    stfish(st.session_state.board_edit)
