import {
  renderRecommendationCard,
  renderStatusMessage,
} from "../components.js";

export function renderRecommendationsPage(recommendations) {
  if (!recommendations.length) {
    return `
      <section>
        <h2 class="page-title">Recommendations</h2>
        ${renderStatusMessage("No recommendations matched the current datasets.")}
      </section>
    `;
  }

  const cards = recommendations
    .map((recommendation) => renderRecommendationCard(recommendation))
    .join("");

  return `
    <section>
      <h2 class="page-title">Recommendations</h2>
      <p class="page-description">
        Ranked, explainable matches between enriched Reddit posts and
        normalized Alberta community services.
      </p>
      <div class="recommendation-list">
        ${cards}
      </div>
    </section>
  `;
}
