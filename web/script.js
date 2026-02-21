const storyEl = document.getElementById("story");
const choicesEl = document.getElementById("choices");
const statsEl = document.getElementById("stats");
const nameInput = document.getElementById("playerName");
const startBtn = document.getElementById("startBtn");
const restartBtn = document.getElementById("restartBtn");

let state = null;

function newState() {
  return {
    name: (nameInput.value || "Explorer").trim(),
    health: 10,
    luck: 0,
    courage: 0,
    inventory: [],
    ended: false,
  };
}

function renderStats() {
  if (!state) {
    statsEl.textContent = "";
    return;
  }
  statsEl.textContent = `💚 Health: ${state.health} | 🍀 Luck: ${state.luck} | 🦁 Courage: ${state.courage} | 🎒 ${state.inventory.join(", ") || "nothing yet"}`;
}

function setScene(text, options = []) {
  storyEl.textContent = text;
  choicesEl.innerHTML = "";
  options.forEach((option) => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.textContent = option.label;
    btn.addEventListener("click", option.action);
    choicesEl.appendChild(btn);
  });
  renderStats();
}

function ending(message) {
  state.ended = true;
  setScene(`${message} Play again if you want a different ending!`, []);
}

function houseScene() {
  setScene("You enter the creaky old house. On a table is a shining amulet, and upstairs you hear a soft sound.", [
    {
      label: "✨ Take the magical amulet",
      action: () => {
        state.inventory.push("magical amulet");
        state.luck += 2;
        ending("The amulet glows and teleports you safely out of the forest. You win! 🌈");
      },
    },
    {
      label: "🪜 Go upstairs",
      action: () => {
        if (state.inventory.includes("lantern")) {
          state.courage += 1;
          ending("Your lantern reveals the broken step! You avoid danger and find a safe exit. You win! 🏆");
          return;
        }
        state.health -= 3;
        ending("A weak stair cracks and you tumble down. Oops! Game over this time. 😵");
      },
    },
  ]);
}

function clearTrailScene() {
  // Gentle random event for replay variety.
  const roll = Math.floor(Math.random() * 3);
  if (roll === 0) {
    state.health += 1;
    state.luck += 1;
    storyEl.textContent = "You found healing berries on the path! (+1 health, +1 luck)";
  } else if (roll === 1) {
    state.luck += 1;
    storyEl.textContent = "You found a lucky acorn charm! (+1 luck)";
  } else {
    storyEl.textContent = "A butterfly lands on your shoulder and points toward a house ahead.";
  }

  setScene("You follow the bright trail and reach a mysterious old house.", [
    { label: "🏠 Enter the house", action: houseScene },
    {
      label: "🚶 Keep walking to the village",
      action: () => ending("You safely reach a cozy village and celebrate with hot cocoa. You win! ☕"),
    },
  ]);
}

function darkPathScene() {
  setScene("You take the dark path. You hear a rustling sound nearby...", [
    {
      label: "🔎 Investigate the sound",
      action: () => {
        if (state.inventory.includes("scout clue")) {
          state.inventory.push("lantern");
          state.luck += 1;
          setScene("Because you scouted earlier, you avoid danger and find a lantern on the ground!", [
            { label: "➡️ Continue to the clear trail", action: clearTrailScene },
          ]);
          return;
        }
        state.health -= 4;
        ending("A grumpy bear was sleeping there! You run, but the adventure ends for now. 🐻");
      },
    },
    {
      label: "↩️ Quietly backtrack",
      action: () => {
        state.luck += 1;
        clearTrailScene();
      },
    },
  ]);
}

function treeScene() {
  state.courage += 1;
  state.inventory.push("scout clue");
  setScene("From the treetop, you spot safe routes and hidden movement below.", [
    { label: "🌑 Take the dark path with your scouting clue", action: darkPathScene },
    { label: "☀️ Follow the clear trail", action: clearTrailScene },
  ]);
}

function crossroadsScene() {
  setScene(`Welcome, ${state.name}! You stand at a forest crossroads. What do you do?`, [
    { label: "🌑 Take the dark overgrown path", action: darkPathScene },
    { label: "☀️ Follow the clear bright trail", action: clearTrailScene },
    { label: "🌳 Climb a tree to scout", action: treeScene },
  ]);
}

startBtn.addEventListener("click", () => {
  state = newState();
  restartBtn.classList.remove("hidden");
  crossroadsScene();
});

restartBtn.addEventListener("click", () => {
  state = newState();
  crossroadsScene();
});
