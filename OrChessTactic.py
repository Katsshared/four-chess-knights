
import streamlit as st
import gettext

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

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

st.write(tenpr[st.session_state.sellang])


if __name__ == '__main__':
    pass