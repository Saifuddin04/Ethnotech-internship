let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let gameActive = true;

const statusText = document.getElementById("status");
const cells = document.querySelectorAll(".cell");

const winPatterns = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
];

// ✅ attach click listeners (NO inline JS)
cells.forEach(cell => {
    cell.addEventListener("click", () => {
        const index = cell.getAttribute("data-index");
        makeMove(index);
    });
});

function makeMove(index) {

    if (board[index] !== "" || !gameActive) return;

    board[index] = currentPlayer;

    cells[index].innerText = currentPlayer;

    if (checkWinner()) {
        statusText.innerText = `🎉 Player ${currentPlayer} Wins!`;
        gameActive = false;
        return;
    }

    if (!board.includes("")) {
        statusText.innerText = "🤝 It's a Draw!";
        gameActive = false;
        return;
    }

    currentPlayer = currentPlayer === "X" ? "O" : "X";
    statusText.innerText = `Player ${currentPlayer}'s Turn`;
}

function checkWinner() {
    return winPatterns.some(pattern => {
        return pattern.every(i => board[i] === currentPlayer);
    });
}

function resetGame() {
    board = ["", "", "", "", "", "", "", "", ""];
    currentPlayer = "X";
    gameActive = true;

    cells.forEach(cell => cell.innerText = "");

    statusText.innerText = "Player X's Turn";
}