import {
  renderFeaturedMatch,
  renderStatItem,
  renderStatusMessage,
} from "../components.js";

export function renderDashboard({
  services,
  redditSummary,
  recommendations,
}) {
  const topRecommendation = recommendations[0];
  const matchedPostCount = new Set(
    recommendations.map((recommendation) => recommendation.post_id),
  ).size;

  return `
    <section>
      <ul class="stats-row">
        ${renderStatItem("Services", services.length)}
        ${renderStatItem("Posts", redditSummary.total_posts)}
        ${renderStatItem("Posts matched", matchedPostCount)}
        ${renderStatItem("Recommendations", recommendations.length)}
      </ul>

      <div class="home-section">
        <h2 class="section-title section-title--prominent">Best match</h2>
        <div class="best-match-panel">
          ${
            topRecommendation
              ? renderFeaturedMatch(topRecommendation)
              : renderStatusMessage("No matches yet.")
          }
        </div>
      </div>
    </section>
  `;
}
