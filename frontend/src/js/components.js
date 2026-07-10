import { parseMatchReasons, renderMatchingSummary } from "./explain.js";

export function renderStatusMessage(message, { isError = false } = {}) {
  const className = isError
    ? "status-message status-message--error"
    : "status-message";

  return `<p class="${className}">${message}</p>`;
}

export function renderReasonTags(reasons) {
  const { tags } = parseMatchReasons(reasons);

  if (!tags.length) {
    return "";
  }

  const items = tags
    .map(
      (tag) => `
        <li class="tag tag--${tag.type}">
          <span class="tag__label">${tag.label}</span>
          <span class="tag__value">${tag.value}</span>
        </li>
      `,
    )
    .join("");

  return `
    <div class="tag-group">
      <p class="tag-group__label">Match signals</p>
      <ul class="tag-list" aria-label="Match signals">${items}</ul>
    </div>
  `;
}

export function renderScoreBreakdown(recommendation) {
  const { breakdown } = parseMatchReasons(recommendation.match_reasons);

  if (!breakdown.length) {
    return "";
  }

  const rows = breakdown
    .map(
      (item) => `
        <li class="breakdown-row">
          <div class="breakdown-row__copy">
            <span class="breakdown-row__label">${item.label}</span>
            ${item.detail ? `<span class="breakdown-row__detail">${item.detail}</span>` : ""}
          </div>
          <span class="breakdown-row__points">+${item.points}</span>
        </li>
      `,
    )
    .join("");

  return `
    <div class="breakdown">
      <p class="breakdown__label">How this score was calculated</p>
      <ol class="breakdown-list">${rows}</ol>
      <div class="breakdown-total">
        <span>Total score</span>
        <strong>${recommendation.score}</strong>
      </div>
    </div>
  `;
}

export function renderStatItem(label, value) {
  return `
    <li class="stat-item">
      <span class="stat-item__label">${label}</span>
      <span class="stat-item__value">${value}</span>
    </li>
  `;
}

export function renderRecommendationItem(recommendation, { showSummary = false } = {}) {
  return `
    <li class="recommendation-item">
      <div class="recommendation-item__row">
        <h3 class="recommendation-item__title">
          ${recommendation.service_name}
        </h3>
        <p class="recommendation-item__score">Score ${recommendation.score}</p>
      </div>

      <div class="match-context">
        <div class="match-context__block">
          <p class="match-context__label">Reddit post</p>
          <p class="match-context__value">
            ${recommendation.post_title || recommendation.post_id}
          </p>
        </div>
        <div class="match-context__block">
          <p class="match-context__label">Matched service</p>
          <p class="match-context__value">
            ${recommendation.organization} · ${recommendation.city} ·
            ${recommendation.category.replaceAll("_", " ")}
          </p>
        </div>
      </div>

      ${showSummary ? renderMatchingSummary() : ""}
      ${renderScoreBreakdown(recommendation)}
      ${renderReasonTags(recommendation.match_reasons)}
    </li>
  `;
}

export { renderMatchingSummary };
