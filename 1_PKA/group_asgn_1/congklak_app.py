import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from modules.state import CongklakState
from modules.strategies import get_max_diff, maximize_house_strategy, simple_strategy, random_strategy

st.set_page_config(
    page_title="congklak", page_icon="⚫", initial_sidebar_state="expanded"
)

st.write(
    """
# ⚫ Main Congklak
Simulasi permainan congklak.
"""
)

def auto(state, strategies):
    if (strategies == 'max_diff'):
        maximize_diff_score_strategy = get_max_diff(maximize_house_strategy)
        next_state = sorted(maximize_diff_score_strategy(state))[0][2]
        return next_state

    elif (strategies == 'max_house'):
        next_state = sorted(maximize_house_strategy(state))[0][2]
        return next_state
        
    elif (strategies == 'random'):
        next_state = sorted(random_strategy(state))[0][2]
        return next_state
        
    elif (strategies == 'simple'):
        next_state = sorted(simple_strategy(state))[0][2]
        return next_state

def circle_num(num, color):
    return st.markdown(f"""
        <style>
            .circle {{
                max-width: 30px;
                text-align: center;
                border: 1px solid {color};
                border-radius: 20px; 
                color: {color};  
            }}
        </style>
        <div class='circle'>{num}</div>
    """, unsafe_allow_html=True,)

if 'state' not in st.session_state:
    st.session_state['state'] = CongklakState(player=0, holes=7, init_beads=7)

if 'start_game' not in st.session_state:
    st.session_state['start_game'] = False

if 'strategy' not in st.session_state:
    st.session_state['strategy'] = 'max_diff'

for num in ['holes', 'beads']:
    if num not in st.session_state:
        st.session_state[num] = 7

with st.form('Input'):
    col1, col2, col3 = st.columns(3)
    with col1:
        strategy = st.selectbox(
            label="Strategi lawan",
            options=("max_diff", "max_house", "random", "simple")
        )

    with col2:
        num_holes = st.number_input(label="Jumlah lubang", value=7)

    with col3:
        num_beads = st.number_input(label="Jumlah biji disetiap lubang", value=7)
        start = st.form_submit_button("Update")
        
        if start:
            # st.session_state['start_game'] = True
            st.session_state['state'] = CongklakState(player=0, holes=num_holes, init_beads=num_beads)
            st.session_state['holes'] = num_holes
            st.session_state['beads'] = num_beads
            st.session_state['strategy'] = strategy
        # else:
            # st.session_state['start_game'] = False

# if st.session_state['start_game']:
state = st.session_state['state']
st.markdown("### Giliranmu" if not bool(state.player) else "### Giliran Lawan")

for i, col in enumerate(st.columns(st.session_state['holes'] + 1)):
    with col:
        # p = state.player
        circle_num(state.board[1][i], "red")
        st.write(" ")
        circle_num(state.board[0][i], "black")
        st.write(" ")
        if (not bool(state.player) and i != 0 and state.board[0][i] != 0):
            if (st.button(f"Go", key=i)):
                st.session_state['state'] = state.action(i)

        if (bool(state.player) and i==st.session_state['holes'] and not state.is_terminal()):
            if (st.button("Next")):
                st.session_state['state'] = auto(state, st.session_state['strategy'])

if (np.all(state.board[0,1:] == 0) and state.player == 0):
    home_0 = state.board[0][0]
    home_1 = state.board[1][0]
    
    if home_0 == home_1:
        st.info("seri, main lagi..")
    elif home_0 > home_1:
        st.success("yeay menang :)")
    else:
        st.error("hahahaha kalaah :D")