/**
 * Act 1: Training phase (ages 7→10) — simple UI test.
 * Matches docs/ACT1_DESIGN.md: 4 skills, baseline 2, primary 4, supplementary 3,
 * 10 actions per year, choose focus after all ≥ baseline, readiness when Year 3 + thresholds.
 */

const SKILLS = ["Strength", "Agility", "Smarts", "Spirit"];
const BASELINE = 2;
const PRIMARY_THRESHOLD = 4;
const SUPPLEMENTARY_THRESHOLD = 3;
const ACTIONS_PER_YEAR = 10;

const QUESTIONS = {
  Strength: {
    text: "What's the safest way to carry a heavy orb?",
    options: ["In one hand", "Close to your body with both hands", "On your head", "Tossing it"],
    correctIndex: 1,
  },
  Agility: {
    text: "What's the best way to step so you don't startle a creature?",
    options: ["Stomp loudly", "Move slowly and quietly", "Run toward it", "Jump"],
    correctIndex: 1,
  },
  Smarts: {
    text: "What do Moss Bunnies eat?",
    options: ["Berries", "Insects", "Grass and leaves", "Seeds"],
    correctIndex: 2,
  },
  Spirit: {
    text: "What should you do if a creature looks scared?",
    options: ["Chase it", "Stay calm and still, speak softly", "Throw food at it", "Leave immediately"],
    correctIndex: 1,
  },
};

let state = null;

function getState() {
  return {
    name: "",
    skills: { Strength: 0, Agility: 0, Smarts: 0, Spirit: 0 },
    actions: 0,
    year: 1,
    primary: null,
    supplementary: [],
    focusChosen: false,
    screen: "start",
  };
}

function actionsThisYear() {
  return state.actions % ACTIONS_PER_YEAR;
}

function currentYearLabel() {
  const y = Math.min(3, Math.floor(state.actions / ACTIONS_PER_YEAR) + 1);
  return `Year ${y} of 3`;
}

function allAtBaseline() {
  return SKILLS.every((s) => state.skills[s] >= BASELINE);
}

function isReady() {
  if (!state.focusChosen || state.primary === null || state.supplementary.length !== 2) return false;
  const yearIndex = Math.floor(state.actions / ACTIONS_PER_YEAR);
  if (yearIndex < 2) return false;
  if (state.skills[state.primary] < PRIMARY_THRESHOLD) return false;
  if (state.supplementary.some((s) => state.skills[s] < SUPPLEMENTARY_THRESHOLD)) return false;
  return true;
}

function showScreen(id) {
  document.getElementById("screen-start").classList.add("hidden");
  document.getElementById("screen-training").classList.add("hidden");
  document.getElementById("screen-focus").classList.add("hidden");
  document.getElementById("screen-ready").classList.add("hidden");
  document.getElementById(id).classList.remove("hidden");
}

function renderStats() {
  const el = document.getElementById("act1Stats");
  if (!el) return;
  const parts = SKILLS.map((s) => {
    let c = "skill-card";
    if (state.primary === s) c += " primary";
    if (state.supplementary.includes(s)) c += " supplementary";
    return `<div class="${c}"><span class="skill-name">${s}</span><br><span class="skill-value">${state.skills[s]}</span></div>`;
  });
  el.innerHTML = `<div><span class="year-badge">${currentYearLabel()}</span> Actions: ${state.actions}</div><div class="skill-grid">${parts.join("")}</div>`;
}

function renderTrainingChoices() {
  const storyEl = document.getElementById("act1Story");
  const choicesEl = document.getElementById("act1Choices");
  const questionEl = document.getElementById("act1Question");
  questionEl.classList.add("hidden");

  storyEl.textContent = `What do you want to study, ${state.name}?`;

  choicesEl.innerHTML = "";
  SKILLS.forEach((skill) => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.textContent = `Study ${skill}`;
    btn.addEventListener("click", () => showQuestion(skill));
    choicesEl.appendChild(btn);
  });
}

function showQuestion(skill) {
  const q = QUESTIONS[skill];
  document.getElementById("act1QuestionText").textContent = q.text;
  const answersEl = document.getElementById("act1Answers");
  answersEl.innerHTML = "";
  q.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "answer-btn choice-btn";
    btn.textContent = opt;
    btn.addEventListener("click", () => submitAnswer(skill, i, btn, answersEl));
    answersEl.appendChild(btn);
  });
  document.getElementById("act1Feedback").classList.add("hidden");
  document.getElementById("act1Question").classList.remove("hidden");
}

function submitAnswer(skill, chosenIndex, chosenBtn, answersEl) {
  const q = QUESTIONS[skill];
  const correct = chosenIndex === q.correctIndex;
  const feedbackEl = document.getElementById("act1Feedback");
  feedbackEl.classList.remove("hidden", "ok", "fail");
  feedbackEl.classList.add(correct ? "ok" : "fail");
  feedbackEl.textContent = correct
    ? `Correct! +1 ${skill}.`
    : `Not quite. The right answer was: "${q.options[q.correctIndex]}". No change this time.`;

  Array.from(answersEl.querySelectorAll("button")).forEach((b) => {
    b.disabled = true;
    b.classList.remove("correct", "wrong");
  });
  chosenBtn.classList.add(correct ? "correct" : "wrong");
  const correctBtn = answersEl.children[q.correctIndex];
  if (!correct) correctBtn.classList.add("correct");

  if (correct) state.skills[skill] += 1;
  state.actions += 1;

  setTimeout(() => {
    renderStats();
    if (!state.focusChosen && allAtBaseline()) {
      state.focusChosen = true;
      showFocusScreen();
      return;
    }
    if (isReady()) {
      showReadyScreen();
      return;
    }
    renderTrainingChoices();
    document.getElementById("act1Question").classList.add("hidden");
  }, 1800);
}

function showFocusScreen() {
  state.screen = "focus";
  showScreen("screen-focus");
  document.getElementById("focusStory").textContent =
    "You're getting stronger in every way. Now choose one primary skill (your main focus) and two supplementary skills. You'll need to reach higher levels in those three by the time you're 10.";
  const choicesEl = document.getElementById("focusChoices");
  choicesEl.innerHTML = "";

  const row1 = document.createElement("p");
  row1.innerHTML = "<strong>Pick your primary skill (must reach 4):</strong>";
  choicesEl.appendChild(row1);
  SKILLS.forEach((skill) => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.textContent = skill;
    btn.addEventListener("click", () => choosePrimary(skill, choicesEl));
    choicesEl.appendChild(btn);
  });
}

function choosePrimary(skill, choicesEl) {
  state.primary = skill;
  const others = SKILLS.filter((s) => s !== skill);
  choicesEl.innerHTML = "";
  const row2 = document.createElement("p");
  row2.innerHTML = `<strong>Primary: ${skill}. Now pick two supplementary skills (each must reach 3):</strong>`;
  choicesEl.appendChild(row2);
  others.forEach((s) => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.textContent = s;
    btn.addEventListener("click", () => chooseSupplementary(s, choicesEl));
    choicesEl.appendChild(btn);
  });
}

function chooseSupplementary(skill, choicesEl) {
  if (state.supplementary.includes(skill)) return;
  state.supplementary.push(skill);
  if (state.supplementary.length === 2) {
    state.screen = "training";
    showScreen("screen-training");
    renderStats();
    renderTrainingChoices();
  } else {
    const others = SKILLS.filter((s) => s !== state.primary && !state.supplementary.includes(s));
    choicesEl.innerHTML = "";
    const row = document.createElement("p");
    row.innerHTML = `<strong>Supplementary: ${state.supplementary.join(", ")}. Pick one more:</strong>`;
    choicesEl.appendChild(row);
    others.forEach((s) => {
      const btn = document.createElement("button");
      btn.className = "choice-btn";
      btn.textContent = s;
      btn.addEventListener("click", () => chooseSupplementary(s, choicesEl));
      choicesEl.appendChild(btn);
    });
  }
}

function showReadyScreen() {
  state.screen = "ready";
  showScreen("screen-ready");
  document.getElementById("readyStory").innerHTML =
    `You've turned 10. You're ready.<br><br>` +
    `Your primary skill, <strong>${state.primary}</strong>, and your supplementary skills, <strong>${state.supplementary.join("</strong> and <strong>")}</strong>, are strong enough. ` +
    `You say goodbye and set out for Ridgecamp.<br><br>` +
    `🎉 <strong>Act 1 complete.</strong> To play Act 2 (catch creatures, win the Exhibition), run the CLI game: <code>python adventure_game.py</code>`;
}

function startAct1() {
  const nameInput = document.getElementById("act1Name");
  state = getState();
  state.name = (nameInput.value || "Keeper").trim();
  document.getElementById("screen-start").classList.add("hidden");
  showScreen("screen-training");
  renderStats();
  renderTrainingChoices();
}

function init() {
  const btn = document.getElementById("act1StartBtn");
  if (btn) btn.addEventListener("click", startAct1);
}
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
