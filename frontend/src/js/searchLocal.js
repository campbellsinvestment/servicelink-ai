const CATEGORY_ALIASES = {
  transportation: [
    "transportation",
    "senior transport",
    "transport",
    "transportation help",
    "rides",
    "ride",
    "medical appointments",
  ],
  food_support: [
    "food support",
    "meal assistance",
    "meal delivery",
    "meals on wheels",
    "deliver meals",
    "meal",
    "meals",
    "food",
  ],
  home_care: [
    "home care",
    "in-home care",
    "in home care",
    "home care assistance",
    "in-home assistance",
    "home care assistant",
    "community support worker",
    "daily living",
    "caregiver",
    "in home support",
    "in-home support",
  ],
};

const LOCATIONS = ["Edmonton", "Stony Plain", "Spruce Grove"];

const SOURCE_TRUST = {
  InformAlberta: 5,
  "Community Services": 2,
};

const STOP_WORDS = new Set([
  "about",
  "after",
  "also",
  "any",
  "are",
  "can",
  "for",
  "from",
  "has",
  "have",
  "help",
  "her",
  "his",
  "how",
  "into",
  "its",
  "just",
  "like",
  "living",
  "need",
  "needs",
  "old",
  "one",
  "our",
  "out",
  "she",
  "that",
  "the",
  "their",
  "them",
  "there",
  "these",
  "they",
  "this",
  "through",
  "very",
  "was",
  "were",
  "what",
  "when",
  "where",
  "which",
  "with",
  "would",
  "your",
]);

function tokenize(text) {
  return new Set(
    (text.toLowerCase().match(/[a-z0-9]+/g) || []).filter(
      (token) => token.length > 3 && !STOP_WORDS.has(token),
    ),
  );
}

function extractCategories(text) {
  const normalized = text.toLowerCase();
  const categories = [];

  for (const [category, aliases] of Object.entries(CATEGORY_ALIASES)) {
    const sorted = [...aliases].sort((a, b) => b.length - a.length);

    if (sorted.some((alias) => normalized.includes(alias))) {
      categories.push(category);
    }
  }

  return categories;
}

function extractLocations(text) {
  const normalized = text.toLowerCase();

  return LOCATIONS.filter((city) => normalized.includes(city.toLowerCase()));
}

function interpretQuery(query) {
  const cleaned = query.trim();
  const categories = extractCategories(cleaned);
  const locations = extractLocations(cleaned);
  const parts = [];

  if (categories.length) {
    parts.push(
      `looking for ${categories.map((category) => category.replaceAll("_", " ")).join(", ")}`,
    );
  }

  if (locations.length) {
    parts.push(`in ${locations.join(", ")}`);
  }

  let summary = "No clear service category or location detected.";

  if (parts.length) {
    const joined = parts.join(" ");
    summary = `${joined[0].toUpperCase()}${joined.slice(1)}.`;
  }

  return {
    query: cleaned,
    categories,
    locations,
    keywords: [],
    summary,
  };
}

function scoreService(interpretation, service) {
  if (
    interpretation.categories.length &&
    !interpretation.categories.includes(service.category)
  ) {
    return null;
  }

  let score = 0;
  const matchReasons = [];

  if (interpretation.categories.length) {
    if (interpretation.locations.length) {
      score += 10;
      matchReasons.push(`category:${service.category}`);

      if (interpretation.locations.includes(service.city)) {
        score += 5;
        matchReasons.push(`city:${service.city}`);
      } else {
        return null;
      }
    } else {
      score += 5;
      matchReasons.push(`category:${service.category}`);
    }
  } else if (interpretation.locations.length) {
    if (!interpretation.locations.includes(service.city)) {
      return null;
    }

    score += 5;
    matchReasons.push(`city:${service.city}`);
  }

  const queryTokens = tokenize(interpretation.query);
  const serviceText = `${service.service_name || ""} ${service.description || ""}`;
  const serviceTokens = tokenize(serviceText);
  const shared = [...queryTokens].filter((token) => serviceTokens.has(token)).sort();

  if (shared.length) {
    score += shared.length * 3;
    matchReasons.push(`keywords:${shared.join(",")}`);
  }

  if (!matchReasons.length) {
    return null;
  }

  const sourceScore = SOURCE_TRUST[service.source] || 0;

  if (sourceScore) {
    score += sourceScore;
    matchReasons.push(`source:${service.source}`);
  }

  return { score, matchReasons };
}

function buildAnswer(interpretation, results) {
  if (!results.length) {
    if (interpretation.categories.length || interpretation.locations.length) {
      return (
        "I could not find a matching community service for that request " +
        "in the current demo datasets."
      );
    }

    return (
      "Try asking about transportation, meal delivery, or home care " +
      "in Edmonton, Stony Plain, or Spruce Grove."
    );
  }

  const top = results[0];

  if (results.length === 1) {
    return (
      `I found ${top.service_name} from ${top.organization} ` +
      `in ${top.city} (${top.category.replaceAll("_", " ")}).`
    );
  }

  return (
    `I found ${results.length} matching services. ` +
    `The strongest match is ${top.service_name} from ${top.organization} ` +
    `in ${top.city}.`
  );
}

export function searchServicesLocal(query, services, limit = 5) {
  const interpretation = interpretQuery(query);
  const scored = [];

  for (const service of services) {
    const result = scoreService(interpretation, service);

    if (!result) {
      continue;
    }

    scored.push({ service, ...result });
  }

  scored.sort((a, b) => b.score - a.score || a.service.service_id.localeCompare(b.service.service_id));

  const results = scored.slice(0, limit).map((item, index) => ({
    rank: index + 1,
    service_id: item.service.service_id,
    service_name: item.service.service_name,
    organization: item.service.organization,
    city: item.service.city,
    category: item.service.category,
    score: item.score,
    match_reasons: item.matchReasons,
  }));

  return {
    interpretation,
    results,
    answer: buildAnswer(interpretation, results),
  };
}
