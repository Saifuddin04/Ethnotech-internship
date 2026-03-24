let currentQ = null;

async function loadQuestion() {
    const res = await fetch("/quiz");
    const data = await res.json();

    if (data.completed) {
        window.location.href = "/quiz-completed";
        return;
    }

    currentQ = data;

    // Question
    document.getElementById("question").innerText = data.question;

    // ✅ FIXED PROGRESS TEXT
    document.getElementById("progress").innerText =
        `Questions Done: ${data.progress + 1} / ${data.total}`;

    // ✅ FIXED PROGRESS BAR (REAL %)
    let percent = ((data.progress + 1) / data.total) * 100;
    document.getElementById("progressBar").style.width = percent + "%";

    // Options
    let optionsHTML = "";

    ["A","B","C","D"].forEach((letter, index) => {
        optionsHTML += `
        <button class="btn btn-primary option-btn"
            onclick="submitAnswer('${letter}', this)">
            ${letter}. ${data.options[index]}
        </button>
        `;
    });

    document.getElementById("options").innerHTML = optionsHTML;
}

async function submitAnswer(option, btn) {

    const res = await fetch("/quiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            qid: currentQ.id,
            option: option
        })
    });

    const data = await res.json();

    let buttons = document.querySelectorAll(".option-btn");

    buttons.forEach(b => {
        if (b.innerText.startsWith(data.correct)) {
            b.classList.add("correct");
        }
    });

    if (option !== data.correct) {
        btn.classList.add("wrong");
    }

    document.getElementById("score").innerText = data.score;

    setTimeout(loadQuestion, 1200);
}

// ✅ Skip button event
document.getElementById("skipBtn").addEventListener("click", loadQuestion);

// initial load
loadQuestion();

console.log(data);