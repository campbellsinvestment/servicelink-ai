import { buildGraphData } from "../graph/buildGraph.js";
import { renderForceGraph } from "../graph/renderGraph.js";
import { renderStatusMessage } from "../components.js";

let destroyGraph = null;

export function renderGraphPage({ posts, services, links }) {
  const graphData = buildGraphData({ posts, services, links });

  if (!graphData.nodes.length) {
    return `
      <section>
        ${renderStatusMessage("No graph data in the current datasets.")}
      </section>
    `;
  }

  const matchCount = graphData.links.filter((link) => link.type === "match").length;

  return `
    <section class="graph-page">
      <p class="page-intro">
        ${graphData.nodes.length} entities and ${graphData.links.length} relationships
        (${matchCount} post-to-service matches).
      </p>
      <div class="graph-legend" aria-label="Graph legend">
        <span class="graph-legend__item">
          <span class="graph-legend__swatch graph-legend__swatch--post"></span>
          Post
        </span>
        <span class="graph-legend__item">
          <span class="graph-legend__swatch graph-legend__swatch--service"></span>
          Service
        </span>
        <span class="graph-legend__item">
          <span class="graph-legend__swatch graph-legend__swatch--organization"></span>
          Organization
        </span>
      </div>
      <div class="graph-panel" id="knowledge-graph"></div>
    </section>
  `;
}

export function mountGraphPage(container, { posts, services, links }) {
  if (destroyGraph) {
    destroyGraph();
    destroyGraph = null;
  }

  const graphRoot = container.querySelector("#knowledge-graph");

  if (!graphRoot) {
    return;
  }

  const graphData = buildGraphData({ posts, services, links });
  destroyGraph = renderForceGraph(graphRoot, graphData);
}
