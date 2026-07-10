const FALLBACK_API_BASE = "http://localhost:8000";

let demoDataPromise = null;

function isDemoMode() {
  return ACIE_DEMO_MODE;
}

async function loadDemoData() {
  if (!demoDataPromise) {
    demoDataPromise = import("../demo/demo.json").then((module) => module.default);
  }

  return demoDataPromise;
}

export function getApiBaseUrl() {
  return window.ACIE_API_BASE || ACIE_API_BASE_DEFAULT || FALLBACK_API_BASE;
}

export function isDemoBuild() {
  return isDemoMode();
}

export async function fetchJson(path) {
  if (isDemoMode()) {
    const demo = await loadDemoData();
    const payload = demo.endpoints[path];

    if (payload === undefined) {
      throw new Error(`Demo data missing for ${path}`);
    }

    return payload;
  }

  const response = await fetch(`${getApiBaseUrl()}${path}`);

  if (!response.ok) {
    throw new Error(`Request failed for ${path}: ${response.status}`);
  }

  return response.json();
}

export function fetchDashboardData() {
  return Promise.all([
    fetchJson("/services"),
    fetchJson("/social-posts/reddit/summary"),
    fetchJson("/recommendations"),
  ]).then(([services, redditSummary, recommendations]) => ({
    services,
    redditSummary,
    recommendations,
  }));
}

export function fetchRecommendations() {
  return fetchJson("/recommendations");
}

export function fetchGraphData() {
  return Promise.all([
    fetchJson("/social-posts/reddit"),
    fetchJson("/job-postings"),
    fetchJson("/services"),
    fetchJson("/entity-links"),
    fetchJson("/job-links"),
  ]).then(([posts, jobs, services, links, jobLinks]) => ({
    posts,
    jobs,
    services,
    links,
    jobLinks,
  }));
}
