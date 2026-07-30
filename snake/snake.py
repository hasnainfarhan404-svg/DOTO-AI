import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Streamlit Snake Game", page_icon="🐍", layout="centered")

st.title("🐍 Streamlit Snake Game")
st.write("Game board par click karein aur **Arrow Keys** se control karein. Restart karne ke liye **Spacebar** dabayein.")

# HTML5 Canvas based game (No Tkinter, No Streamlit Buttons)
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #0e1117;
            display: flex;
            flex-direction: column;
            align-items: center;
            color: white;
            font-family: Arial, sans-serif;
            margin: 0;
        }
        #score-board {
            font-size: 18px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        #status {
            font-size: 14px;
            margin-bottom: 10px;
            color: #888888;
        }
        canvas {
            border: 2px solid #333;
            background-color: #000000;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            outline: none;
        }
    </style>
</head>
<body>

<div id="score-board">Score: <span id="score">0</span> | High Score: <span id="high-score">0</span></div>
<div id="status">Press SPACE to Start / Restart</div>
<canvas id="gameCanvas" width="400" height="400" tabindex="1"></canvas>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreEl = document.getElementById("score");
    const highScoreEl = document.getElementById("high-score");
    const statusEl = document.getElementById("status");

    const cellSize = 20;
    const gridWidth = canvas.width / cellSize;
    const gridHeight = canvas.height / cellSize;

    let snake = [];
    let food = { x: 0, y: 0 };
    let direction = "RIGHT";
    let nextDirection = "RIGHT";
    let score = 0;
    let highScore = 0;
    let gameOver = false;
    let gameLoop = null;

    function drawGrid() {
        ctx.strokeStyle = "#1a1a1a";
        for (let i = 0; i <= canvas.width; i += cellSize) {
            ctx.beginPath();
            ctx.moveTo(i, 0);
            ctx.lineTo(i, canvas.height);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(0, i);
            ctx.lineTo(canvas.width, i);
            ctx.stroke();
        }
    }

    function placeFood() {
        while (true) {
            let x = Math.floor(Math.random() * gridWidth);
            let y = Math.floor(Math.random() * gridHeight);
            let onSnake = snake.some(s => s.x === x && s.y === y);
            if (!onSnake) {
                food = { x: x, y: y };
                break;
            }
        }
    }

    function draw() {
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        drawGrid();

        // Draw Food
        ctx.fillStyle = "red";
        ctx.beginPath();
        let fx = food.x * cellSize + cellSize / 2;
        let fy = food.y * cellSize + cellSize / 2;
        ctx.arc(fx, fy, 7, 0, 2 * Math.PI);
        ctx.fill();

        // Draw Snake
        snake.forEach((segment, index) => {
            ctx.fillStyle = index === 0 ? "#00FF00" : "#00CC00";
            ctx.fillRect(
                segment.x * cellSize + 1,
                segment.y * cellSize + 1,
                cellSize - 2,
                cellSize - 2
            );
        });

        if (gameOver) {
            ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "red";
            ctx.font = "bold 24px Arial";
            ctx.textAlign = "center";
            ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 10);

            ctx.fillStyle = "white";
            ctx.font = "14px Arial";
            ctx.fillText("Final Score: " + score, canvas.width / 2, canvas.height / 2 + 20);
        }
    }

    function startGame() {
        if (gameLoop) clearInterval(gameLoop);

        gameOver = false;
        score = 0;
        direction = "RIGHT";
        nextDirection = "RIGHT";
        scoreEl.innerText = score;
        statusEl.innerText = "Game Running!";

        let startX = Math.floor(gridWidth / 2);
        let startY = Math.floor(gridHeight / 2);
        snake = [
            { x: startX, y: startY },
            { x: startX - 1, y: startY },
            { x: startX - 2, y: startY }
        ];

        placeFood();
        draw();
        gameLoop = setInterval(update, 100);
    }

    function update() {
        if (gameOver) return;

        direction = nextDirection;
        let head = { ...snake[0] };

        if (direction === "UP") head.y -= 1;
        if (direction === "DOWN") head.y += 1;
        if (direction === "LEFT") head.x -= 1;
        if (direction === "RIGHT") head.x += 1;

        if (head.x < 0 || head.x >= gridWidth || head.y < 0 || head.y >= gridHeight) {
            endGame("Hit Wall!");
            return;
        }

        if (snake.some(s => s.x === head.x && s.y === head.y)) {
            endGame("Ate Self!");
            return;
        }

        snake.unshift(head);

        if (head.x === food.x && head.y === food.y) {
            score += 10;
            if (score > highScore) {
                highScore = score;
                highScoreEl.innerText = highScore;
            }
            scoreEl.innerText = score;
            placeFood();
        } else {
            snake.pop();
        }

        draw();
    }

    function endGame(reason) {
        gameOver = true;
        clearInterval(gameLoop);
        statusEl.innerText = "Game Over! (" + reason + ") Press SPACE to restart";
        draw();
    }

    // Direct Arrow Keys Control
    window.addEventListener("keydown", function(e) {
        if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].includes(e.key)) {
            e.preventDefault();
        }

        if (e.key === "ArrowUp" && direction !== "DOWN") nextDirection = "UP";
        if (e.key === "ArrowDown" && direction !== "UP") nextDirection = "DOWN";
        if (e.key === "ArrowLeft" && direction !== "RIGHT") nextDirection = "LEFT";
        if (e.key === "ArrowRight" && direction !== "LEFT") nextDirection = "RIGHT";

        if (e.key === " " && (gameOver || snake.length === 0)) {
            startGame();
        }
    });

    drawGrid();
</script>

</body>
</html>
"""

components.html(game_code, height=500)