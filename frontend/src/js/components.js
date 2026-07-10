export function renderStatusMessage(message, { isError = false } = {}) {
  const className = isError
    ? "status-message status-message--error"
    : "status-message";

  return `<p class="${className}">${message}</p>`;
}

export function renderReasonList(reasons) {
  if (!reasons.length) {
    return "";
  }

  const items = reasons
    .map((reason) => `<li class="reason-list__item">${reason}</li>`)
    .join("");

  return `<ul class="reason-list" aria-label="Match reasons">${items}</ul>`;
}

export function renderStatCard(label, value) {
  return `
    <article class="stat-card">
      <p class="stat-card__label">${label}</p>
      <p class="stat-card__value">${value}</p>
    </article>
  `;
}

export function renderRecommendationCard(recommendation) {
  return `
    <article class="recommendation-card">
      <div class="recommendation-card__header">
        <h3 class="recommendation-card__title">
          #${recommendation.rank} ${recommendation.service_name}
        </h3>
        <p class="recommendation-card__score">Score ${recommendation.score}</p>
      </div>
      <p class="recommendation-card__meta">
        ${recommendation.organization} · ${recommendation.city} ·
        ${recommendation.category}
      </p>
      <p class="recommendation-card__meta">
        Linked to ${recommendation.post_title || recommendation.post_id}
      </p>
      ${renderReasonList(recommendation.match_reasons)}
    </article>
  `;
}
