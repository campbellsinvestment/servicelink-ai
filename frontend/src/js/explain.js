const KEYWORD_OVERLAP_SCORE = 3;

const SOURCE_TRUST_SCORES = {
  InformAlberta: 5,
  "Community Services": 2,
};

export function parseMatchReasons(reasons) {
  const tags = [];
  const hasCity = reasons.some((reason) => reason.startsWith("city:"));

  for (const reason of reasons) {
    if (reason.startsWith("category:")) {
      tags.push({
        type: "category",
        value: reason.slice("category:".length).replaceAll("_", " "),
      });
      continue;
    }

    if (reason.startsWith("city:")) {
      tags.push({
        type: "city",
        value: reason.slice("city:".length),
      });
      continue;
    }

    if (reason.startsWith("keywords:")) {
      for (const value of reason.slice("keywords:".length).split(",")) {
        tags.push({ type: "keyword", value });
      }
      continue;
    }

    if (reason.startsWith("source:")) {
      tags.push({
        type: "source",
        value: reason.slice("source:".length),
      });
      continue;
    }

    if (reason.startsWith("organization:")) {
      tags.push({
        type: "organization",
        value: reason.slice("organization:".length),
      });
    }
  }

  const breakdown = [];

  if (reasons.some((reason) => reason.startsWith("category:"))) {
    breakdown.push({
      label: "Category match",
      points: hasCity ? 10 : 5,
    });
  }

  if (hasCity) {
    breakdown.push({ label: "City match", points: 5 });
  }

  const keywordReason = reasons.find((reason) => reason.startsWith("keywords:"));

  if (keywordReason) {
    const keywordCount = keywordReason.slice("keywords:".length).split(",").length;
    breakdown.push({
      label: "Keyword overlap",
      points: keywordCount * KEYWORD_OVERLAP_SCORE,
    });
  }

  const sourceReason = reasons.find((reason) => reason.startsWith("source:"));

  if (sourceReason) {
    const source = sourceReason.slice("source:".length);
    breakdown.push({
      label: "Source trust",
      points: SOURCE_TRUST_SCORES[source] || 0,
    });
  }

  if (reasons.some((reason) => reason.startsWith("organization:"))) {
    breakdown.push({ label: "Organization mention", points: 8 });
  }

  return { tags, breakdown };
}

export function formatScoreSummary(breakdown, totalScore) {
  if (!breakdown.length) {
    return `Score ${totalScore}`;
  }

  const parts = breakdown.map((item) => `${item.label} +${item.points}`);

  return `Score ${totalScore} · ${parts.join(" · ")}`;
}
