import * as d3 from "d3";

const TYPE_LABELS = {
  post: "Post",
  job: "Job",
  service: "Service",
  organization: "Organization",
};

const NODE_STYLES = {
  post: {
    fill: "#eef6fb",
    stroke: "#7eb8d4",
    text: "#334155",
  },
  job: {
    fill: "#edf7f0",
    stroke: "#7db899",
    text: "#2f4f3a",
  },
  service: {
    fill: "#005072",
    stroke: "#003f5c",
    text: "#ffffff",
  },
  organization: {
    fill: "#faf6ef",
    stroke: "#c9a66b",
    text: "#5c4a32",
  },
};

const LINK_STYLES = {
  match: {
    color: "#005072",
    width: 2,
    dash: null,
    label: "Post match",
  },
  "job-match": {
    color: "#2f7a4b",
    width: 2,
    dash: null,
    label: "Job match",
  },
  provides: {
    color: "#b8b8b8",
    width: 1,
    dash: "4 3",
    label: "Provided by",
  },
  mentions: {
    color: "#c9a66b",
    width: 1,
    dash: "4 3",
    label: "Mentions",
  },
};

const COLUMN_ORDER = ["post", "job", "service", "organization"];

function isScoredMatch(type) {
  return type === "match" || type === "job-match";
}

function resolveLinks(nodes, links) {
  const nodesById = new Map(nodes.map((node) => [node.id, node]));

  return links
    .map((link) => ({
      ...link,
      source: nodesById.get(link.source),
      target: nodesById.get(link.target),
    }))
    .filter((link) => link.source && link.target);
}

function layoutNodes(nodes, width, height) {
  const top = 56;
  const bottom = 28;
  const columnX = {
    post: width * 0.11,
    job: width * 0.34,
    service: width * 0.61,
    organization: width * 0.88,
  };

  for (const type of COLUMN_ORDER) {
    const group = nodes.filter((node) => node.type === type);
    const step = (height - top - bottom) / Math.max(group.length + 1, 2);

    group.forEach((node, index) => {
      node.x = columnX[type];
      node.y = top + step * (index + 1);
    });
  }
}

function measureNode(node) {
  const nameLength = node.label.length;
  const width = Math.min(Math.max(nameLength * 6.4 + 28, 112), 168);
  const height = 44;

  return { width, height };
}

function linkPath(link) {
  const sourceX = link.source.x + measureNode(link.source).width / 2;
  const targetX = link.target.x - measureNode(link.target).width / 2;
  const sourceY = link.source.y;
  const targetY = link.target.y;
  const midX = (sourceX + targetX) / 2;

  return `M${sourceX},${sourceY} C${midX},${sourceY} ${midX},${targetY} ${targetX},${targetY}`;
}

function getConnectedIds(nodeId, links) {
  const connected = new Set([nodeId]);

  for (const link of links) {
    if (link.source.id === nodeId) {
      connected.add(link.target.id);
    }

    if (link.target.id === nodeId) {
      connected.add(link.source.id);
    }
  }

  return connected;
}

function describeNode(node, links) {
  const matches = links.filter(
    (link) => link.type === "match" && link.source.id === node.id,
  );
  const jobMatches = links.filter(
    (link) => link.type === "job-match" && link.source.id === node.id,
  );
  const matchedBy = links.filter(
    (link) => link.type === "match" && link.target.id === node.id,
  );
  const matchedByJobs = links.filter(
    (link) => link.type === "job-match" && link.target.id === node.id,
  );
  const provides = links.filter(
    (link) => link.type === "provides" && link.source.id === node.id,
  );
  const providedBy = links.filter(
    (link) => link.type === "provides" && link.target.id === node.id,
  );
  const mentions = links.filter(
    (link) => link.type === "mentions" && link.source.id === node.id,
  );
  const mentionedBy = links.filter(
    (link) => link.type === "mentions" && link.target.id === node.id,
  );

  if (node.type === "post") {
    if (!matches.length && !mentions.length) {
      return `${node.fullLabel} has no linked services yet.`;
    }

    const matchText = matches
      .map((link) => `${link.target.fullLabel} (${link.score})`)
      .join(", ");

    const mentionText = mentions
      .map((link) => link.target.fullLabel)
      .join(", ");

    const parts = [];

    if (matchText) {
      parts.push(`Matched services: ${matchText}`);
    }

    if (mentionText) {
      parts.push(`Mentioned organizations: ${mentionText}`);
    }

    return parts.join(" · ");
  }

  if (node.type === "job") {
    if (!jobMatches.length) {
      return `${node.fullLabel} has no linked services yet.`;
    }

    const matchText = jobMatches
      .map((link) => `${link.target.fullLabel} (${link.score})`)
      .join(", ");

    return `Matched services: ${matchText}`;
  }

  if (node.type === "service") {
    const parts = [];

    if (matchedBy.length) {
      parts.push(
        `Matched by ${matchedBy.length} post${matchedBy.length === 1 ? "" : "s"}`,
      );
    }

    if (matchedByJobs.length) {
      parts.push(
        `Matched by ${matchedByJobs.length} job${matchedByJobs.length === 1 ? "" : "s"}`,
      );
    }

    if (providedBy.length) {
      parts.push(`Provided by ${providedBy[0].source.fullLabel}`);
    }

    return parts.join(" · ") || node.fullLabel;
  }

  const parts = [];

  if (provides.length) {
    parts.push(
      `Provides ${provides.length} service${provides.length === 1 ? "" : "s"}`,
    );
  }

  if (mentionedBy.length) {
    parts.push(
      `Mentioned in ${mentionedBy.length} post${mentionedBy.length === 1 ? "" : "s"}`,
    );
  }

  return parts.join(" · ") || node.fullLabel;
}

export function renderForceGraph(container, graphData, detailPanel) {
  container.replaceChildren();

  const width = container.clientWidth || 960;
  const height = 560;
  const nodes = graphData.nodes.map((node) => ({ ...node }));
  const links = resolveLinks(nodes, graphData.links);

  layoutNodes(nodes, width, height);

  const svg = d3
    .select(container)
    .append("svg")
    .attr("viewBox", [0, 0, width, height])
    .attr("role", "img")
    .attr("aria-label", "Knowledge graph of posts, jobs, services, and organizations");

  svg
    .append("defs")
    .append("marker")
    .attr("id", "graph-arrow")
    .attr("viewBox", "0 -4 8 8")
    .attr("refX", 7)
    .attr("refY", 0)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,-4L8,0L0,4")
    .attr("fill", "#005072");

  svg
    .select("defs")
    .append("marker")
    .attr("id", "graph-arrow-job")
    .attr("viewBox", "0 -4 8 8")
    .attr("refX", 7)
    .attr("refY", 0)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,-4L8,0L0,4")
    .attr("fill", "#2f7a4b");

  const columnTitles = [
    { label: "Reddit posts", x: width * 0.11 },
    { label: "Job postings", x: width * 0.34 },
    { label: "Community services", x: width * 0.61 },
    { label: "Organizations", x: width * 0.88 },
  ];

  svg
    .append("g")
    .attr("class", "graph-columns")
    .selectAll("text")
    .data(columnTitles)
    .join("text")
    .attr("class", "graph-column-title")
    .attr("x", (datum) => datum.x)
    .attr("y", 24)
    .attr("text-anchor", "middle")
    .text((datum) => datum.label);

  const linkGroup = svg.append("g").attr("class", "graph-links");
  const nodeGroup = svg.append("g").attr("class", "graph-nodes");

  const link = linkGroup
    .selectAll("path")
    .data(links)
    .join("path")
    .attr("class", (datum) => `graph-link graph-link--${datum.type}`)
    .attr("fill", "none")
    .attr("stroke", (datum) => LINK_STYLES[datum.type].color)
    .attr("stroke-width", (datum) => LINK_STYLES[datum.type].width)
    .attr("stroke-dasharray", (datum) => LINK_STYLES[datum.type].dash || null)
    .attr("stroke-opacity", 0.85)
    .attr("marker-end", (datum) => {
      if (datum.type === "match") {
        return "url(#graph-arrow)";
      }

      if (datum.type === "job-match") {
        return "url(#graph-arrow-job)";
      }

      return null;
    })
    .attr("d", linkPath);

  link.append("title").text((datum) => {
    const style = LINK_STYLES[datum.type];

    if (isScoredMatch(datum.type)) {
      return `${style.label}: score ${datum.score}`;
    }

    return style.label;
  });

  const node = nodeGroup
    .selectAll("g")
    .data(nodes)
    .join("g")
    .attr("class", (datum) => `graph-node graph-node--${datum.type}`)
    .attr("transform", (datum) => `translate(${datum.x},${datum.y})`);

  node.each(function appendNode(datum) {
    const group = d3.select(this);
    const size = measureNode(datum);
    const styles = NODE_STYLES[datum.type];

    group
      .append("rect")
      .attr("class", "graph-node__box")
      .attr("x", -size.width / 2)
      .attr("y", -size.height / 2)
      .attr("width", size.width)
      .attr("height", size.height)
      .attr("rx", 8)
      .attr("fill", styles.fill)
      .attr("stroke", styles.stroke);

    group
      .append("text")
      .attr("class", "graph-node__type")
      .attr("text-anchor", "middle")
      .attr("y", -4)
      .attr("fill", styles.text)
      .text(TYPE_LABELS[datum.type]);

    group
      .append("text")
      .attr("class", "graph-node__label")
      .attr("text-anchor", "middle")
      .attr("y", 14)
      .attr("fill", styles.text)
      .text(datum.label);
  });

  function setFocus(nodeId = null) {
    const connected = nodeId ? getConnectedIds(nodeId, links) : null;

    node.classed("is-dimmed", (datum) => connected && !connected.has(datum.id));
    link.classed("is-dimmed", (datum) => {
      if (!connected) {
        return false;
      }

      return !connected.has(datum.source.id) || !connected.has(datum.target.id);
    });

    if (detailPanel) {
      if (!nodeId) {
        detailPanel.textContent =
          "Hover a node to see how it connects across the graph.";
        return;
      }

      const activeNode = nodes.find((datum) => datum.id === nodeId);

      if (activeNode) {
        detailPanel.textContent = describeNode(activeNode, links);
      }
    }
  }

  node
    .on("mouseenter", (_, datum) => setFocus(datum.id))
    .on("mouseleave", () => setFocus(null))
    .on("focus", (_, datum) => setFocus(datum.id))
    .on("blur", () => setFocus(null));

  node.attr("tabindex", 0).attr("role", "button");

  setFocus(null);

  return () => {
    node.on("mouseenter mouseleave focus blur", null);
  };
}
