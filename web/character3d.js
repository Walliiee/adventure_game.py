/**
 * Wildlands 3D — Milestone 1 interaction shell.
 * Three.js from CDN; WASD + mouse look (PointerLock);
 * design panel + Teacher interaction vertical slice.
 */
import * as THREE from "three";

const canvas = document.getElementById("canvas");
const ui = document.getElementById("ui");
const designPanel = document.getElementById("design-panel");
const colorPicker = document.getElementById("colorPicker");
const heightSlider = document.getElementById("heightSlider");
const heightValue = document.getElementById("heightValue");
const designDone = document.getElementById("designDone");

const objectiveText = document.getElementById("objectiveText");
const promptText = document.getElementById("promptText");
const toast = document.getElementById("toast");
const interactionPanel = document.getElementById("interaction-panel");
const interactionTitle = document.getElementById("interaction-title");
const interactionQuestion = document.getElementById("interaction-question");
const interactionAnswers = document.getElementById("interaction-answers");

const state = {
  objectiveDone: false,
  activeNpc: null,
  interactionOpen: false,
};

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);
scene.fog = new THREE.Fog(0x87ceeb, 20, 80);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 500);
camera.position.set(0, 4, 8);

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const ambient = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffffff, 0.9);
sun.position.set(20, 30, 10);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 100;
sun.shadow.camera.left = -30;
sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30;
sun.shadow.camera.bottom = -30;
sun.shadow.bias = -0.0001;
scene.add(sun);

const groundGeo = new THREE.PlaneGeometry(120, 120);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x3d6b2e });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

const boxGeo = new THREE.BoxGeometry(4, 3, 2);
const boxMat = new THREE.MeshStandardMaterial({ color: 0x8b7355 });
[-15, 10, -10].forEach((z, i) => {
  const box = new THREE.Mesh(boxGeo, boxMat.clone());
  box.position.set(i * 12 - 10, 1.5, z);
  box.castShadow = true;
  box.receiveShadow = true;
  scene.add(box);
});

function createCharacter(colorHex = 0x4a9fd4) {
  const group = new THREE.Group();

  const bodyGeo = new THREE.CylinderGeometry(0.35, 0.4, 0.9, 12);
  const bodyMat = new THREE.MeshStandardMaterial({ color: colorHex });
  const body = new THREE.Mesh(bodyGeo, bodyMat);
  body.position.y = 0.45;
  body.castShadow = true;
  group.add(body);

  const headGeo = new THREE.SphereGeometry(0.32, 12, 12);
  const headMat = new THREE.MeshStandardMaterial({ color: 0xffdbac });
  const head = new THREE.Mesh(headGeo, headMat);
  head.position.y = 1.0;
  head.castShadow = true;
  group.add(head);

  group.position.set(0, 0, 0);
  group.userData.bodyMat = bodyMat;
  return group;
}

function addTeacherMarker() {
  const group = new THREE.Group();
  const post = new THREE.Mesh(
    new THREE.CylinderGeometry(0.25, 0.25, 1.4, 10),
    new THREE.MeshStandardMaterial({ color: 0x2f6fff })
  );
  post.position.y = 0.7;
  const orb = new THREE.Mesh(
    new THREE.SphereGeometry(0.35, 12, 12),
    new THREE.MeshStandardMaterial({ color: 0x79a8ff, emissive: 0x16346d, emissiveIntensity: 0.5 })
  );
  orb.position.y = 1.65;
  group.add(post);
  group.add(orb);
  group.position.set(6, 0, -5);
  group.userData.npc = "Teacher";
  scene.add(group);
  return group;
}

const teacherQuestion = {
  text: "Teacher asks: Why classify habitats by region?",
  options: [
    "For decoration only",
    "To match creatures with likely environments",
    "To make maps harder",
    "No reason",
  ],
  correct: 1,
};

let character = createCharacter(0x4a9fd4);
scene.add(character);
const teacherMarker = addTeacherMarker();

const keys = { w: false, a: false, s: false, d: false };
const moveSpeed = 8;
const turnSpeed = 0.002;
let yaw = 0;
let pitch = 0.2;
let pointerLocked = false;

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

canvas.addEventListener("click", () => {
  if (!pointerLocked && !state.interactionOpen) canvas.requestPointerLock();
});

document.addEventListener("pointerlockchange", () => {
  pointerLocked = document.pointerLockElement === canvas;
  ui.style.visibility = "visible";
});

document.addEventListener("pointerlockerror", () => {
  pointerLocked = false;
});

document.addEventListener("mousemove", (e) => {
  if (!pointerLocked || state.interactionOpen) return;
  yaw -= e.movementX * turnSpeed;
  pitch -= e.movementY * turnSpeed;
  pitch = Math.max(-0.6, Math.min(0.6, pitch));
});

function showToast(text) {
  toast.textContent = text;
  toast.style.display = "block";
  setTimeout(() => {
    toast.style.display = "none";
  }, 1600);
}

function setObjectiveText() {
  if (state.objectiveDone) {
    objectiveText.textContent = "Great job. Milestone 1 complete: Teacher interaction done.";
  } else {
    objectiveText.textContent = "Find Teacher and answer one Smarts question.";
  }
}

function openTeacherInteraction() {
  state.interactionOpen = true;
  if (document.pointerLockElement === canvas) document.exitPointerLock();

  interactionTitle.textContent = "Teacher Session — Smarts";
  interactionQuestion.textContent = teacherQuestion.text;
  interactionAnswers.innerHTML = "";
  teacherQuestion.options.forEach((opt, idx) => {
    const btn = document.createElement("button");
    btn.className = "answer-btn";
    btn.type = "button";
    btn.textContent = opt;
    btn.addEventListener("click", () => {
      const correct = idx === teacherQuestion.correct;
      if (correct) {
        state.objectiveDone = true;
        showToast("Correct! +1 Smarts. Objective complete.");
      } else {
        showToast("Not quite — keep practicing.");
      }
      setObjectiveText();
      state.interactionOpen = false;
      interactionPanel.classList.add("hidden");
    });
    interactionAnswers.appendChild(btn);
  });

  interactionPanel.classList.remove("hidden");
}

document.addEventListener("keydown", (e) => {
  const k = e.code.toLowerCase();

  if (!state.interactionOpen) {
    if (k === "keyw") keys.w = true;
    if (k === "keya") keys.a = true;
    if (k === "keys") keys.s = true;
    if (k === "keyd") keys.d = true;
  }

  if (k === "keyc") {
    e.preventDefault();
    designPanel.classList.toggle("hidden");
  }

  if (k === "keye" && state.activeNpc === "Teacher" && !state.interactionOpen) {
    openTeacherInteraction();
  }
});

document.addEventListener("keyup", (e) => {
  const k = e.code.toLowerCase();
  if (k === "keyw") keys.w = false;
  if (k === "keya") keys.a = false;
  if (k === "keys") keys.s = false;
  if (k === "keyd") keys.d = false;
  if (e.code === "Escape") {
    if (document.pointerLockElement === canvas) document.exitPointerLock();
    designPanel.classList.add("hidden");
    interactionPanel.classList.add("hidden");
    state.interactionOpen = false;
  }
});

colorPicker.addEventListener("input", () => {
  character.userData.bodyMat.color.setStyle(colorPicker.value);
});
heightSlider.addEventListener("input", () => {
  const h = parseFloat(heightSlider.value);
  heightValue.textContent = h.toFixed(1);
  character.scale.setScalar(h);
});
designDone.addEventListener("click", () => {
  designPanel.classList.add("hidden");
});

setObjectiveText();

const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);

  const toTeacher = character.position.distanceTo(teacherMarker.position);
  if (toTeacher < 2.5) {
    state.activeNpc = "Teacher";
    promptText.textContent = state.objectiveDone
      ? "Objective complete. Explore or press C to redesign."
      : "Press E to interact with Teacher.";
  } else {
    state.activeNpc = null;
    promptText.textContent = state.objectiveDone
      ? "Objective complete. Explore or press C to redesign."
      : "Move toward the blue marker to find Teacher.";
  }

  if (pointerLocked && !state.interactionOpen) {
    let vx = 0;
    let vz = 0;
    if (keys.w) vz -= 1;
    if (keys.s) vz += 1;
    if (keys.a) vx -= 1;
    if (keys.d) vx += 1;
    if (vx !== 0 || vz !== 0) {
      const len = Math.hypot(vx, vz);
      vx /= len;
      vz /= len;
      const cos = Math.cos(yaw);
      const sin = Math.sin(yaw);
      const wx = vx * cos - vz * sin;
      const wz = vx * sin + vz * cos;
      character.position.x += wx * moveSpeed * dt;
      character.position.z += wz * moveSpeed * dt;
      character.rotation.y = yaw;
    }
    character.position.y = 0;
  }

  const camDist = 6;
  const camHeight = 3;
  const tx = character.position.x - Math.sin(yaw) * camDist;
  const tz = character.position.z - Math.cos(yaw) * camDist;
  const ty = character.position.y + camHeight;
  camera.position.lerp(new THREE.Vector3(tx, ty, tz), 0.1);
  camera.lookAt(character.position.x, character.position.y + 1.2 + pitch, character.position.z);

  renderer.render(scene, camera);
}
animate();
