console.log("GUESS JS LOADED");

// 🔥 MAIN FUNCTION
async function checkGuess() {

    const guessInput = document.getElementById("guess");
    const guess = guessInput.value;

    if (!guess) return;

    const res = await fetch("/check_guess", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ guess: guess })
    });

    const data = await res.json();

    const resultBox = document.getElementById("resultBox");

    // RESET styles
    resultBox.className = "result-box";

    // FORCE animation restart
    void resultBox.offsetWidth;

    if (data.result === "low") {
        resultBox.innerText = "📉 Too Low!";
        resultBox.classList.add("low", "shake", "animate");
    } 
    else if (data.result === "high") {
        resultBox.innerText = "📈 Too High!";
        resultBox.classList.add("high", "shake", "animate");
    } 
    else if (data.result === "correct") {
        resultBox.innerText = `🎉 CORRECT! (${data.attempts} attempts)`;
        resultBox.classList.add("win", "animate");

        document.getElementById("afterWin").style.display = "block";
    }
}


// ✅ THESE MUST BE GLOBAL (OUTSIDE)
function playAgain() {
    window.location.href = "/reset_guess";
}

function exitGame() {
    window.location.href = "/dashboard";
}