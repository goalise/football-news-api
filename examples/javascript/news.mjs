// Latest transfer news: find the Transfers section, then read its newest articles.
//
// Usage:
//   export GOALISE_TOKEN=your_api_token
//   node news.mjs              # Transfers
//   node news.mjs injuries     # any other section name
//
// Needs Node.js 18+ and nothing else.

const API = "https://api.goalise.com/api/v3";
const wanted = (process.argv[2] ?? "transfers").toLowerCase();

async function get(path, params = {}) {
  const url = new URL(API + path);
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${process.env.GOALISE_TOKEN ?? ""}`,
      Accept: "application/json",
    },
  });
  const data = await response.json();
  if (data.status !== "success") {
    console.error("API error:", data.errors.map((error) => error.code).join(", "));
    process.exit(1);
  }
  return data;
}

const categories = (await get("/news-categories")).response;
const category = categories.find((item) => (item.name ?? "").toLowerCase().includes(wanted));
if (!category) {
  console.error(`No section named "${wanted}". Available: ${categories.map((item) => item.name).join(", ")}`);
  process.exit(1);
}

const news = await get("/news-by-category", { category_id: category.id });
console.log(`${category.name}: ${news.pagination.total_count} articles, newest first\n`);
for (const article of news.response.slice(0, 20)) {
  const teams = article.teams.map((team) => team.name).join(", ");
  console.log(`${article.published_at}  ${article.title}${teams ? `  [${teams}]` : ""}`);
  console.log(`    ${article.original_url}`);
}
