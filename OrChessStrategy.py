
import streamlit as st
import gettext

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

en_tenpr = _('''
Wilhelm/William Steinitz (1836 - 1900) was an Austrian-American chess player and the first undisputed world champion.
In early years his style of play was rather sharp, aggressive and full of sacrifices. Later he came up with his own scientific theory enunciating principles of chess: both for attack and defence.

Here are 10 of his most important principles that can be used in your own games.

1. Remember, the point of any debut is to develop the pieces and position them accordingly. At the same time, you need to prevent your opponent from accomplishing the same. You can get upper hand in two ways: develop quicker or prevent your opponent from developing.

2. Not only is it important to develop quickly, you also need to take care of your King’s safety. If your opponent is behind at development, you should delay him even more by creating threats.
You need to launch an attack as quickly as possible on the side of the board where he is the most vulnerable. Your opponent will need to focus on the threats you create and will not be able to finish development.

3. Another thing you need to pay attention to is the center. Depending on the position you need to occupy the center with either the pawns or the pieces. Strong pawn center will provide space. The piece center will give an opportunity for an attack.

4. You need to be careful concerning any pawn pushes. Always keep in mind that the pawns don’t move backwards and any unnecessary pawn advances will weaken position of you own king.

5. When developing pieces you have to have an exact plan of actions. You need to know what role each piece will play and where it should be positioned to realize this plan.

The difference between a novice player and a master is that a master develops chess pieces with a specific purpose while a beginner develops them just for a sake of developing.

6. The side who possesses an advantage must attack, otherwise he risks losing that advantage. The best way to come up with a plan for an effective attack is to identify a weakness in opponent’s position and to exploit it.

7. The defending side must deflect the threats, follow the plan of his opponent, predict his moves and look for a possibility of an effective counter attack. Keep in mind that defensive play is a much more difficult job than attacking play.

8. If a position is more or less equal the players need to maneuver their pieces to achieve an advantage of some sort and then move on to an attack. With a correct (best) defense the position should remain equal and the game should be drawn.

9. The overall advantage may consist from one big advantage or a multiple smaller advantages. When players of the same level play chess their goal is to obtain multiple small advantages that may ultimately result in winning the game.

10. There are two types of advantages at chess: permanent and temporary.

The permanent advantages are:

– Material advantage
– Weak squares
– Passed pawn
– Weak pawns
– Open diagonal/file
– Bishop pair

The temporary advantages are:

– Development
– Position of pieces
– Center
– Space

When you possess a permanent advantage you need to take your time, do not rush and with a careful play you will ultimately win the game.

When you have a temporary advantage you need to attack as soon as possible, since there is a possibility for your opponent to recover if you don’t act quickly enough.
'''
)

de_tenpr = _('''

Wilhelm/William Steinitz (1836–1900) war ein österreichisch-amerikanischer Schachspieler und der erste unbestrittene Weltmeister. In seinen frühen Jahren war sein Spielstil eher scharf, aggressiv und opferfreudig. Später entwickelte er seine eigene wissenschaftliche Theorie, die Schachprinzipien für Angriff und Verteidigung formulierte.

Hier sind 10 seiner wichtigsten Prinzipien, die Sie in Ihren eigenen Partien anwenden können.

1. Denken Sie daran: Ziel jedes Debüt ist es, die Figuren zu entwickeln und entsprechend zu positionieren. Gleichzeitig müssen Sie verhindern, dass Ihr Gegner dasselbe tut. Sie können sich auf zwei Arten einen Vorteil verschaffen: Entwickeln Sie Ihre Figuren schneller oder verhindern Sie die Entwicklung Ihres Gegners.

2. Neben einer schnellen Entwicklung ist auch die Sicherheit Ihres Königs wichtig. Wenn Ihr Gegner in seiner Entwicklung zurückliegt, sollten Sie ihn durch Drohungen weiter verzögern. Greifen Sie so schnell wie möglich die Seite des Bretts an, auf der er am verwundbarsten ist. Ihr Gegner muss sich auf die von Ihnen erzeugten Drohungen konzentrieren und kann seine Figurenentwicklung nicht abschließen.

3. Achten Sie außerdem auf das Zentrum. Je nach Stellung müssen Sie es entweder mit Bauern oder Figuren besetzen. Ein starkes Bauernzentrum schafft Raum, ein Figurenzentrum bietet Angriffsmöglichkeiten.

4. Seien Sie vorsichtig bei Bauernvorstößen. Denken Sie immer daran, dass Bauern nicht rückwärts ziehen und unnötige Vorstöße die Stellung Ihres Königs schwächen.

5. Bei der Figurenentwicklung benötigen Sie einen genauen Plan. Sie müssen wissen, welche Rolle jede Figur spielt und wo sie positioniert werden muss, um diesen Plan umzusetzen.

Der Unterschied zwischen einem Anfänger und einem Meister liegt darin, dass ein Meister seine Schachfiguren mit einem bestimmten Ziel entwickelt, während ein Anfänger sie nur um der Entwicklung willen entwickelt.

6. Wer im Vorteil ist, muss angreifen, sonst riskiert er, diesen Vorteil zu verlieren. Der beste Weg, einen effektiven Angriffsplan zu entwickeln, besteht darin, eine Schwäche in der gegnerischen Stellung zu erkennen und diese auszunutzen.

7. Die verteidigende Seite muss die Drohungen abwehren, den Plan des Gegners verfolgen, seine Züge vorhersehen und nach einer Möglichkeit für einen effektiven Gegenangriff suchen. Bedenken Sie, dass die Verteidigung deutlich schwieriger ist als der Angriff.

8. Ist die Stellung annähernd ausgeglichen, müssen die Spieler ihre Figuren so manövrieren, dass sie sich einen Vorteil verschaffen und dann zum Angriff übergehen. Mit einer optimalen Verteidigung sollte die Stellung ausgeglichen bleiben und die Partie remis enden.

9. Der Gesamtvorteil kann aus einem großen oder mehreren kleinen Vorteilen bestehen. Wenn Spieler gleichen Niveaus Schach spielen, ist ihr Ziel, mehrere kleine Vorteile zu erlangen, die letztendlich zum Sieg führen können.

10. Es gibt zwei Arten von Vorteilen im Schach: dauerhafte und temporäre.

Die permanenten Vorteile sind:

– Materialvorteil – Schwache Felder – Freibauer – Schwache Bauern – Offene Diagonale/Linie – Läuferpaar

Die temporären Vorteile sind:

– Entwicklung – Stellung der Figuren – Zentrum – Raum

Bei einem permanenten Vorteil sollten Sie sich Zeit lassen, nicht überhastet spielen und mit überlegtem Spiel letztendlich die Partie gewinnen.

Bei einem temporären Vorteil müssen Sie so schnell wie möglich angreifen, da Ihr Gegner die Möglichkeit hat, sich zu erholen, wenn Sie nicht schnell genug handeln.
'''
)


ru_tenpr = _('''
Вильгельм/Уильям Стейниц (1836 - 1900) был австрийско-американским шахматистом и первым бесспорным чемпионом мира по шахматам. В первые годы его стиль игры был довольно острым, агрессивным и жертвенным. Позже он разработал свою научную теорию, излагающую принципы игры в шахматы - как для атаки, так и для защиты.

Вот 10 его самых важных принципов, которые можно использовать в собственной практике.

1. Смысл любого дебюта состоит в том, чтобы развить фигуры и расположить их соответствующим образом. Но одновременно вы должны противодействовать вашему оппоненту, чтобы он не достиг того же. Вы можете лидировать двумя способами: быстрее развиваться или эффективно препятствовать развитию противника.

2. Важно не только быстро развиваться, но и внимательно заботиться о безопасности своего короля. И если ваш противник отстает в развитии, то вам следует ещё больше задерживать его, создавая угрозы.

При этом желательно как можно быстрее начать атаку на той стороне доски, где он наиболее уязвим. Тогда противнику придётся сосредоточиться на угрозах, которые вы создаете, и он не сможет завершить развитие.

3. Ещё один момент, на который стоит обратить внимание - центр. В зависимости от позиции вам нужно занять центр пешками или фигурами. Сильный пешечный центр даст простор. Фигурный центр даст хорошие возможности для атаки.

4. Вы должны быть осторожны с любой пешкой, которую двигаете. Всегда помните, что пешки не ходят назад, и любое ненужное продвижение пешек ослабит позицию вашего короля.

5. При развитии фигур у вас должен быть точный план действий. Вам нужно знать, какую роль будет играть каждая фигура и куда её следует разместить, чтобы реализовать этот план.

Разница между начинающим игроком и мастером в том, что мастер развивает шахматные фигуры с определенной целью, а новичок развивает их просто для развития.

6. Сторона, обладающая преимуществом, должна атаковать, иначе она рискует потерять это преимущество. Лучший способ разработать план эффективной атаки - выявить слабое место в позиции противника и использовать его.

7. Обороняющаяся сторона должна отражать угрозы, следить за планом соперника, прогнозировать его ходы и искать возможность эффективной контратаки. Имейте в виду, что оборонительная игра - более сложная, чем атакующая.

8. Если позиция более или менее равная, игрокам нужно маневрировать фигурами, чтобы добиться какого-то преимущества, а затем переходить к атаке. При правильной (лучшей) защите позиция останется равной, и игра должна завершиться вничью.

9. В целом преимущество может состоять из одного большого преимущества или нескольких меньших. И когда игроки одного уровня играют в шахматы, их цель - получить несколько небольших преимуществ, которые в конечном итоге могут привести к победе в игре.

10. В шахматах есть два типа преимуществ: постоянные и временные.

Постоянные:

– Материальное преимущество
– Слабые поля
– Проходная пешка
– Слабые пешки
– Открытая диагональ / вертикаль
– Два слона

Временные преимущества:

– Развитие
– Расположение фигур
– Центр
– Пространство

Когда у вас постоянное преимущество, то вам нужно не торопиться и при осторожной игре вы, в конечном итоге, выиграете.

А вот когда у вас временное преимущество, вам нужно атаковать как можно скорее, ведь ваш противник может оправиться, если вы не будете действовать достаточно быстро.
'''
)

ua_tenpr = _('''
Вільгельм/Вільям Штайніц (1836 - 1900) був австрійсько-американським шахістом і першим абсолютним чемпіоном світу. У ранні роки його стиль гри був досить різким, агресивним і сповненим жертв. Пізніше він розробив власну наукову теорію, що формулює принципи шахів: як для атаки, так і для захисту.

Ось 10 його найважливіших принципів, які можна використовувати у ваших власних іграх.

1. Пам'ятайте, що сенс будь-якого дебюту полягає в розвитку фігур та їх відповідному розташуванні. Водночас вам потрібно перешкодити своєму супернику досягти того ж. Ви можете отримати перевагу двома способами: розвиватися швидше або перешкодити розвитку суперника.

2. Важливо не тільки швидко розвиватися, але й дбати про безпеку свого короля. Якщо ваш суперник відстає в розвитку, вам слід ще більше затримати його, створюючи загрози. Вам потрібно якомога швидше розпочати атаку на тому боці дошки, де він найбільш вразливий. Вашому опоненту потрібно буде зосередитися на загрозах, які ви створюєте, і він не зможе завершити розвиток.

3. Ще одна річ, на яку вам потрібно звернути увагу, це центр. Залежно від позиції вам потрібно зайняти центр або пішаками, або фігурами. Сильний пішачний центр забезпечить простір. Центр фігури дасть можливість для атаки.

4. Вам потрібно бути обережними щодо будь-яких пішакових просувань. Завжди пам'ятайте, що пішаки не рухаються назад, і будь-які непотрібні пішакові просування послаблять позицію вашого короля.

5. Під час розвитку фігур у вас повинен бути точний план дій. Вам потрібно знати, яку роль відіграватиме кожна фігура і де вона повинна бути розташована, щоб реалізувати цей план.

Різниця між новачком і майстром полягає в тому, що майстер розвиває шахові фігури з певною метою, тоді як новачок розвиває їх лише заради розвитку.

6. Сторона, яка має перевагу, повинна атакувати, інакше вона ризикує втратити цю перевагу. Найкращий спосіб розробити план ефективної атаки - це виявити слабкість у позиції суперника та використати її.

7. Сторона, що захищається, повинна відбивати загрози, слідувати плану свого суперника, передбачати його ходи та шукати можливості для ефективної контратаки. Майте на увазі, що захисна гра набагато складніша, ніж атакуюча.

8. Якщо позиція більш-менш рівна, гравцям потрібно маневрувати своїми фігурами, щоб досягти певної переваги, а потім переходити до атаки. При правильному (найкращому) захисті позиція повинна залишатися рівною, а гра має завершитися внічию.

9. Загальна перевага може складатися з однієї великої переваги або кількох менших переваг. Коли гравці одного рівня грають у шахи, їхня мета — отримати кілька невеликих переваг, які зрештою можуть призвести до виграшу гри.

10. У шахах є два типи переваг: постійні та тимчасові.

Постійні переваги:

– Матеріальна перевага – Слабкі поля – Пасовий пішак – Слабкі пішаки – Відкрита діагональ/лінія – Пара слонів

Тимчасові переваги:

– Розвиток – Положення фігур – Центр – Простір

Коли у вас є постійна перевага, вам потрібно не поспішати, не поспішати, і за допомогою обережної гри ви зрештою виграєте гру.

Коли у вас є тимчасова перевага, вам потрібно атакувати якомога швидше, оскільки існує ймовірність того, що ваш опонент оговтається, якщо ви не діятимете достатньо швидко.
'''
)

tenpr = {"en":en_tenpr, "de":de_tenpr, "ru":ru_tenpr, "ua":ua_tenpr, }

st.title(_("Strategy"))
st.header(_("10 principles of Wilhelm Steinitz"))

st.write(tenpr[st.session_state.sellang])


if __name__ == '__main__':
    pass