import { buildGraphData } from "../graph/buildGraph.js";
import { renderForceGraph } from "../graph/renderGraph.js";
import { renderStatusMessage } from "../components.js";

let destroyGraph = null;

export function renderGraphPage({ posts, jobs, services, links, jobLinks }) {
  const graphData = buildGraphData({ posts, jobs, services, links, jobLinks });

  if (!graphData.nodes.length) {
    return `
      <section>
        ${renderStatusMessage("No graph data in the current datasets.")}
      </section>
    `;
  }

  const matchCount = graphData.links.filter((link) => link.type === "match").length;
  const jobMatchCount = graphData.links.filter(
    (link) => link.type === "job-match",
  ).length;

  return `
    <section class="graph-page">
      <p class="page-intro">
        Read left to right: Reddit posts and job postings link to community
        services, which are provided by organizations.
        ${matchCount} post matches and ${jobMatchCount} job matches in the demo.
      </p>
      <div class="graph-legend" aria-label="Graph legend">
        <span class="graph-legend__item">
          <span class="graph-legend__line graph-legend__line--match"></span>
          Post match
        </span>
        <span class="graph-legend__item">
          <span class="graph-legend__line graph-legend__line--job-match"></span>
          Job match
        </span>
        <span class="graph-legend__item">
          <span class="graph-legend__line graph-legend__line--provides"></span>
          Provided by
        </span>
        <span class="graph-legend__item">
          <span class="graph-legend__line graph-legend__line--mentions"></span>
          Mentions
        </span>
      </div>
      <div class="graph-panel" id="knowledge-graph"></div>
      <p class="graph-detail" id="graph-detail">
        Hover a node to see how it connects across the graph.
      </p>
    </section>
  `;
}

export function mountGraphPage(
  container,
  { posts, jobs, services, links, jobLinks },
) {
  if (destroyGraph) {
    destroyGraph();
    destroyGraph = null;
  }

  const graphRoot = container.querySelector("#knowledge-graph");
  const detailPanel = container.querySelector("#graph-detail");

  if (!graphRoot) {
    return;
  }

  const graphData = buildGraphData({ posts, jobs, services, links, jobLinks });
  destroyGraph = renderForceGraph(graphRoot, graphData, detailPanel);
}
