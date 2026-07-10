import { parseMatchReasons } from "./explain.js";

export function renderStatusMessage(message, { isError = false } = {}) {
  const className = isError
    ? "status-message status-message--error"
    : "status-message";

  return `<p class="${className}">${message}</p>`;
}

export function renderReasonTags(reasons) {
  const tags = parseMatchReasons(reasons);

  if (!tags.length) {
    return "";
  }

  const items = tags
    .map(
      (tag) => `
        <li class="tag tag--${tag.type}" title="${tag.type}">
          ${tag.value}
        </li>
      `,
    )
    .join("");

  return `<ul class="tag-list" aria-label="Why this matched">${items}</ul>`;
}

export function renderStatItem(label, value) {
  return `
    <li class="stat-item">
      <span class="stat-item__label">${label}</span>
      <span class="stat-item__value">${value}</span>
    </li>
  `;
}

export function renderMatchScore(score) {
  return `
    <div class="match-score" aria-label="Match score ${score}">
      <span class="match-score__label">Score</span>
      <span class="match-score__value">${score}</span>
    </div>
  `;
}

export function renderFeaturedMatch(recommendation) {
  return `
    <article class="featured-match">
      <p class="featured-match__lead">
        A Reddit post about
        <strong>${recommendation.post_title || recommendation.post_id}</strong>
        matched
        <strong>${recommendation.service_name}</strong>
        from ${recommendation.organization} in ${recommendation.city}.
      </p>
      <div class="featured-match__footer">
        ${renderMatchScore(recommendation.score)}
        ${renderReasonTags(recommendation.match_reasons)}
      </div>
    </article>
  `;
}

export function renderRecommendationRow(recommendation) {
  return `
    <li class="match-row">
      <div class="match-row__main">
        <p class="match-row__post">
          ${recommendation.post_title || recommendation.post_id}
        </p>
        <p class="match-row__service">
          ${recommendation.service_name}
          <span class="match-row__provider">${recommendation.organization}</span>
        </p>
      </div>
      <div class="match-row__aside">
        ${renderMatchScore(recommendation.score)}
        ${renderReasonTags(recommendation.match_reasons)}
      </div>
    </li>
  `;
}
