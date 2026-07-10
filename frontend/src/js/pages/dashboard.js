import {
  renderFeaturedMatch,
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
      <ul class="stats-row">
        ${renderStatItem("Services", services.length)}
        ${renderStatItem("Posts", redditSummary.total_posts)}
        ${renderStatItem("Jobs", jobSummary.total_jobs)}
        ${renderStatItem("Matches", recommendations.length)}
      </ul>

      <div class="home-section">
        <h2 class="section-title">Best match</h2>
        ${
          topRecommendation
            ? renderFeaturedMatch(topRecommendation)
            : renderStatusMessage("No matches yet.")
        }
      </div>

      <p class="footnote">
        API ${health.status} · ${recommendations.length} ranked recommendations available
      </p>
    </section>
  `;
}
