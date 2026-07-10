import "@abgov/web-components";
import "./styles/main.css";

import { fetchDashboardData, fetchRecommendations } from "./js/api.js";
import { renderDashboard } from "./js/pages/dashboard.js";
import { renderRecommendationsPage } from "./js/pages/recommendations.js";
import { renderStatusMessage } from "./js/components.js";

const PAGES = {
  dashboard: {
    label: "Dashboard",
    load: fetchDashboardData,
    render: renderDashboard,
  },
  recommendations: {
    label: "Recommendations",
    load: fetchRecommendations,
    render: renderRecommendationsPage,
  },
};

function renderShell(activePageKey) {
  const navigation = Object.entries(PAGES)
    .map(([key, page]) => {
      const activeClass = key === activePageKey ? " is-active" : "";

      return `
        <button
          class="app-nav__button${activeClass}"
          type="button"
          data-page="${key}"
        >
          ${page.label}
        </button>
      `;
    })
    .join("");

  return `
    <div class="app-shell">
      <header class="app-header">
        <div class="app-header__inner">
          <h1 class="app-header__title">Alberta Community Intelligence Engine</h1>
          <p class="app-header__subtitle">
            Research dashboard for community-service discovery, social-post
            enrichment, and explainable recommendations.
          </p>
        </div>
      </header>
      <nav class="app-nav" aria-label="Primary">
        <div class="app-nav__inner">
          ${navigation}
        </div>
      </nav>
      <main class="app-main">
        <div class="app-main__inner" id="page-content">
          ${renderStatusMessage("Loading dashboard data...")}
        </div>
      </main>
    </div>
  `;
}

async function renderPage(pageKey) {
  const page = PAGES[pageKey];
  const content = document.getElementById("page-content");

  if (!page || !content) {
    return;
  }

  content.innerHTML = renderStatusMessage(`Loading ${page.label.toLowerCase()}...`);

  try {
    const data = await page.load();
    content.innerHTML = page.render(data);
  } catch (error) {
    content.innerHTML = renderStatusMessage(
      `Unable to load ${page.label.toLowerCase()}. Start the FastAPI server on port 8000.`,
      { isError: true },
    );
    console.error(error);
  }
}

function bindNavigation() {
  document.querySelectorAll("[data-page]").forEach((button) => {
    button.addEventListener("click", () => {
      const pageKey = button.getAttribute("data-page");

      if (!pageKey) {
        return;
      }

      document.querySelectorAll(".app-nav__button").forEach((navButton) => {
        navButton.classList.toggle(
          "is-active",
          navButton.getAttribute("data-page") === pageKey,
        );
      });

      renderPage(pageKey);
    });
  });
}

function initApp() {
  const app = document.getElementById("app");

  if (!app) {
    return;
  }

  app.innerHTML = renderShell("dashboard");
  bindNavigation();
  renderPage("dashboard");
}

initApp();
