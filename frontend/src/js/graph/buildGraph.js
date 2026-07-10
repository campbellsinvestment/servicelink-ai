function truncateLabel(value, maxLength = 28) {
  if (!value || value.length <= maxLength) {
    return value;
  }

  return `${value.slice(0, maxLength - 1)}…`;
}

function addNode(nodes, nodeIds, id, type, label) {
  if (nodeIds.has(id)) {
    return;
  }

  nodeIds.add(id);
  nodes.push({
    id,
    type,
    label: truncateLabel(label || id),
    fullLabel: label || id,
  });
}

function addEdge(edges, edgeKeys, source, target, type, score = null) {
  const key = `${source}|${target}|${type}`;

  if (edgeKeys.has(key)) {
    return;
  }

  edgeKeys.add(key);
  edges.push({
    source,
    target,
    type,
    score,
  });
}

export function buildGraphData({ posts, services, links }) {
  const postMap = Object.fromEntries(posts.map((post) => [post.post_id, post]));
  const serviceMap = Object.fromEntries(
    services.map((service) => [service.service_id, service]),
  );

  const nodes = [];
  const edges = [];
  const nodeIds = new Set();
  const edgeKeys = new Set();

  for (const link of links) {
    const post = postMap[link.post_id];
    const service = serviceMap[link.service_id];

    addNode(
      nodes,
      nodeIds,
      link.post_id,
      "post",
      post?.title || link.post_id,
    );
    addNode(
      nodes,
      nodeIds,
      link.service_id,
      "service",
      service?.service_name || link.service_id,
    );
    addEdge(edges, edgeKeys, link.post_id, link.service_id, "match", link.score);

    if (service?.organization) {
      const organizationId = `org:${service.organization}`;

      addNode(nodes, nodeIds, organizationId, "organization", service.organization);
      addEdge(edges, edgeKeys, link.service_id, organizationId, "provides");
    }
  }

  for (const post of posts) {
    if (!post.organizations?.length) {
      continue;
    }

    addNode(nodes, nodeIds, post.post_id, "post", post.title || post.post_id);

    for (const organization of post.organizations) {
      const organizationId = `org:${organization}`;

      addNode(nodes, nodeIds, organizationId, "organization", organization);
      addEdge(edges, edgeKeys, post.post_id, organizationId, "mentions");
    }
  }

  return { nodes, links: edges };
}
