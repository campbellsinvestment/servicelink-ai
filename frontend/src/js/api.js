const DEFAULT_API_BASE = "http://localhost:8000";

export function getApiBaseUrl() {
  return window.ACIE_API_BASE || DEFAULT_API_BASE;
}

export async function fetchJson(path) {
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
    fetchJson("/services"),
    fetchJson("/entity-links"),
  ]).then(([posts, services, links]) => ({
    posts,
    services,
    links,
  }));
}
