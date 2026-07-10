import {
  renderMatchScore,
  renderReasonTags,
  renderStatusMessage,
} from "../components.js";

const EXAMPLE_QUERIES = [
  "I need rides to medical appointments in Edmonton",
  "Where can I get meal delivery in Stony Plain?",
  "Home care support in Spruce Grove",
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
      </div>
      <div class="match-row__aside">
        ${renderMatchScore(result.score)}
        ${renderReasonTags(result.match_reasons)}
      </div>
    </li>
  `;
}

function renderSearchOutput(response) {
  if (!response) {
    return `
      <div id="search-output">
        <p class="page-intro">
          Ask in plain language. The engine extracts category and city cues,
          then ranks matching community services.
        </p>
      </div>
    `;
  }

  const rows = response.results.map(renderSearchResult).join("");

  return `
    <div id="search-output">
      <p class="search-answer">${escapeHtml(response.answer)}</p>
      <p class="search-interpretation">${escapeHtml(response.interpretation.summary)}</p>
      ${
        response.results.length
          ? `<ul class="match-list">${rows}</ul>`
          : renderStatusMessage("No matching services found.")
      }
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
      <p class="page-intro">
        Conversational search over community services using lexical intent
        extraction — no LLM required for this prototype.
      </p>
      <form class="search-form" id="search-form">
        <label class="search-form__label" for="search-query">Your question</label>
        <div class="search-form__row">
          <input
            class="search-form__input"
            id="search-query"
            name="q"
            type="search"
            placeholder="e.g. meal delivery in Stony Plain"
            autocomplete="off"
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
