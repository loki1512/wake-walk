/* ======================================================
   AUTH + TOKEN HELPERS
====================================================== */

function getToken() {
  return localStorage.getItem("jwt");
}

function setToken(token) {
  localStorage.setItem("jwt", token);
}

function logout() {
  localStorage.removeItem("jwt");
  window.location.href = "/login";
}

/* ======================================================
   PAGE GUARDS
====================================================== */

// Protect dashboard
if (window.location.pathname === "/" && !getToken()) {
  window.location.href = "/login";
}

/* ======================================================
   LOGIN
====================================================== */

const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
  loginBtn.addEventListener("click", async () => {
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();
    const errorEl = document.getElementById("login-error");

    if (!username || !password) {
      errorEl.textContent = "Enter username and password.";
      return;
    }

    const res = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (data.error) {
      errorEl.textContent = data.error;
      return;
    }

    setToken(data.token);

    // Optional welcome animation handled by CSS
    setTimeout(() => {
      window.location.href = "/";
    }, 600);
  });
}

/* ======================================================
   SIGNUP
====================================================== */

const signupBtn = document.getElementById("signupBtn");
if (signupBtn) {
  signupBtn.addEventListener("click", async () => {
    const username = document.getElementById("signup-username").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const password = document.getElementById("signup-password").value.trim();
    const errorEl = document.getElementById("signup-error");

    if (!username || !email || !password) {
      errorEl.textContent = "All fields are required.";
      return;
    }

    const res = await fetch("/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();

    if (data.error) {
      errorEl.textContent = data.error;
      return;
    }

    setToken(data.token);

    setTimeout(() => {
      window.location.href = "/";
    }, 600);
  });
}

/* ======================================================
   DASHBOARD LOAD
====================================================== */

async function loadDashboard() {
  if (window.location.pathname !== "/") return;

  const token = getToken();
  if (!token) return logout();

  // Today
  const todayEl = document.getElementById("todayDisplay");
  if (todayEl) {
    todayEl.textContent = new Date().toISOString().split("T")[0];
  }

  // Stats
  const statsRes = await fetch("/api/stats", {
    headers: { Authorization: "Bearer " + token }
  });

  if (statsRes.status === 401) return logout();

  const stats = await statsRes.json();

  document.getElementById("currentStreak").textContent = stats.current;
  document.getElementById("bestStreak").textContent = stats.best;

  // Recent table
  loadRecentEntries();
}

async function loadRecentEntries() {
  const token = getToken();
  if (!token) return;

  const res = await fetch("/recent", {
    headers: { Authorization: "Bearer " + token }
  });

  if (res.status === 401) return logout();

  const rows = await res.json();
  const tbody = document.getElementById("recentBody");

  if (!tbody) return;
  tbody.innerHTML = "";

  rows.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${r.entry_date}</td>
      <td>${r.wake_time ? r.wake_time : "-"}</td>
      <td>${r.walk_minutes ?? "-"}</td>
    `;
    tbody.appendChild(tr);
  });
}

/* ======================================================
   MODALS
====================================================== */

const loadingModal = document.getElementById("loadingModal");
const successModal = document.getElementById("successModal");

function showLoading() {
  if (loadingModal) loadingModal.classList.remove("hidden");
}

function hideLoading() {
  if (loadingModal) loadingModal.classList.add("hidden");
}

function showSuccess() {
  if (!successModal) return;
  successModal.classList.remove("hidden");
  setTimeout(() => successModal.classList.add("hidden"), 1200);
}

/* ======================================================
   MASCOT (SUBTLE)
====================================================== */

function celebrateMascot() {
  const m = document.getElementById("dashboardMascot");
  if (!m) return;

  m.src = "/static/assets/mascot/mascot-dancing.png";
  m.classList.remove("mascot-idle");
  m.classList.add("mascot-celebrate");

  setTimeout(() => {
    m.src = "/static/assets/mascot/mascot-happy.png";
    m.classList.remove("mascot-celebrate");
    m.classList.add("mascot-idle");
  }, 1500);
}

/* ======================================================
   CONFETTI (ONLY ON STREAK UP)
====================================================== */

function fireConfetti() {
  const canvas = document.getElementById("confettiCanvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  canvas.classList.remove("hidden");

  const pieces = Array.from({ length: 100 }).map(() => ({
    x: Math.random() * canvas.width,
    y: -20,
    size: Math.random() * 6 + 4,
    speed: Math.random() * 3 + 2,
    color: `hsl(${Math.random() * 360}, 80%, 60%)`
  }));

  function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pieces.forEach(p => {
      p.y += p.speed;
      ctx.fillStyle = p.color;
      ctx.fillRect(p.x, p.y, p.size, p.size);
    });
    requestAnimationFrame(update);
  }

  update();
  setTimeout(() => canvas.classList.add("hidden"), 1600);
}

/* ======================================================
   WAKE / WALK ACTIONS
====================================================== */

const wakeupBtn = document.getElementById("wakeupBtn");
if (wakeupBtn) {
  wakeupBtn.addEventListener("click", async () => {
    const token = getToken();
    if (!token) return logout();

    showLoading();

    const res = await fetch("/api/wakeup", {
      method: "POST",
      headers: { Authorization: "Bearer " + token }
    });

    const data = await res.json();
    hideLoading();

    if (data.streak_increased) {
      celebrateMascot();
      showSuccess();
      fireConfetti();
    }

    setTimeout(() => location.reload(), 800);
  });
}

const walkBtn = document.getElementById("walkBtn");
if (walkBtn) {
  walkBtn.addEventListener("click", async () => {
    const token = getToken();
    if (!token) return logout();

    const minutes = parseInt(document.getElementById("walkMinutes").value);
    if (!minutes || minutes <= 0) {
      alert("Enter walk minutes (1+)");
      return;
    }

    showLoading();

    const res = await fetch("/api/walk", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token
      },
      body: JSON.stringify({ minutes })
    });

    const data = await res.json();
    hideLoading();

    if (data.streak_increased) {
      celebrateMascot();
      showSuccess();
      fireConfetti();
    }

    setTimeout(() => location.reload(), 800);
  });
}

/* ======================================================
   LOGOUT
====================================================== */

const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", logout);
}

/* ======================================================
   INIT
====================================================== */

loadDashboard();
