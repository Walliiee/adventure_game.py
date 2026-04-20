const storyEl = document.getElementById("story");
const choicesEl = document.getElementById("choices");
const nameInput = document.getElementById("playerName");
const startBtn = document.getElementById("startBtn");
const restartBtn = document.getElementById("restartBtn");
const hudEl = document.getElementById("hud");
const inventoryPanel = document.getElementById("inventoryPanel");
const inventoryGrid = document.getElementById("inventoryGrid");
const achievementsPanel = document.getElementById("achievementsPanel");

// Item definitions
const ITEMS = {
  healing_herb: { name: "Healing Herb", icon: "🌿" },
  capture_charm: { name: "Capture Charm", icon: "✨" },
  explorer_map: { name: "Explorer Map", icon: "🗺️" },
  companion_treat: { name: "Companion Treat", icon: "🍖" },
};

let state = null;

function newState() {
  return {
    name: (nameInput.value || "Keeper").trim(),
    health: 10,
    maxHealth: 10,
    coins: 0,
    luck: 0,
    courage: 0,
    inventory: {},
    achievements: [],
    captured: [],
    ended: false,
    currentScene: "intro",
  };
}

function renderHUD() {
  if (!state) return;
  document.getElementById("healthVal").textContent = `${state.health}/${state.maxHealth}`;
  document.getElementById("coinVal").textContent = state.coins;
  document.getElementById("luckVal").textContent = state.luck;
  document.getElementById("courageVal").textContent = state.courage;
}

function renderInventory() {
  if (!state) return;
  const inv = state.inventory;
  const keys = Object.keys(inv).filter(k => inv[k] > 0);
  
  if (keys.length === 0) {
    inventoryGrid.innerHTML = '<p class="empty-inv">Your pack is empty. Items appear here when found.</p>';
    return;
  }
  
  inventoryGrid.innerHTML = keys.map(key => {
    const item = ITEMS[key] || { name: key, icon: "📦" };
    return `<div class="inventory-item">${item.icon} ${item.name}<span class="count">${inv[key]}</span></div>`;
  }).join("");
}

function addItem(itemId, count = 1) {
  if (!state) return;
  state.inventory[itemId] = (state.inventory[itemId] || 0) + count;
  renderInventory();
}

function unlockAchievement(id) {
  if (!state || state.achievements.includes(id)) return;
  state.achievements.push(id);
  const el = document.querySelector(`.achievement[data-id="${id}"]`);
  if (el) {
    el.classList.remove("locked");
    el.classList.add("unlocked");
  }
}

function setScene(text, options = []) {
  storyEl.innerHTML = text;
  choicesEl.innerHTML = "";
  options.forEach((option) => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.innerHTML = option.label;
    btn.addEventListener("click", option.action);
    choicesEl.appendChild(btn);
  });
  renderHUD();
}

function ending(message) {
  state.ended = true;
  setScene(
    `${message}<br><br><em>You can <strong>Restart</strong> to try different choices, or play the full game with <code>python adventure_game.py</code></em>`,
    []
  );
}

function introScene() {
  state.currentScene = "intro";
  setScene(
    `Welcome to the Wildlands, <strong>${state.name}</strong>! You stand at Ridgecamp, a hub for Keepers. The wind carries whispers of creatures in nearby regions.`,
    [
      { label: "🌾 Visit Sunmeadow", action: sunmeadowScene },
      { label: "🏛️ Explore Old Ruins", action: ruinsScene },
      { label: "🌊 Check Silver River", action: riverScene },
    ]
  );
}

function sunmeadowScene() {
  state.currentScene = "sunmeadow";
  state.luck += 1;
  if (Math.random() > 0.5) {
    addItem("healing_herb", 1);
    setScene(
      "Sunmeadow stretches before you like a green ocean. You spot some healing herbs growing near a rabbit burrow. <strong>+1 Healing Herb added to inventory!</strong>",
      [
        { label: "🔍 Search for creatures", action: () => encounterScene("Moss Bunny", "meadow") },
        { label: "🗺️ Return to Ridgecamp", action: introScene },
      ]
    );
  } else {
    setScene(
      "Sunmeadow is peaceful today. The tall grass sways in the breeze, but you don't spot any creatures yet.",
      [
        { label: "🔍 Keep searching", action: () => encounterScene("Moss Bunny", "meadow") },
        { label: "🗺️ Return to Ridgecamp", action: introScene },
      ]
    );
  }
}

function ruinsScene() {
  state.currentScene = "ruins";
  state.courage += 1;
  setScene(
    "Old Ruins stand half-buried in moss. Echoes make every step feel like a story returning. You notice strange markings on the walls.",
    [
      { label: "🔍 Investigate the markings", action: () => encounterScene("Spark Finch", "ruins") },
      { label: "💰 Look for treasure", action: findCoinsScene },
      { label: "🗺️ Return to Ridgecamp", action: introScene },
    ]
  );
}

function riverScene() {
  state.currentScene = "river";
  setScene(
    "Silver River glitters under shifting light. Smooth stones mark safe crossings for careful Keepers.",
    [
      { label: "🔍 Watch for river creatures", action: () => encounterScene("Pebble Otter", "river") },
      { label: "🎣 Try fishing", action: fishingScene },
      { label: "🗺️ Return to Ridgecamp", action: introScene },
    ]
  );
}

function findCoinsScene() {
  const coins = Math.floor(Math.random() * 5) + 3;
  state.coins += coins;
  setScene(
    `You found an old Keeper's pouch! <strong>+${coins} coins</strong> added to your purse.`,
    [
      { label: "🗺️ Return to Ridgecamp", action: introScene },
    ]
  );
}

function fishingScene() {
  const roll = Math.random();
  if (roll > 0.6) {
    addItem("companion_treat", 1);
    setScene(
      "You caught something! A Companion Treat floats to the surface. <strong>+1 Companion Treat added!</strong>",
      [
        { label: "🗺️ Return to Ridgecamp", action: introScene },
      ]
    );
  } else {
    setScene(
      "The fish aren't biting today. But the peaceful moment restores your spirit.",
      [
        { label: "🗺️ Return to Ridgecamp", action: introScene },
      ]
    );
  }
}

function encounterScene(creatureName, region) {
  unlockAchievement("explorer");
  state.currentScene = "encounter";
  setScene(
    `A wild <strong>${creatureName}</strong> appears! It's ${region === "meadow" ? "nibbling on grass" : region === "ruins" ? "perched on a broken pillar" : "playing in the shallows"}. What do you do?`,
    [
      { label: "🎯 Attempt capture", action: () => captureScene(creatureName, region) },
      { label: "🍖 Use Companion Treat (if available)", action: () => useTreatScene(creatureName, region) },
      { label: "👋 Leave peacefully", action: () => leaveScene(creatureName) },
    ]
  );
}

function captureScene(creatureName, region) {
  const success = Math.random() > 0.4;
  if (success) {
    state.captured.push({ name: creatureName, region, bond: 1 });
    state.coins += 5;
    unlockAchievement("first_catch");
    if (state.captured.length >= 5) unlockAchievement("collector");
    setScene(
      `Success! You captured the <strong>${creatureName}</strong>! <strong>+5 coins</strong>. The creature seems calm in your presence.`,
      [
        { label: "🗺️ Return to Ridgecamp", action: introScene },
        { label: "🏆 Enter Exhibition", action: exhibitionScene },
      ]
    );
  } else {
    state.health -= 2;
    if (state.health <= 0) {
      ending("The creature broke free and you stumbled, exhausted. A fellow Keeper finds you and helps you back to camp. Better luck next time!");
      return;
    }
    setScene(
      `The ${creatureName} dodged your capture attempt! <strong>-2 health</strong>. The creature watches you carefully.`,
      [
        { label: "🔄 Try again", action: () => captureScene(creatureName, region) },
        { label: "👋 Leave peacefully", action: () => leaveScene(creatureName) },
      ]
    );
  }
}

function useTreatScene(creatureName, region) {
  if (state.inventory.companion_treat > 0) {
    state.inventory.companion_treat -= 1;
    renderInventory();
    setScene(
      `You offer a Companion Treat. The <strong>${creatureName}</strong> approaches cautiously and accepts it! It's more likely to bond with you now.`,
      [
        { label: "🎯 Attempt capture (boosted)", action: () => boostedCaptureScene(creatureName, region) },
        { label: "👋 Leave peacefully", action: () => leaveScene(creatureName) },
      ]
    );
  } else {
    setScene(
      `You don't have any Companion Treats. Try fishing at the river or exploring to find some!`,
      [
        { label: "🎯 Attempt capture anyway", action: () => captureScene(creatureName, region) },
        { label: "👋 Leave peacefully", action: () => leaveScene(creatureName) },
      ]
    );
  }
}

function boostedCaptureScene(creatureName, region) {
  const success = Math.random() > 0.2;
  if (success) {
    state.captured.push({ name: creatureName, region, bond: 2 });
    state.coins += 5;
    unlockAchievement("first_catch");
    setScene(
      `The treat worked! The <strong>${creatureName}</strong> trusts you and enters your care willingly. <strong>+5 coins</strong> and <strong>+2 bond</strong>!`,
      [
        { label: "🗺️ Return to Ridgecamp", action: introScene },
        { label: "🏆 Enter Exhibition", action: exhibitionScene },
      ]
    );
  } else {
    state.health -= 1;
    setScene(
      `Even with the treat, the ${creatureName} is skittish and escapes! <strong>-1 health</strong>.`,
      [
        { label: "🗺️ Return to Ridgecamp", action: introScene },
      ]
    );
  }
}

function leaveScene(creatureName) {
  setScene(
    `You leave the ${creatureName} in peace. Not every encounter needs to end in capture. The Wildlands respect your choice.`,
    [
      { label: "🗺️ Return to Ridgecamp", action: introScene },
    ]
  );
}

function exhibitionScene() {
  if (state.captured.length === 0) {
    setScene(
      "You need at least one companion to enter an exhibition. Go catch some creatures first!",
      [
        { label: "🗺️ Return to Ridgecamp", action: introScene },
      ]
    );
    return;
  }
  unlockAchievement("exhibition_champion");
  const companion = state.captured[state.captured.length - 1];
  const strategies = ["strength", "speed", "bond"];
  const strategy = strategies[Math.floor(Math.random() * strategies.length)];
  const score = Math.floor(Math.random() * 40) + 60;
  const rewards = Math.floor(score / 10);
  state.coins += rewards;
  
  setScene(
    `<strong>🏆 Exhibition Complete!</strong><br><br>Your ${companion.name} performed with ${strategy} strategy.<br>Score: <strong>${score}/100</strong><br>Reward: <strong>+${rewards} coins</strong>!<br><br>The crowd cheers for your performance!`,
    [
      { label: "🗺️ Return to Ridgecamp", action: introScene },
      { label: "🎭 Another exhibition", action: exhibitionScene },
    ]
  );
}

startBtn.addEventListener("click", () => {
  state = newState();
  hudEl.classList.remove("hidden");
  inventoryPanel.classList.remove("hidden");
  achievementsPanel.classList.remove("hidden");
  restartBtn.classList.remove("hidden");
  startBtn.classList.add("hidden");
  introScene();
});

restartBtn.addEventListener("click", () => {
  state = newState();
  // Reset achievements display
  document.querySelectorAll(".achievement").forEach(el => {
    el.classList.remove("unlocked");
    el.classList.add("locked");
  });
  renderInventory();
  renderHUD();
  introScene();
});

// Initialize
hudEl?.classList.add("hidden");
