"""
Web Scraper for Job Listings & Hacker News
Scrapes from multiple sites to learn how different HTML structures work.
Each site has its own scraping function — this teaches you that
every website's HTML is different, so you need to inspect and adapt.
"""

import re  # Regular expressions — for extracting numbers from text like "4 hours ago"
import requests  # Library to make HTTP requests (like a browser visiting a page)
from bs4 import BeautifulSoup  # Library to parse and search through HTML


# ============================================================
# SCRAPER 1: Fake Jobs (realpython.github.io/fake-jobs)
# ============================================================

def scrape_jobs(search_term=None):
    """
    Scrape job listings from the fake jobs website.
    Optionally filter by a search term (matches title, company, or location).
    Returns a list of job dictionaries.
    """

    # Step 1: Fetch the web page (like opening it in your browser)
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url, timeout=10)

    # Check if the request was successful (status code 200 = OK)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return []

    # Step 2: Parse the HTML content with BeautifulSoup
    # This turns raw HTML into a searchable tree structure
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 3: Find all job listing cards on the page
    # We inspect the page's HTML to find the right CSS class
    job_cards = soup.find_all("div", class_="card-content")

    # Step 4: Extract data from each job card
    jobs = []
    for card in job_cards:
        # .find() locates the first matching element inside the card
        title = card.find("h2", class_="title").text.strip()
        company = card.find("h3", class_="company").text.strip()
        location = card.find("p", class_="location").text.strip()

        # Get the "Apply" link from the card's footer
        footer = card.find_next_sibling("footer")
        apply_link = ""
        if footer:
            link_tag = footer.find("a", string="Apply")
            if link_tag:
                apply_link = link_tag.get("href", "")

        # Build a dictionary for this job
        job = {
            "title": title,
            "company": company,
            "location": location,
            "apply_link": apply_link,
        }

        # Step 5: Filter by search term if one was provided
        if search_term:
            # Convert everything to lowercase so search is case-insensitive
            term = search_term.lower()
            if (
                term in title.lower()
                or term in company.lower()
                or term in location.lower()
            ):
                jobs.append(job)
        else:
            jobs.append(job)

    return jobs


# ============================================================
# SCRAPER 2: Hacker News (news.ycombinator.com)
# A completely different HTML structure — this is the key lesson!
# ============================================================

def parse_time_ago(time_str):
    """
    Convert a string like '4 hours ago' into total minutes.
    This lets us sort stories by how recent they are.
    Uses regular expressions (re) to extract the number from the string.
    """
    if not time_str:
        return 0

    # re.search(r"\d+", text) finds the first number in the text
    match = re.search(r"(\d+)", time_str)
    if not match:
        return 0

    num = int(match.group(1))

    # Convert to minutes based on the time unit
    if "minute" in time_str:
        return num
    elif "hour" in time_str:
        return num * 60
    elif "day" in time_str:
        return num * 60 * 24
    return 0


def scrape_hackernews(search_term=None, sort_by="default"):
    """
    Scrape the Hacker News front page.
    HN uses a table-based layout (old-school HTML), so the parsing
    logic is very different from the job listings site.
    sort_by: "default" (HN ranking), "newest", or "oldest"
    Returns a list of story dictionaries.
    """

    url = "https://news.ycombinator.com"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print(f"Failed to fetch HN. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # HN uses <tr class="athing"> for each story row
    # Each story has TWO rows: the title row and the subtext row below it
    story_rows = soup.find_all("tr", class_="athing")

    stories = []
    for row in story_rows:
        # The title is inside a <span class="titleline"> with an <a> tag
        titleline = row.find("span", class_="titleline")
        if not titleline:
            continue

        link_tag = titleline.find("a")
        if not link_tag:
            continue

        title = link_tag.text.strip()
        story_url = link_tag.get("href", "")

        # Some HN links are relative (e.g. "item?id=123"), make them absolute
        if story_url.startswith("item?"):
            story_url = f"https://news.ycombinator.com/{story_url}"

        # Get the site domain if shown (e.g. "(github.com)")
        site_tag = titleline.find("span", class_="sitestr")
        site = site_tag.text.strip() if site_tag else ""

        # The subtext row is the NEXT sibling <tr> — it has points, author, comments
        # .find_next_sibling() finds the next <tr> after the current one
        subtext_row = row.find_next_sibling("tr")
        points = ""
        author = ""
        comments = ""
        time_ago = ""

        if subtext_row:
            subtext = subtext_row.find("td", class_="subtext")
            if subtext:
                # Points: <span class="score">
                score_tag = subtext.find("span", class_="score")
                points = score_tag.text.strip() if score_tag else "0 points"

                # Author: <a class="hnuser">
                author_tag = subtext.find("a", class_="hnuser")
                author = author_tag.text.strip() if author_tag else ""

                # Time: <span class="age">
                age_tag = subtext.find("span", class_="age")
                time_ago = age_tag.text.strip() if age_tag else ""

                # Comments: last <a> in subtext that contains "comment"
                all_links = subtext.find_all("a")
                for a in all_links:
                    if "comment" in a.text or "discuss" in a.text:
                        comments = a.text.strip()

        # Convert "4 hours ago" to a number (240 minutes) for sorting
        minutes_ago = parse_time_ago(time_ago)

        story = {
            "title": title,
            "url": story_url,
            "site": site,
            "points": points,
            "author": author,
            "time_ago": time_ago,
            "minutes_ago": minutes_ago,
            "comments": comments,
        }

        # Filter by search term if provided
        if search_term:
            term = search_term.lower()
            if (
                term in title.lower()
                or term in site.lower()
                or term in author.lower()
            ):
                stories.append(story)
        else:
            stories.append(story)

    # Sort stories if requested
    # sorted() creates a new list, key= tells it what to sort by
    # reverse=True means descending order (biggest number first = oldest)
    if sort_by == "newest":
        stories = sorted(stories, key=lambda s: s["minutes_ago"])
    elif sort_by == "oldest":
        stories = sorted(stories, key=lambda s: s["minutes_ago"], reverse=True)

    return stories


# This runs when you execute the file directly: python3 scraper.py
if __name__ == "__main__":
    # Test the job scraper
    print("=== SCRAPER 1: Job Listings ===\n")
    jobs = scrape_jobs()
    print(f"Found {len(jobs)} jobs!\n")
    for i, job in enumerate(jobs[:3], start=1):
        print(f"{i}. {job['title']}")
        print(f"   Company:  {job['company']}")
        print(f"   Location: {job['location']}")
        print()

    # Test the Hacker News scraper
    print("=== SCRAPER 2: Hacker News ===\n")
    stories = scrape_hackernews()
    print(f"Found {len(stories)} stories!\n")
    for i, story in enumerate(stories[:5], start=1):
        print(f"{i}. {story['title']}")
        print(f"   {story['points']} | {story['author']} | {story['time_ago']} | {story['comments']}")
        print(f"   {story['url']}")
        print()
