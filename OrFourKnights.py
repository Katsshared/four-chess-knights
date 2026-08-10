'''

# create .mo
msgfmt -o locales/en/LC_MESSAGES/messages.mo locales/en/LC_MESSAGES/messages.po
msgfmt -o locales/de/LC_MESSAGES/messages.mo locales/de/LC_MESSAGES/messages.po
msgfmt -o locales/ru/LC_MESSAGES/messages.mo locales/ru/LC_MESSAGES/messages.po
msgfmt -o locales/ua/LC_MESSAGES/messages.mo locales/ua/LC_MESSAGES/messages.po
# update .po ASCII - UTF-8
msgmerge -U locales/en/LC_MESSAGES/messages.po locales/messages.pot
msgmerge -U locales/de/LC_MESSAGES/messages.po locales/messages.pot
msgmerge -U locales/ru/LC_MESSAGES/messages.po locales/messages.pot
msgmerge -U locales/ua/LC_MESSAGES/messages.po locales/messages.pot
#create .po
msginit -l en_EN.UTF8 -o locales/en/LC_MESSAGES/messages.po -i locales/messages.pot --no-translator
msginit -l de_DE.UTF8 -o locales/de/LC_MESSAGES/messages.po -i locales/messages.pot --no-translator
msginit -l ru_RU.UTF8 -o locales/ru/LC_MESSAGES/messages.po -i locales/messages.pot --no-translator
msginit -l ua_UA.UTF8 -o locales/ua/LC_MESSAGES/messages.po -i locales/messages.pot --no-translator

#generate .pot
xgettext -d messages -o locales/messages.pot OrFourKnights.py OrHome.py OrChessPuzzles.py --from-code UTF-8

#setup gettext
https://gnuwin32.sourceforge.net/packages/gettext.htm
sudo apt install gettext

cd /home/cat/eclipse-workspace/Orientaion/STREAMLITCLOUD/
streamlit run /home/cat/eclipse-workspace/Orientaion/STREAMLITCLOUD/OrFourKnights.py

'''

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import gettext

langs = ['en ' + "🇬🇧", 'de ' + "🇩🇪", 'ru ' + "🇷🇺", 'ua ' + "🇺🇦",]

lang_sel = st.sidebar.selectbox(" ", langs)

st.session_state.sellang = lang_sel[0:2]
    
localizator = gettext.translation('messages', localedir='locales', languages=[lang_sel[0:2]])    
localizator.install() 
_ = localizator.gettext 


@st.dialog(" ", dismissible=True, on_dismiss="rerun")
def on_click():
    st.header("🇬🇧" + " Four Chess Knights Club") 
    st.header("🇩🇪" + " Vier-Schach-Ritter-Club")
    st.header("🇷🇺" + " Клуб четырех шахматных рыцарей")
    st.header("🇺🇦" + " Клуб чотирьох шахових лицарів")
with st.sidebar:
    streamlit_image_coordinates("images/FourKnights.png", key="global", on_click=on_click)    
                
pg = st.navigation([
    st.Page("OrHome.py", title=_("Four Chess Knights"), icon="🏠"),
    st.Page("OrChessStrategy.py", title=_("Strategy"), icon="♟️"),
    st.Page("OrChessTactic.py", title=_("Tactic"), icon="♟️"),
    st.Page("OrChessDebut.py", title=_("Debut"), icon="♟️"),
    st.Page("OrSvgChessEngine.py", title=_("Play") + " " + _("chess"), icon="♟️"),
#    st.Page("OrSvgChessStockfish.py", title=_("Play") + " " + _("chess"), icon="♟️"),
    st.Page("OrChessPuzzles.py", title=_("Chess puzzles"), icon="♟️"),
    st.Page("OrSvgEditChessBoard.py", title=_("Chess editor"), icon="♟️"),
    st.Page("OrEmailContact.py", title=_("Contact"), icon="📫"),
])

pg.run()
    
if __name__=='__main__':
    pass
    