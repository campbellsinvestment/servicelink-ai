import {
  renderRecommendationItem,
  renderStatItem,
  renderStatusMessage,
} from "../components.js";

export function renderDashboard({
  health,
  services,
  redditSummary,
  jobSummary,
  recommendations,
}) {
  const topRecommendation = recommendations[0];

  return `
    <section>
      <div class="page-heading">
        <h2 class="page-title">Overview</h2>
        <p class="page-description">
          Normalized services, social posts, and explainable recommendations.
        </p>
      </div>

      <ul class="stats-row">
        ${renderStatItem("Status", health.status)}
        ${renderStatItem("Services", services.length)}
        ${renderStatItem("Posts", redditSummary.total_posts)}
        ${renderStatItem("Jobs", jobSummary.total_jobs)}
        ${renderStatItem("Matches", recommendations.length)}
      </ul>

      <p class="section-label">Top match</p>
      ${
        topRecommendation
          ? `<ul class="recommendation-list">${renderRecommendationItem(topRecommendation, { showSummary: true })}</ul>`
          : renderStatusMessage("No matches yet.")
      }

      <p class="meta-line">
        Sources: ${redditSummary.communities.join(", ")} ·
        ${jobSummary.sources.join(", ")}
      </p>
    </section>
  `;
}
