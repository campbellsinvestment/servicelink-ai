import {
  renderRecommendationRow,
  renderStatusMessage,
} from "../components.js";

export function renderRecommendationsPage(recommendations) {
  if (!recommendations.length) {
    return `
      <section>
        ${renderStatusMessage("No recommendations in the current datasets.")}
      </section>
    `;
  }

  const matchedPostCount = new Set(
    recommendations.map((recommendation) => recommendation.post_id),
  ).size;

  const rows = recommendations
    .map((recommendation) => renderRecommendationRow(recommendation))
    .join("");

  return `
    <section>
      <p class="page-intro">
        ${recommendations.length} ranked recommendations across ${matchedPostCount} posts.
      </p>
      <ul class="match-list">
        ${rows}
      </ul>
    </section>
  `;
}
