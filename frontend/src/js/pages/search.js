import {
  renderMatchScore,
  renderReasonTags,
  renderStatusMessage,
} from "../components.js";

const EXAMPLE_QUERIES = [
  "meal delivery in Stony Plain",
  "rides in Edmonton",
  "home care in Spruce Grove",
];

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderSearchResult(result) {
  return `
    <li class="match-row">
      <div class="match-row__main">
        <p class="match-row__service">
          ${escapeHtml(result.service_name)}
          <span class="match-row__provider">
            ${escapeHtml(result.organization)} · ${escapeHtml(result.city)}
          </span>
        </p>
        ${renderReasonTags(result.match_reasons)}
      </div>
      <div class="match-row__aside">
        ${renderMatchScore(result.score)}
      </div>
    </li>
  `;
}

function renderSearchOutput(response) {
  if (!response) {
    return `<div id="search-output"></div>`;
  }

  if (!response.results.length) {
    return `
      <div id="search-output">
        <p class="search-answer">${escapeHtml(response.answer)}</p>
      </div>
    `;
  }

  const rows = response.results.map(renderSearchResult).join("");

  return `
    <div id="search-output">
      <p class="search-answer">${escapeHtml(response.answer)}</p>
      <ul class="match-list">${rows}</ul>
    </div>
  `;
}

export function renderSearchPage() {
  const examples = EXAMPLE_QUERIES.map(
    (query) => `
      <button class="search-example" type="button" data-example="${escapeHtml(query)}">
        ${escapeHtml(query)}
      </button>
    `,
  ).join("");

  return `
    <section class="search-page">
      <form class="search-form" id="search-form">
        <div class="search-form__row">
          <input
            class="search-form__input"
            id="search-query"
            name="q"
            type="search"
            placeholder="Ask about a community service…"
            autocomplete="off"
            aria-label="Search question"
          />
          <button class="search-form__submit" type="submit">Search</button>
        </div>
      </form>
      <div class="search-examples" aria-label="Example questions">
        ${examples}
      </div>
      ${renderSearchOutput(null)}
    </section>
  `;
}

export function mountSearchPage(container, { search }) {
  const form = container.querySelector("#search-form");
  const input = container.querySelector("#search-query");

  if (!form || !input) {
    return;
  }

  async function runSearch(query) {
    const cleaned = query.trim();
    const output = container.querySelector("#search-output");

    if (!cleaned || !output) {
      return;
    }

    input.value = cleaned;
    output.innerHTML = renderStatusMessage("Searching...");

    try {
      const response = await search(cleaned);
      output.outerHTML = renderSearchOutput(response);
    } catch (error) {
      output.innerHTML = renderStatusMessage(
        "Search failed. Check that the API is running.",
        { isError: true },
      );
      console.error(error);
    }
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    runSearch(input.value);
  });

  container.querySelectorAll("[data-example]").forEach((button) => {
    button.addEventListener("click", () => {
      runSearch(button.getAttribute("data-example") || "");
    });
  });
}
