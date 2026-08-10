
import streamlit as st
import gettext

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

en_tenpr = _('''
Chess debutes are categorized by their first moves as open, semi-open, closed, semi-closed, and flank. This traditional system helps to quickly and easily understand the game plan at the beginning of a game.

1. Open Debutes

Any debute that begins with first moves e4 e5 is classified as an open debute. These moves allow the center to open up easily, as they are central pawns, providing space for the minor pieces to develop better.
Further pawn exchanges in the center allow the game to open up further and also provide the opportunity for faster exchanges of minor pieces. Open play allows pieces to move more quickly into enemy territory and utilize tactical combinations.
Since the center is open, it is important for the king to castle within the first ten moves to be safe.

2. Closed Debutes

Debutes that begin with first moves d4 d5 are called closed. They are called closed because the two central pawns are protected by queens, making it difficult to exchange or attack these pawns. Consequently, play revolves around these pawns, which to a certain extent limits further development. This difficulty in long-term development will delay castling for both sides. The protected pawns on the d-file also cannot be easily attacked, forcing the game to degenerate into a closed position.

3. Semi-Open Debutes

If Black responds to d4 with anything other than d5, the symmetry of the center is broken, and this is called a semi-closed opening. The term "semi-closed" is used because there is only one pawn in the center, leaving the center half-open and half-closed.
The unbalanced position in such positions forces both players to use strategic maneuvers to organize an attack on the opponent. The King's Indian Defense is an example of this.
'''
)

de_tenpr = _('''
Schachdepüts werden nach ihren ersten Zügen in offene, halboffene, geschlossene, halbgeschlossene und Flankendebüts unterteilt.

1. Offene Debüts

Debüts, die mit ersten Schritten e4 e5 beginnen beginnen, gelten als offene Debüts. Diese Züge ermöglichen es, das Zentrum leicht zu öffnen, da es sich um zentrale Bauern handelt, die den Leichtfiguren Raum zur besseren Entwicklung geben. Weitere Bauerntausche im Zentrum ermöglichen es, die Partie weiter zu öffnen und auch schnellere Tausche von Leichtfiguren zu ermöglichen. Offenes Spiel erlaubt es den Figuren, schneller in gegnerisches Gebiet vorzudringen und taktische Kombinationen zu nutzen. Da das Zentrum offen ist, ist es wichtig, dass der König innerhalb der ersten zehn Züge rochiert, um auf der sicheren Seite zu sein.

2. Geschlossene Debüts

Debüts, die mit ersten Schritten d4 d5 beginnen, werden als geschlossen bezeichnet. Sie werden als geschlossen bezeichnet, weil die beiden zentralen Bauern durch Damen gedeckt sind, was es schwierig macht, diese Bauern zu tauschen oder anzugreifen. Folglich dreht sich das Spiel um diese Bauern, was die weitere Entwicklung bis zu einem gewissen Grad einschränkt. Diese Schwierigkeit der langfristigen Entwicklung verzögert die Rochade auf beiden Seiten. Die gedeckten Bauern auf der d-Linie sind ebenfalls schwer anzugreifen, wodurch das Spiel in eine geschlossene Stellung abgleitet.

3. Halboffene Debüts

Antwortet Schwarz auf d4 mit etwas anderem als d5, wird die Symmetrie des Zentrums gebrochen, und man spricht von einer halboffenen Eröffnung. Der Begriff „halboffen“ rührt daher, dass sich nur ein Bauer im Zentrum befindet, wodurch dieses halb offen und halb geschlossen ist.
Die unausgewogene Stellung in solchen Stellungen zwingt beide Spieler zu strategischen Manövern, um einen Angriff auf den Gegner zu organisieren. Die Königsindische Verteidigung ist ein Beispiel dafür.
'''
)


ru_tenpr = _('''
Шахматные дебюты делятся по первым ходам на открытые, полуоткрытые, закрытые, полузакрытые и фланговые. Эта традиционная система помогает просто и быстро понять план игры в начале партии 

1. Открытые дебюты

Любой дебют, начинающийся с ходов e4 e5, относится к категории открытых дебютов. Эти ходы позволяют центру легко раскрыться, поскольку они являются центральными пешками, которые предоставляют пространство для лучшего развития лёгких фигур.
Дальнейшие размены пешек в центре позволяют игре ещё больше раскрыться, а также предоставляют возможность для более быстрого размена лёгкими фигурами. Открытая игра позволяет фигурам быстрее перемещаться на территорию противника и использовать тактические комбинации.
Поскольку центр открыт, важно, чтобы король сделал рокировку в течение первых десяти ходов, чтобы быть в безопасности.

2. Закрытые дебюты

Дебюты, начинающиеся с ходов d4 d5, называются закрытыми. Они называются закрытыми, поскольку две центральные пешки защищены ферзями, что затрудняет размен или атаку этих пешек. Следовательно, игра вращается вокруг этих пешек, что в определённой степени ограничивает дальнейшее развитие. Эта трудность в долгосрочном развитии задержит рокировку для обеих сторон. Защищённые пешки на линии «d» также не могут быть легко атакованы, что вынуждает игру перейти в закрытую позицию.

3. Полуоткрытые дебюты

Если чёрные отвечают на d4 чем-то иным, чем d5, симметрия центра нарушается, и это называется полузакрытым дебютом. Термин «полузакрытый» используется потому, что в центре находится только одна пешка, поэтому центр остаётся полуоткрытым и полузакрытым.
Несбалансированное положение в таких позициях вынуждает обоих игроков использовать стратегические приёмы для организации атаки на соперника. Староиндийская защита является тому примером.
'''
)

ua_tenpr = _('''
Шахові дебюти діляться першими ходами на відкриті, напіввідкриті, закриті, напівзакриті і флангові. Ця традиційна система допомагає легко і швидко зрозуміти план гри на початку партії.

1. Відкриті дебюти

Будь-який дебют, що починається з ходів e4 e5, відноситься до категорії відкритих дебютів. Ці ходи дозволяють центру легко розкритися, оскільки є центральними пішаками, які надають простір для кращого розвитку легких фігур.
Подальші розміни пішаків у центрі дозволяють грі ще більше розкритися, а також надають можливість швидкого розміну легкими фігурами. Відкрита гра дозволяє фігурам швидше переміщатися на територію супротивника та використовувати тактичні комбінації.
Оскільки центр відкритий, важливо, щоб король зробив рокіровку протягом перших десяти ходів, щоб бути в безпеці.

2. Закриті дебюти

Дебюти, що починаються з ходів d4 d5, називають закритими. Вони називаються закритими, оскільки два центральні пішаки захищені ферзями, що ускладнює розмін або атаку цих пішаків. Отже, гра обертається навколо цих пішаків, що певною мірою обмежує подальший розвиток. Ця складність у довгостроковому розвитку затримає рокіровку для обох сторін. Захищені пішаки на лінії d також не можуть бути легко атаковані, що змушує гру перейти в закриту позицію.

3. Напіввідкриті дебюти

Якщо чорні відповідають на d4 чимось іншим, ніж d5, симетрія центру порушується, і це називається напівзакритим дебютом. Термін «напівзакритий» використовується тому, що в центрі знаходиться лише один пішак, тому центр залишається напіввідкритим та напівзакритим.
Незбалансоване становище у таких позиціях змушує обох гравців використовувати стратегічні прийоми організації атаки на суперника.Староіндійський захист є тому прикладом.
'''
)

tenpr = {"en":en_tenpr, "de":de_tenpr, "ru":ru_tenpr, "ua":ua_tenpr, }

st.title(_("Debut"))
#st.header(_("Basic tactical techniques"))

st.write(tenpr[st.session_state.sellang])


if __name__ == '__main__':
    pass