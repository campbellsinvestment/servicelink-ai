export function renderStatusMessage(message, { isError = false } = {}) {
  const className = isError
    ? "status-message status-message--error"
    : "status-message";

  return `<p class="${className}">${message}</p>`;
}

export function renderReasonText(reasons) {
  if (!reasons.length) {
    return "";
  }

  return `<p class="reason-text">${reasons.join(" · ")}</p>`;
}

export function renderStatItem(label, value) {
  return `
    <li class="stat-item">
      <span class="stat-item__label">${label}</span>
      <span class="stat-item__value">${value}</span>
    </li>
  `;
}

export function renderRecommendationItem(recommendation) {
  return `
    <li class="recommendation-item">
      <div class="recommendation-item__row">
        <h3 class="recommendation-item__title">
          ${recommendation.service_name}
        </h3>
        <p class="recommendation-item__score">${recommendation.score}</p>
      </div>
      <p class="recommendation-item__meta">
        ${recommendation.organization} · ${recommendation.city}
      </p>
      <p class="recommendation-item__meta">
        ${recommendation.post_title || recommendation.post_id}
      </p>
      ${renderReasonText(recommendation.match_reasons)}
    </li>
  `;
}
