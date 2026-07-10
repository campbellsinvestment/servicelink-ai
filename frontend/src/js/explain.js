const KEYWORD_OVERLAP_SCORE = 3;

const SOURCE_TRUST_SCORES = {
  InformAlberta: 5,
  "Community Services": 2,
};

const REASON_TYPE_LABELS = {
  category: "Category",
  city: "Location",
  keyword: "Keyword",
  source: "Source",
  organization: "Organization",
};

export function parseMatchReasons(reasons) {
  const tags = [];
  const hasCity = reasons.some((reason) => reason.startsWith("city:"));

  for (const reason of reasons) {
    if (reason.startsWith("category:")) {
      const value = reason.slice("category:".length).replaceAll("_", " ");

      tags.push({
        type: "category",
        label: REASON_TYPE_LABELS.category,
        value,
      });
      continue;
    }

    if (reason.startsWith("city:")) {
      tags.push({
        type: "city",
        label: REASON_TYPE_LABELS.city,
        value: reason.slice("city:".length),
      });
      continue;
    }

    if (reason.startsWith("keywords:")) {
      const values = reason.slice("keywords:".length).split(",");

      for (const value of values) {
        tags.push({
          type: "keyword",
          label: REASON_TYPE_LABELS.keyword,
          value,
        });
      }
      continue;
    }

    if (reason.startsWith("source:")) {
      tags.push({
        type: "source",
        label: REASON_TYPE_LABELS.source,
        value: reason.slice("source:".length),
      });
      continue;
    }

    if (reason.startsWith("organization:")) {
      tags.push({
        type: "organization",
        label: REASON_TYPE_LABELS.organization,
        value: reason.slice("organization:".length),
      });
    }
  }

  const breakdown = [];

  if (reasons.some((reason) => reason.startsWith("category:"))) {
    breakdown.push({
      label: "Service category matched post topic",
      points: hasCity ? 10 : 5,
    });
  }

  if (hasCity) {
    const city = reasons
      .find((reason) => reason.startsWith("city:"))
      ?.slice("city:".length);

    breakdown.push({
      label: "Same Alberta city in post and service record",
      detail: city,
      points: 5,
    });
  }

  const keywordReason = reasons.find((reason) => reason.startsWith("keywords:"));

  if (keywordReason) {
    const keywordCount = keywordReason.slice("keywords:".length).split(",").length;

    breakdown.push({
      label: "Shared terms in post body and service description",
      detail: `${keywordCount} keyword${keywordCount === 1 ? "" : "s"}`,
      points: keywordCount * KEYWORD_OVERLAP_SCORE,
    });
  }

  const sourceReason = reasons.find((reason) => reason.startsWith("source:"));

  if (sourceReason) {
    const source = sourceReason.slice("source:".length);

    breakdown.push({
      label: "Trusted source registry weighting",
      detail: source,
      points: SOURCE_TRUST_SCORES[source] || 0,
    });
  }

  const organizationReason = reasons.find((reason) =>
    reason.startsWith("organization:"),
  );

  if (organizationReason) {
    breakdown.push({
      label: "Organization explicitly mentioned in post",
      detail: organizationReason.slice("organization:".length),
      points: 8,
    });
  }

  return { tags, breakdown };
}

export function renderMatchingSummary() {
  return `
    <p class="match-summary">
      Matches are produced by enriching Reddit posts with categories, locations,
      and organization names, then scoring aligned community services using
      deterministic rules in the ACIE backend.
    </p>
  `;
}
