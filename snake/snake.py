import random
import time
import streamlit as st

# Page setup
st.set_page_config(page_title="Streamlit Snake Game", page_icon="🐍")

st.title("🐍 Streamlit Snake Game")

# Game Configuration
GRID_SIZE = 15

# Initialize Session States
if "snake" not in st.session_state:
    st.session_state.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (
        random.randint(0, GRID_SIZE - 1),
        random.randint(0, GRID_SIZE - 1),
    )
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.is_running = False


def reset_game():
    st.session_state.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (
        random.randint(0, GRID_SIZE - 1),
        random.randint(0, GRID_SIZE - 1),
    )
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.is_running = True


def move_snake():
    if st.session_state.game_over or not st.session_state.is_running:
        return

    head_x, head_y = st.session_state.snake[0]
    dir_x, dir_y = 0, 0

    if st.session_state.direction == "UP":
        dir_y = -1
    elif st.session_state.direction == "DOWN":
        dir_y = 1
    elif st.session_state.direction == "LEFT":
        dir_x = -1
    elif st.session_state.direction == "RIGHT":
        dir_x = 1

    new_head = (head_x + dir_x, head_y + dir_y)

    # Wall Collision Check
    if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
        st.session_state.game_over = True
        st.session_state.is_running = False
        return

    # Self Collision Check
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        st.session_state.is_running = False
        return

    st.session_state.snake.insert(0, new_head)

    # Food Collision Check
    if new_head == st.session_state.food:
        st.session_state.score += 10
        while True:
            new_food = (
                random.randint(0, GRID_SIZE - 1),
                random.randint(0, GRID_SIZE - 1),
            )
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    else:
        st.session_state.snake.pop()


# Game Controls UI
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader(f"Score: {st.session_state.score}")

    if st.button("▶️ Start / Reset Game", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown("### Controls")
    c1, c2, c3 = st.columns(3)

    with c2:
        if st.button("⬆️", key="up") and st.session_state.direction != "DOWN":
            st.session_state.direction = "UP"

    with c1:
        if st.button("⬅️", key="left") and st.session_state.direction != "RIGHT":
            st.session_state.direction = "LEFT"

    with c3:
        if st.button("➡️", key="right") and st.session_state.direction != "LEFT":
            st.session_state.direction = "RIGHT"

    _, c2_dn, _ = st.columns(3)
    with c2_dn:
        if st.button("⬇️", key="down") and st.session_state.direction != "UP":
            st.session_state.direction = "DOWN"

    if st.session_state.game_over:
        st.error("💥 Game Over!")

with col1:
    # Render Game Grid
    board_html = "<div style='display: grid; grid-template-columns: repeat(15, 20px); gap: 1px; background-color: #333; width: fit-content; padding: 5px; border-radius: 5px;'>"

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (c, r) == st.session_state.snake[0]:
                color = "#00FF00"  # Snake Head
            elif (c, r) in st.session_state.snake:
                color = "#00CC00"  # Snake Body
            elif (c, r) == st.session_state.food:
                color = "#FF0000"  # Food
            else:
                color = "#111111"  # Background Grid

            board_html += f"<div style='width: 20px; height: 20px; background-color: {color}; border-radius: 2px;'></div>"

    board_html += "</div>"
    st.markdown(board_html, unsafe_allow_html=True)

# Auto Loop for continuous movement
if st.session_state.is_running and not st.session_state.game_over:
    time.sleep(0.3)
    move_snake()
    st.rerun()