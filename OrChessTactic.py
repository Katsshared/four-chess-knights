
import pyvips
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import chess
import chess.svg
import gettext

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

TACTICFILENAME = "tactic_fork.png"

en_tenpr = _('''
Basic Tactical Techniques

Below are the key elements that make up most combinations on the board:

• Double Attack (Fork) - a situation in which one piece simultaneously attacks two or more enemy pieces. The most famous example is the knight fork, but absolutely any piece can perform a double attack.

• Pin - a restriction on the mobility of a piece that cannot escape an attack because a more valuable piece (usually a king or queen) is behind it.

• Through Attack (Spear) - an attack on a long-range piece (queen, rook, or bishop), which, after escaping from attack, leaves another piece standing behind it undefended.

• Open Check - a situation in which one piece makes a move, opening a line of action for another piece, which begins to attack the king. A variation of this technique is the double check, when both pieces (the one that moved and the one that opened) declare check. 

• Mill - a cyclical technique in which open checks and discovered attacks are used repeatedly, allowing for a series of blows and the capture of the opponent's pieces.

• Distraction - the forced removal of an opponent's piece from an important square (for example, from protecting a key piece or from protecting against checkmate).

• Enticement - the forced transfer of an opponent's piece to a square where it is vulnerable (often leading to a checkmate combination or the loss of material).

• Overload - exploiting the fact that an opponent's piece physically cannot defend two important points or pieces at once.

• Destruction of a defense - the removal of a piece or pawn that serves as a support for defending other pieces or a point in the opponent's position.

'''
)

de_tenpr = _('''
Grundlegende taktische Techniken

Nachfolgend sind die wichtigsten Elemente aufgeführt, aus denen die meisten Kombinationen auf dem Schachbrett bestehen:

• Doppelangriff (Gabel) – Eine Figur greift gleichzeitig zwei oder mehr gegnerische Figuren an. Das bekannteste Beispiel ist die Springergabel, aber grundsätzlich kann jede Figur einen Doppelangriff ausführen.

• Fesselung – Eine Figur ist in ihrer Bewegungsfreiheit eingeschränkt und kann einem Angriff nicht entkommen, weil sich dahinter eine wertvollere Figur (meist König oder Dame) befindet.

• Durchstoß (Speer) – Ein Angriff auf eine Fernkampffigur (Dame, Turm oder Läufer), der nach erfolgreicher Flucht eine andere Figur ungedeckt zurücklässt.

• Offenes Schach – Eine Figur macht einen Zug und eröffnet damit eine Handlungslinie für eine andere Figur, die den König angreift. Eine Variante dieser Technik ist das Doppelschach, bei dem beide Figuren (die ziehende und die öffnende) Schach anbieten. 

• Mühle – eine zyklische Technik, bei der offene Schachgebote und Abzugsangriffe wiederholt eingesetzt werden, um eine Reihe von Schlägen und das Schlagen gegnerischer Figuren zu ermöglichen.

• Ablenkung – das erzwungene Entfernen einer gegnerischen Figur von einem wichtigen Feld (z. B. vom Schutz einer Schlüsselfigur oder von der Verteidigung gegen Matt).

• Verlockung – das erzwungene Versetzen einer gegnerischen Figur auf ein Feld, auf dem sie verwundbar ist (was oft zu einer Mattkombination oder Materialverlust führt).

• Überlastung – Ausnutzen der Tatsache, dass eine gegnerische Figur physisch nicht zwei wichtige Punkte oder Figuren gleichzeitig verteidigen kann.

• Zerstörung einer Verteidigung – das Entfernen einer Figur oder eines Bauern, der als Unterstützung für die Verteidigung anderer Figuren oder eines Punktes in der gegnerischen Stellung dient.

'''
)


ru_tenpr = _('''
Основные тактические приёмы

Ниже приведены главные элементы, из которых складывается большинство комбинаций на доске:
    
• Двойной удар (вилка) — ситуация, при которой одна фигура одновременно нападает на две или более фигуры противника. Самым известным примером является коневая вилка, но двойной удар может сделать абсолютно любая фигура.

• Связка — ограничение подвижности фигуры, которая не может уйти из-под удара, так как за ней находится более ценная фигура (обычно король или ферзь).

• Сквозной удар (копьё) — нападение на дальнобойную фигуру (ферзя, ладью или слона), которая после отхода из-под атаки оставляет незащищенной другую фигуру, стоящую позади неё.

• Открытый (вскрытый) шах — ситуация, когда одна фигура делает ход, открывая линию действия другой фигуре, которая начинает атаковать короля. Разновидностью этого приема является двойной шах, когда шах объявляют обе фигуры (та, что сходила, и та, что открылась). 

• Мельница — цикличный приём, при котором открытые шахи и вскрытые нападения используются многократно, позволяя наносить серии ударов и собирать фигуры противника.

• Отвлечение — вынужденный увод фигуры противника с важного поля (например, от защиты ключевой фигуры или от защиты от мата).

• Завлечение — принудительный перевод фигуры противника на поле, где она оказывается уязвимой (часто ведет к матовой комбинации или потере материала).

• Перегрузка — использование того факта, что фигура противника физически не может защищать сразу две важные точки или фигуры.

• Уничтожение защиты — устранение фигуры или пешки, которая служит опорой для защиты других фигур или пункта позиции соперника.

'''
)

ua_tenpr = _('''
Основні тактичні прийоми

Нижче наведено основні елементи, з яких складається більшість комбінацій на дошці: 

• Подвійний удар (вилка) — ситуація, коли одна фігура одночасно нападає на дві чи більше фігури противника. Найвідомішим прикладом є конева вилка, але подвійний удар може зробити будь-яка фігура. 

• Зв'язка – обмеження рухливості фігури, яка не може піти з-під удару, оскільки за нею знаходиться більш цінна фігура (зазвичай король чи ферзь). 

• Наскрізний удар (спис) - напад на далекобійну фігуру (ферзя, човна або слона), яка після відходу з-під атаки залишає незахищеною іншу фігуру, що стоїть позаду неї. 

• Відкритий (розкритий) шах — ситуація, коли одна фігура робить хід, відкриваючи лінію дії іншій фігурі, яка починає атакувати короля. Різновидом цього прийому є подвійний шах, коли шах оголошують обидві фігури (та, що сходила, та відкрита). 

• Млин – циклічний прийом, при якому відкриті шахи та розкриті напади використовуються багаторазово, дозволяючи завдавати серії ударів та збирати фігури супротивника. 

• Відволікання — вимушене відведення фігури супротивника з важливого поля (наприклад, від захисту ключової фігури або від захисту від мату). 

• Залучення — примусове переведення фігури супротивника на поле, де вона виявляється вразливою (часто веде до матової комбінації або втрати матеріалу). 

• Перевантаження — Використання того, що фігура супротивника фізично не може захищати дві важливі точки або фігури. 

• Знищення захисту — усунення фігури або пішака, яка є опорою для захисту інших фігур або пункту позиції суперника.

'''
)

tenpr = {"en":en_tenpr, "de":de_tenpr, "ru":ru_tenpr, "ua":ua_tenpr, }

st.title(_("Tactic"))
#st.header(_("Basic tactical techniques"))

fork_dict = {
   "1_Knight":["r2qk1nr/1bpn1ppp/p2p4/2b1p1N1/2B1P3/3P4/PPP2PPP/R1BQK2R w KQkq - 0 1", ["g5f7"],],
   "2_Bishop":["4r1k1/p4ppp/4p1n1/8/r7/4P1P1/P4PBP/3R1RK1 w - - 0 1", ["g2c6"],],
   "3_Pawn":["6k1/5p1p/6b1/1n1n4/8/3P1N2/2PBP1P1/4K3 w - - 0 1", ["c2c4"],],
   "4_Knight":["4r1k1/3Q1ppp/8/2B5/p1n5/Pq1b1BP1/5P1P/3R2K1 b - - 0 1", ["b3d1", "f3d1", "e8e1", "g1g2", "d3f1", "g2f3", "c4e5"],],
}

def get_boardta():
    board_ta = chess.Board()
    return board_ta

if "boardta" not in st.session_state:
    st.session_state.boardta = get_boardta()

def clearHistory():
    st.session_state.historyta = []
    
def showHistory():
    ls = []
    j = 1
    for i, move in enumerate(st.session_state.historyta):
        text = ""
        if i % 2 == 0:
            text = f"{j}. {move}"
        else:
            text = f" {move}"
            j = j + 1            
        ls.append(text)
    st.markdown(ls)
#    print(st.session_state.historyta)

def delHistory(move):
    h = st.session_state.historyta
    del h[st.session_state.indexta]
    
def addHistory(move):
    st.session_state.historyta.append(f"{move.uci()}")
              
def clearBoard(board):
    board.clear()
      
def saveBoard(board):
    img = pyvips.Image.new_from_buffer(chess.svg.board(board).encode(), options="")
    img.pngsave(TACTICFILENAME)

def popMove(board):
    moves = st.session_state.movesta
    idx = st.session_state.indexta
#    print("POP", moves[idx])
    board.pop()
    delHistory(moves[idx])
    st.session_state.actionta = -1
    saveBoard(board)

def pushMove(board):
    moves = st.session_state.movesta
    idx = st.session_state.indexta
    move = moves[idx]
#    print("PUSH", move)
    board.push(move)
    addHistory(move)
    st.session_state.actionta = +1
    saveBoard(board)
    
def stepExample(board, step=1):
    idx = st.session_state.indexta
    moves = st.session_state.movesta
    size = len(moves)
    act = st.session_state.actionta
#    print("IDX ACT SIZE STEP", idx, act, size, step)
    
    if act == 0:
        if idx == 0 and step < 0:
            return            
        elif idx == size - 1 and idx != 0 and step > 0:
            return
            
    if step < 0:
        if act >= 0:
            popMove(board)            
        elif act < 0:
            if idx > 0:
                st.session_state.indexta = idx - 1          
                popMove(board)
        if st.session_state.indexta < 0:
            st.session_state.indexta = 0
    elif step > 0:
        if act <= 0:
            pushMove(board)            
        elif act > 0:    
            if idx < size - 1:       
                st.session_state.indexta = idx + 1
                pushMove(board)            
        if st.session_state.indexta > size - 1:
            st.session_state.indexta = size - 1    

def setFen():
    board = st.session_state.boardta
    fdict = st.session_state.dictta
    board.clear()
    dc = fdict[st.session_state.tacticta]
    board.set_fen(dc[0])
    
def endExample(board):
#    initExample(board)
    if st.session_state.actionta == +2:
        return
    
    setFen()
    clearHistory()
    moves = st.session_state.movesta
    size = len(moves)
    print(moves)
    for i in range(0, size):
        board.push(moves[i])
        addHistory(moves[i])
    
    st.session_state.actionta = 0
    st.session_state.indexta = size -1
    st.session_state.actionta = +2
    
    saveBoard(board)

def initExample(board):
    setFen()
    st.session_state.indexta = 0
    st.session_state.actionta = 0
    st.session_state.historyta = []
    
    saveBoard(board)
    
    clearHistory()
    
def movesBoard(fdict):
    dc = fdict[st.session_state.tacticta]

    mvs = []
    move = None
    for mv in dc[1]:
        try:
#            print(mv)
            move = chess.Move.from_uci(mv)
             
        except Exception as e:
            board = st.session_state.boardta
            move = board.push_san(mv)
            st.error(f"Failed:\n {e}")

        
        mvs.append(move)
    return mvs

def makeBoard(fdict):
    dc = fdict[st.session_state.tacticta]
    board = chess.Board(dc[0])
    
    saveBoard(board)

    return board
    
def selectExample(fdict, tactic_sel):
    if "tacticta" not in st.session_state or tactic_sel != st.session_state.tacticta:
#        print("SELECT GAME", game_sel)
        st.session_state.dictta = fdict
        st.session_state.tacticta = tactic_sel

        st.session_state.movesta = movesBoard(fdict)
        st.session_state.indexta = 0
        st.session_state.actionta = 0
        st.session_state.historyta = []
        
        initExample(st.session_state.boardta)
      
def add_point():
    return

def main(fdict):
    tactic_sel = st.selectbox(label=" ", options=fdict.keys(), key="tacticsel_1")    
    selectExample(fdict, tactic_sel)

    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
    
        try:
            
            with st.container(horizontal=True, horizontal_alignment="left"):
                streamlit_image_coordinates(
                    TACTICFILENAME,
                    key="pil",
                    click_and_drag=True,
                    on_click=add_point
                )
            
            with st.container(horizontal=True, horizontal_alignment="left"):
                bb = st.button("|<-")
                bl = st.button("<-")
                br = st.button("->")
                be = st.button("->|")
                if bb: initExample(st.session_state.boardta)
                if be: endExample(st.session_state.boardta)
                if bl: stepExample(st.session_state.boardta, -1)
                if br: stepExample(st.session_state.boardta)
            
        except Exception as e:
            st.error(f"Failed:\n {e}")
            
    with col2:
        showHistory()
    
    
if __name__ == '__main__':            
    tab1, tab2 = st.tabs([_("Theory"), _("Fork"),])
    with tab1:
        st.write(tenpr[st.session_state.sellang])
    with tab2:
        main(fork_dict)


