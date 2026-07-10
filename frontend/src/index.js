import "./styles/main.css";

import { fetchDashboardData, fetchGraphData, fetchRecommendations } from "./js/api.js";
import { renderDashboard } from "./js/pages/dashboard.js";
import { mountGraphPage, renderGraphPage } from "./js/pages/graph.js";
import { renderRecommendationsPage } from "./js/pages/recommendations.js";
import { renderStatusMessage } from "./js/components.js";
import { renderAppFooter, renderHeaderActions } from "./js/links.js";

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
  graph: {
    label: "Graph",
    load: fetchGraphData,
    render: renderGraphPage,
    mount: mountGraphPage,
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
        <div class="shell-inner app-header__inner">
          <div>
            <p class="app-header__eyebrow">Alberta Community Intelligence Engine</p>
            <h1 class="app-header__title">ACIE</h1>
          </div>
          ${renderHeaderActions()}
        </div>
      </header>
      <nav class="app-nav" aria-label="Primary">
        <div class="shell-inner app-nav__inner">
          ${navigation}
        </div>
      </nav>
      <main class="app-main">
        <div class="shell-inner" id="page-content">
          ${renderStatusMessage("Loading...")}
        </div>
      </main>
      ${renderAppFooter()}
    </div>
  `;
}

async function renderPage(pageKey) {
  const page = PAGES[pageKey];
  const content = document.getElementById("page-content");

  if (!page || !content) {
    return;
  }

  content.innerHTML = renderStatusMessage("Loading...");

  try {
    const data = await page.load();
    content.innerHTML = page.render(data);

    if (page.mount) {
      page.mount(content, data);
    }
  } catch (error) {
    content.innerHTML = renderStatusMessage(
      "Unable to reach the API. Start the server on port 8000.",
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
