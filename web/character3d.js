/**
 * Wildlands 3D — Simple character you can design and walk around with keyboard.
 * Three.js from CDN; WASD + mouse look (PointerLock); design panel for color and height.
 */
import * as THREE from "three";

const canvas = document.getElementById("canvas");
const ui = document.getElementById("ui");
const designPanel = document.getElementById("design-panel");
const colorPicker = document.getElementById("colorPicker");
const heightSlider = document.getElementById("heightSlider");
const heightValue = document.getElementById("heightValue");
const designDone = document.getElementById("designDone");

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);
scene.fog = new THREE.Fog(0x87ceeb, 20, 80);

// Camera (will follow character)
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 500);
camera.position.set(0, 4, 8);

// Renderer
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Lights
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

// Ground
const groundGeo = new THREE.PlaneGeometry(120, 120);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x3d6b2e });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Simple obstacles to walk around
const boxGeo = new THREE.BoxGeometry(4, 3, 2);
const boxMat = new THREE.MeshStandardMaterial({ color: 0x8b7355 });
[-15, 10, -10].forEach((z, i) => {
  const box = new THREE.Mesh(boxGeo, boxMat.clone());
  box.position.set(i * 12 - 10, 1.5, z);
  box.castShadow = true;
  box.receiveShadow = true;
  scene.add(box);
});

// --- Character (body + head group) ---
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
  group.userData.headMat = headMat;
  return group;
}

let character = createCharacter(0x4a9fd4);
scene.add(character);

// Movement state
const keys = { w: false, a: false, s: false, d: false };
const velocity = new THREE.Vector3(0, 0, 0);
const direction = new THREE.Vector3(0, 0, -1);
const moveSpeed = 8;
const turnSpeed = 0.002;
let yaw = 0;       // character/camera rotation around Y (radians)
let pitch = 0.2;    // camera pitch (look up/down), clamped
let pointerLocked = false;

// Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Pointer lock
canvas.addEventListener("click", () => {
  if (!pointerLocked) canvas.requestPointerLock();
});

document.addEventListener("pointerlockchange", () => {
  pointerLocked = document.pointerLockElement === canvas;
  ui.style.visibility = pointerLocked ? "visible" : "visible";
});

document.addEventListener("pointerlockerror", () => {
  pointerLocked = false;
});

// Mouse look
document.addEventListener("mousemove", (e) => {
  if (!pointerLocked) return;
  yaw -= e.movementX * turnSpeed;
  pitch -= e.movementY * turnSpeed;
  pitch = Math.max(-0.6, Math.min(0.6, pitch));
});

// Keyboard
document.addEventListener("keydown", (e) => {
  const k = e.code.toLowerCase();
  if (k === "keyw") keys.w = true;
  if (k === "keya") keys.a = true;
  if (k === "keys") keys.s = true;
  if (k === "keyd") keys.d = true;
  if (k === "keyc") {
    e.preventDefault();
    designPanel.classList.toggle("hidden");
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
  }
});

// Design panel
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

// Update: move character, then camera
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);

  if (pointerLocked) {
    let vx = 0, vz = 0;
    if (keys.w) { vz -= 1; }
    if (keys.s) { vz += 1; }
    if (keys.a) { vx -= 1; }
    if (keys.d) { vx += 1; }
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

  // Third-person camera: behind and above character
  const camDist = 6;
  const camHeight = 3;
  const tx = character.position.x - Math.sin(yaw) * camDist;
  const tz = character.position.z - Math.cos(yaw) * camDist;
  const ty = character.position.y + camHeight;
  camera.position.lerp(new THREE.Vector3(tx, ty, tz), 0.1);
  camera.lookAt(character.position.x, character.position.y + 1.2, character.position.z);

  renderer.render(scene, camera);
}
animate();
