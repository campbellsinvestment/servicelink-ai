import {
  renderRecommendationCard,
  renderStatCard,
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
      <h2 class="page-title">Dashboard</h2>
      <p class="page-description">
        Overview of normalized community services, social posts, job records,
        and explainable recommendations from the ACIE research pipeline.
      </p>

      <div class="stats-grid">
        ${renderStatCard("API Status", health.status)}
        ${renderStatCard("Community Services", services.length)}
        ${renderStatCard("Reddit Posts", redditSummary.total_posts)}
        ${renderStatCard("Job Postings", jobSummary.total_jobs)}
        ${renderStatCard("Recommendations", recommendations.length)}
      </div>

      <article class="panel">
        <h3 class="panel__title">Top Recommendation</h3>
        ${
          topRecommendation
            ? renderRecommendationCard(topRecommendation)
            : renderStatusMessage("No recommendations are available yet.")
        }
      </article>

      <article class="panel">
        <h3 class="panel__title">Data Sources</h3>
        <p class="page-description">
          Reddit communities: ${redditSummary.communities.join(", ")}.
          Job sources: ${jobSummary.sources.join(", ")}.
        </p>
      </article>
    </section>
  `;
}
