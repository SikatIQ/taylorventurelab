const DEFAULT_FEED_ENDPOINT = "http://localhost:8000/feed";

async function getEndpoint() {
  return new Promise(resolve => {
    chrome.storage.sync.get(["tvl_feed_endpoint"], result =>
      resolve(result.tvl_feed_endpoint || DEFAULT_FEED_ENDPOINT)
    );
  });
}

async function fetchFeed() {
  const feedRoot = document.getElementById("feed-root");
  const errorEl = document.getElementById("error");
  const sourceLabel = document.getElementById("source-label");
  errorEl.textContent = "";

  try {
    const endpoint = await getEndpoint();
    sourceLabel.textContent = endpoint;

    const resp = await fetch(endpoint, { cache: "no-store" });
    const data = await resp.json();

    feedRoot.innerHTML = "";
    (data.items || []).forEach(item => {
      const el = document.createElement("div");
      el.className = "item";
      el.innerHTML = `
        <div class="item-title">${item.title}</div>
        <div class="item-meta">${item.source} • ${item.published_date}</div>
        <div class="item-summary">${item.summary}</div>
      `;
      feedRoot.appendChild(el);
    });
  } catch (err) {
    console.error("Feed load error:", err);
    errorEl.textContent = "Could not load feed. Check your agent.";
  }
}

document.getElementById("refresh-btn").addEventListener("click", fetchFeed);

fetchFeed();
