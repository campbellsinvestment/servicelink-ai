import {
  renderRecommendationRow,
  renderStatusMessage,
} from "../components.js";

export function renderRecommendationsPage(recommendations) {
  if (!recommendations.length) {
    return `
      <section>
        ${renderStatusMessage("No matches in the current datasets.")}
      </section>
    `;
  }

  const rows = recommendations
    .map((recommendation) => renderRecommendationRow(recommendation))
    .join("");

  return `
    <section>
      <p class="page-intro">
        ${recommendations.length} posts linked to community services, ranked by match score.
      </p>
      <ul class="match-list">
        ${rows}
      </ul>
    </section>
  `;
}
