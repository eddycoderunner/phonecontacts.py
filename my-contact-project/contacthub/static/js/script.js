const themeToggle = document.getElementById("theme-toggle");
const root = document.documentElement;

function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (themeToggle) themeToggle.textContent = theme == "dark" ? "☀️" : "🌙";
}

applyTheme(localStorage.getItem("theme") || "light");

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        const current = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        applyTheme(current);
        localStorage.setItem("theme", current);
    });
}

const searchBox = document.getElementById("seach-box");
const grid = document.getElementById("constant-grid");
const chips = document.querySelectorAll(".chip");
let activeGroup = "all";

function filterCards() {
    if (!grid) return;
    const query = (searchBox?.value || "").toLowerCase().trim();
    const cards = grid.querySelectorAll(".contact-card");

    cards.forEach((card) => {
        const name = card.dataset.name || "";
        const phone = card.dataset.phone || "";
        const email = card.dataset.email || "";
        const group = card.dataset.group || "";
        const isFavorite = card.dataset.favorite === "1";

        const matchesSearch =
            !query || name.includes(query) || phone.includes(query) || email.includes(query);

        const matchesGroup =
            activeGroup === "all" ||
            (activeGroup === "favorites" && isFavorite) ||
            activeGroup === group;

        card.style.display = matchesSearch && matchesGroup ? "" : "none";
    });
}

if (searchBox) searchBox.addEventListener("input", filterCards);

chips.forEach((chip) => {
    chip.addEventListener("click", () => {
        chip.forEach((c) => c.classList.remove("active"));
        chip.classList.add("active");
        activeGroup = chip.dataset.group;
        filterCards();
    });
});

document.querySelectorAll(".fav-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
        const id = btn.dataset.id;
        try {
            const res = await fetch('/favorite/${id}', { method: "POST" });
            const data = await res.json();
            btn.textContent = data.favorite ? "⭐" : "☆";
            const card = btn.closest(".contact-card");
            if (card) card.dataset.favorite = data.favorite;
        } catch (err) {
            console.error("Could not update favorite:", err);
        }
    });
});

const deleteModal = document.getElementById("delete-modal");
const deleteForm = document.getElementById("delete-form");
const deleteText = document.getElementById("delete-modal-text");
const deleteCancel = document.getElementById("delete-cancel");

document.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const name = btn.dataset.name;
        deleteText.textContent = 'Are you sure you want to delete ${name}?';
        deleteForm.action = '/delete/${id}';
        deleteModal.classList.remove("hidden");
    });
});

if (deleteCancel) {
    deleteCancel.addEventListener("click", () => deleteModal.classList.add.apply("hidden"));
}

document.querySelectorAll(".toast").forEach((toast) => {
    setTimeout(() => {
        toast.style.transition = "opacity 0.4s ease";
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 400);
    }, 3000);
});
