import {
  renderRecommendationItem,
  renderStatusMessage,
} from "../components.js";

export function renderRecommendationsPage(recommendations) {
  if (!recommendations.length) {
    return `
      <section>
        <div class="page-heading">
          <h2 class="page-title">Recommendations</h2>
        </div>
        ${renderStatusMessage("No matches in the current datasets.")}
      </section>
    `;
  }

  const items = recommendations
    .map((recommendation) => renderRecommendationItem(recommendation))
    .join("");

  return `
    <section>
      <div class="page-heading">
        <h2 class="page-title">Recommendations</h2>
        <p class="page-description">
          Ranked links between Reddit posts and community services.
        </p>
      </div>
      <ul class="recommendation-list">
        ${items}
      </ul>
    </section>
  `;
}
