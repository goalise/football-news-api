# ⚽ Football News API

The **Football News API** provides real-time football news, transfer news, match previews, match predictions with multilingual coverage of major leagues and tournaments.  
Easily integrate fresh football content into your website, app, or sports project.

👉 **Official website:** [https://goalise.com](https://goalise.com/football-news-api)

---

## 🚀 Features

- 📰 **Latest football news** from trusted global sources  
- 🌍 **Multilingual support** (English, Spanish, Italian, and more)  
- ⚡ **Fast JSON API** with pagination and flexible endpoints  
- 🏟️ **League & team-based filtering**

---

## 🧩 Example Endpoints

```bash
GET /api/v2/news-by-date?date=2025-01-01
GET /api/v2/news-by-category?id=3
GET /api/v2/news-by-league?id=618
GET /api/v2/news-by-team?id=418
```

> The paths above are API v2. They keep working for existing integrations. New projects should use **API v3**, described below.

---

## ⚡ Quick Start (API v3)

1. Pick a plan at [goalise.com/checkout](https://goalise.com/checkout?product=basic&billing=monthly&utm_source=github&utm_medium=referral&utm_campaign=football-news-api). The Basic plan starts with a **7-day free trial**.
2. Copy your API token from the [dashboard](https://goalise.com/account).
3. Ask for the headlines of one day:

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  "https://api.goalise.com/api/v3/news-by-date?date=2026-09-12"
```

---

## 📚 API v3 Endpoints

Base URL `https://api.goalise.com/api/v3` · Auth `Authorization: Bearer YOUR_API_TOKEN` · JSON · 120 articles per page, newest first

| Endpoint | Example | Returns |
| --- | --- | --- |
| `GET /news-by-date` | `?date=2026-09-12` | Articles published on one day |
| `GET /news-by-league` | `?league_id=618` | Articles about one competition (618 is the Champions League) |
| `GET /news-by-team` | `?team_id=404` | Articles about one club (404 is Cagliari) |
| `GET /news-by-category` | `?category_id=3` | Articles of one section, for example Transfers |
| `GET /news-categories` | | The sections of the feed and their ids |
| `GET /news-content` | `?id=275071` | One article with its full HTML body |

Optional on every list: `page` (starts at 1), `timezone` (an IANA zone such as `Europe/Madrid` for `published_at`) and `expand=leagues,teams` for full league and team objects.

Do not know an id? `GET /search?query=arsenal&type=team` turns a name into the id.

---

## 🧾 What an Article Looks Like

Every answer uses the same envelope: `status`, `pagination`, `errors`, `meta`, `response`. One item of `response` (illustrative values):

```json
{
  "id": 275071,
  "title": "Cagliari agree a deal for a new striker",
  "image": "https://...",
  "alias": "2026-09-10-cagliari-agree-a-deal-for-a-new-striker",
  "original_url": "https://publisher.example/2026/09/10/cagliari-agree-a-deal-for-a-new-striker",
  "lang": "en",
  "timestamp": 1788606132,
  "timezone": "UTC",
  "published_at": "2026-09-10 15:17:12",
  "reading_time": null,
  "categories": [{ "id": 3, "name": "Transfers" }],
  "leagues": [{ "id": 646, "name": "Serie A", "logo": "https://...", "type": "League" }],
  "teams": [{ "id": 404, "name": "Cagliari", "logo": "https://..." }]
}
```

- Categories, leagues and teams arrive as objects with names and logos, so a news list is one request.
- `GET /news-content?id=...` adds `html_content` (the body, ready for a web view), `html_content_scripts` (script tags that embedded posts need) and fills in `reading_time` in minutes.
- `original_url` points to the article at its publisher.

---

## 🏆 Coverage

News is available for 37 competitions at the moment, including the Premier League, LaLiga, Serie A, Bundesliga, Ligue 1, Eredivisie, Liga Portugal, MLS, the Champions League, the Europa League and the World Cup 2026.

The live list needs no token: call `GET https://api.goalise.com/api/v3/country-coverage` and look at the `coverage.news` flag of each competition.

---

## 💻 Code Examples

Runnable scripts are in [`examples/`](examples): [Python](examples/python/news.py), [JavaScript](examples/javascript/news.mjs), [PHP](examples/php/news.php). They use only the standard library and read the token from the `GOALISE_TOKEN` environment variable.

```python
import json, os, urllib.request

request = urllib.request.Request(
    "https://api.goalise.com/api/v3/news-by-league?league_id=618",
    headers={"Authorization": "Bearer " + os.environ["GOALISE_TOKEN"]},
)
for article in json.load(urllib.request.urlopen(request))["response"]:
    print(article["published_at"], article["title"], article["original_url"])
```

---

## 🛠️ What You Can Build

- A news section for a football website, fan site or club blog
- Team and league news next to live scores in a mobile app
- Transfer news feeds and alerts
- Telegram and Discord bots that post the latest headlines
- Newsletters and digests by team or competition

---

## 🤖 AI-Rewritten News (On Request)

Need unique text for SEO? Goalise can deliver AI-rewritten versions of the articles on demand. It is an additional feature: [contact support](https://goalise.com/support) to enable it.

---

## 💳 Pricing

| Plan | Price | Requests per day |
| --- | --- | --- |
| Basic | $15/month, first 7 days free | 5,000 |
| Pro | $30/month | 50,000 |
| Premium | $50/month | 150,000 |

News is included in every plan together with live scores, fixtures, standings, statistics, odds and video highlights: one token, 46 endpoints. Annual billing is 30% cheaper. [See the plans](https://goalise.com/checkout?utm_source=github&utm_medium=referral&utm_campaign=football-news-api).

---

## ❓ FAQ

**Is there a free football news API?**
Goalise has no permanent free tier. The Basic plan starts with a 7-day free trial, then costs $15 per month. A card is required to start the trial and you can cancel at any time.

**Do I get the full text of the articles?**
Yes. The list endpoints return headlines with images and links, and `GET /news-content` returns the full article body as HTML.

**How do I get transfer news?**
Call `GET /news-categories`, take the id of the Transfers section and pass it to `GET /news-by-category`.

**Can I get the news of one team or one league?**
Yes: `GET /news-by-team?team_id=...` and `GET /news-by-league?league_id=...`.

**Is news a separate subscription?**
No. Every plan includes the news endpoints, and the same token works for the rest of the Goalise Football API.

**What happens when I reach the limit?**
The API answers `429` with the code `rate_limit.exceeded` and a `Retry-After` header. Every answer carries `X-Rate-Limit-Remaining`, and `GET /quota` shows your usage without spending a request.

---

## 🔗 Related

- [Football API](https://github.com/goalise/football-api) – live scores, fixtures, standings, lineups, statistics and odds
- [Football Highlights API](https://github.com/goalise/football-highlights-api) – official match highlights and goal clips with embed URLs
- [Football MCP Server](https://goalise.com/football-mcp-server?utm_source=github&utm_medium=referral&utm_campaign=football-news-api) – the same data for AI assistants
- [API reference](https://docs.goalise.com/v3/apireference/openapi#tag/news) and [getting started guide](https://docs.goalise.com/v3/get-started)

---

## 📄 License

The example code in this repository is released under the MIT License. Use of the API is subject to the [Goalise terms](https://goalise.com/terms).
