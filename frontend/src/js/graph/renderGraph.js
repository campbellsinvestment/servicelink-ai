import * as d3 from "d3";

const NODE_RADIUS = {
  post: 10,
  service: 12,
  organization: 9,
};

const NODE_COLORS = {
  post: "#d6e8f3",
  service: "#005072",
  organization: "#faf6ef",
};

const NODE_STROKES = {
  post: "#7eb8d4",
  service: "#003f5c",
  organization: "#c9a66b",
};

const LINK_COLORS = {
  match: "#005072",
  provides: "#999999",
  mentions: "#c9a66b",
};

function drag(simulation) {
  function dragStarted(event) {
    if (!event.active) {
      simulation.alphaTarget(0.3).restart();
    }

    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  function dragEnded(event) {
    if (!event.active) {
      simulation.alphaTarget(0);
    }

    event.subject.fx = null;
    event.subject.fy = null;
  }

  return d3
    .drag()
    .on("start", dragStarted)
    .on("drag", dragged)
    .on("end", dragEnded);
}

export function renderForceGraph(container, graphData) {
  container.replaceChildren();

  const width = container.clientWidth || 860;
  const height = 480;

  const svg = d3
    .select(container)
    .append("svg")
    .attr("viewBox", [0, 0, width, height])
    .attr("role", "img")
    .attr("aria-label", "Knowledge graph of posts, services, and organizations");

  const simulation = d3
    .forceSimulation(graphData.nodes)
    .force(
      "link",
      d3
        .forceLink(graphData.links)
        .id((node) => node.id)
        .distance((link) => (link.type === "match" ? 120 : 70)),
    )
    .force("charge", d3.forceManyBody().strength(-280))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(24));

  const linkGroup = svg.append("g").attr("class", "graph-links");
  const nodeGroup = svg.append("g").attr("class", "graph-nodes");

  const link = linkGroup
    .selectAll("line")
    .data(graphData.links)
    .join("line")
    .attr("class", (datum) => `graph-link graph-link--${datum.type}`)
    .attr("stroke", (datum) => LINK_COLORS[datum.type])
    .attr("stroke-width", (datum) => (datum.type === "match" ? 2 : 1))
    .attr("stroke-opacity", (datum) => (datum.type === "match" ? 0.75 : 0.55));

  const node = nodeGroup
    .selectAll("g")
    .data(graphData.nodes)
    .join("g")
    .attr("class", (datum) => `graph-node graph-node--${datum.type}`)
    .call(drag(simulation));

  node
    .append("circle")
    .attr("r", (datum) => NODE_RADIUS[datum.type])
    .attr("fill", (datum) => NODE_COLORS[datum.type])
    .attr("stroke", (datum) => NODE_STROKES[datum.type])
    .attr("stroke-width", 1.5);

  node
    .append("text")
    .attr("x", (datum) => NODE_RADIUS[datum.type] + 6)
    .attr("y", 4)
    .text((datum) => datum.label)
    .attr("class", "graph-node__label");

  node.append("title").text((datum) => datum.fullLabel);

  simulation.on("tick", () => {
    link
      .attr("x1", (datum) => datum.source.x)
      .attr("y1", (datum) => datum.source.y)
      .attr("x2", (datum) => datum.target.x)
      .attr("y2", (datum) => datum.target.y);

    node.attr("transform", (datum) => `translate(${datum.x},${datum.y})`);
  });

  return () => {
    simulation.stop();
  };
}
