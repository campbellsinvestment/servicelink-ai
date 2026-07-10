export function parseMatchReasons(reasons) {
  const tags = [];

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

  return tags;
}
