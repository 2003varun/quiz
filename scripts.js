// ================== QUESTIONS ==================
const questionsData = {
  easy: [
    { q: "HTML stands for?", o: ["Hyper Text Markup Language","High Text Machine","Hyperlinks Text"], a: "Hyper Text Markup Language" },
    { q: "Which tag is used to write CSS?", o: ["<style>","<css>","<script>"], a: "<style>" },
    { q: "Which tag creates a hyperlink?", o: ["<a>","<link>","<href>"], a: "<a>" }
  ],
  medium: [
    { q: "Which is NOT a JavaScript framework?", o: ["React","Angular","Django"], a: "Django" },
    { q: "CSS property to change text color?", o: ["color","font-color","text-color"], a: "color" },
    { q: "HTML5 semantic tag for navigation?", o: ["<nav>","<section>","<div>"], a: "<nav>" }
  ],
  hard: [
    { q: "Which HTTP method is idempotent?", o: ["POST","GET","PATCH"], a: "GET" },
    { q: "Which property adds shadow to text in CSS?", o: ["text-shadow","box-shadow","shadow"], a: "text-shadow" },
    { q: "JS keyword to declare a constant?", o: ["var","let","const"], a: "const" }
  ]
};

let allQuestions = [];
let index = 0;
let score = 0;

// ================== PREPARE QUIZ ==================
window.onload = () => {
  // Combine all levels
  allQuestions = [...questionsData.easy, ...questionsData.medium, ...questionsData.hard];
  allQuestions = shuffle(allQuestions);
  showScreen("quiz-screen");
  loadQuestion();
};

// ================== LOAD QUESTION ==================
function loadQuestion() {
  updateProgress();
  const current = allQuestions[index];
  document.getElementById("question").innerText = current.q;

  const optionsDiv = document.getElementById("options");
  optionsDiv.innerHTML = "";

  shuffle(current.o).forEach(opt => {
    const btn = document.createElement("button");
    btn.innerText = opt;
    btn.onclick = () => checkAnswer(opt);
    optionsDiv.appendChild(btn);
  });
}

// ================== CHECK ANSWER ==================
function checkAnswer(selected) {
  if (selected === allQuestions[index].a) score++;

  index++;
  index < allQuestions.length ? loadQuestion() : showResult();
}

// ================== SHOW RESULT ==================
function showResult() {
  showScreen("result-screen");

  document.getElementById("score-text").innerText =
    `Your Score: ${score} / ${allQuestions.length}`;

  const feedback = document.getElementById("feedback");
  if (score === allQuestions.length) feedback.innerText = "🔥 Perfect Score!";
  else if (score >= allQuestions.length / 2) feedback.innerText = "😄 Good job!";
  else feedback.innerText = "🧠 Keep practicing!";
}

// ================== RESTART QUIZ ==================
function restartQuiz() {
  index = 0;
  score = 0;
  allQuestions = shuffle([...questionsData.easy, ...questionsData.medium, ...questionsData.hard]);
  showScreen("quiz-screen");
  loadQuestion();
  updateProgress();
}

// ================== PROGRESS BAR ==================
function updateProgress() {
  const percent = (index / allQuestions.length) * 100;
  document.getElementById("progress-bar").style.width = percent + "%";
}

// ================== UTILITIES ==================
function shuffle(arr) {
  return arr.sort(() => Math.random() - 0.5);
}

function showScreen(id) {
  document.querySelectorAll(".screen").forEach(s =>
    s.classList.remove("active")
  );
  document.getElementById(id).classList.add("active");
}
