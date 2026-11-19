"""Print football news headlines by date, league, team or category.

Usage:
    export GOALISE_TOKEN=your_api_token
    python news.py --date 2026-09-12
    python news.py --league 618        # 618 = Champions League
    python news.py --team 404          # 404 = Cagliari
    python news.py --category 3        # ids come from GET /news-categories

Needs Python 3.8+ and nothing else.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.goalise.com/api/v3"


def get(path, params):
    request = urllib.request.Request(
        "{}{}?{}".format(API, path, urllib.parse.urlencode(params)),
        headers={
            "Authorization": "Bearer " + os.environ.get("GOALISE_TOKEN", ""),
            "Accept": "application/json",
            "User-Agent": "goalise-examples/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        try:
            return json.load(error)  # errors use the same JSON envelope
        except ValueError:
            sys.exit("HTTP {} from the API".format(error.code))


def main():
    parser = argparse.ArgumentParser(description="Football news from the Goalise API")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--date", help="publication day, YYYY-MM-DD")
    group.add_argument("--league", type=int, help="league_id")
    group.add_argument("--team", type=int, help="team_id")
    group.add_argument("--category", type=int, help="category_id")
    parser.add_argument("--timezone", default="UTC", help="IANA zone for the dates, default UTC")
    args = parser.parse_args()

    if args.date:
        path, params = "/news-by-date", {"date": args.date}
    elif args.league:
        path, params = "/news-by-league", {"league_id": args.league}
    elif args.team:
        path, params = "/news-by-team", {"team_id": args.team}
    else:
        path, params = "/news-by-category", {"category_id": args.category}
    params["timezone"] = args.timezone

    data = get(path, params)
    if data["status"] != "success":
        sys.exit("API error: " + ", ".join(error["code"] for error in data["errors"]))

    for article in data["response"]:
        teams = ", ".join(team["name"] for team in article["teams"])
        print("{}  {}".format(article["published_at"], article["title"]))
        print("    {}{}".format(article["original_url"], "  [" + teams + "]" if teams else ""))

    page = data["pagination"]
    print("\npage {} of {}, {} articles in total".format(page["current_page"], page["page_count"], page["total_count"]))


if __name__ == "__main__":
    main()
