import {
  renderFeaturedMatch,
  renderStatItem,
  renderStatusMessage,
} from "../components.js";

export function renderDashboard({
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

      <div class="home-section best-match-panel">
        <h2 class="section-title section-title--prominent">Best match</h2>
        ${
          topRecommendation
            ? renderFeaturedMatch(topRecommendation)
            : renderStatusMessage("No matches yet.")
        }
      </div>
    </section>
  `;
}
