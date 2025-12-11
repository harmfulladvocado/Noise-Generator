import argparse
import random
import time
import sys
import signal
from html import unescape

try:
    import requests
except Exception:
    requests = None
    DEFAULT_TERMS = [
        "weather today", "pasta recipes", "technology news", "python tutorial",
        "best coffee", "tourist attractions amsterdam", "movie reviews",
        "gardening tips", "running plan", "budget travel",
        "weather tomorrow", "healthy smoothie recipes", "ai news", "javascript guide",
        "best tea", "museums in paris", "book reviews", "houseplants care",
        "cycling routes netherlands", "cheap flights", "cooking tips for beginners",
        "travel tips europe", "personal finance advice", "yoga exercises",
        "science news", "gaming reviews", "photography tips", "sustainable living",
        "home office setup", "netflix shows", "smartphone reviews", "weekend getaway ideas",
        "meditation guide", "concerts near me", "crypto news", "healthy lunch ideas",
        "weekly meal plan", "hiking trails", "children books recommendations",
        "student budget tips", "car reviews", "bali vacation", "online courses",
        "sports fixtures today", "diy projects", "movie trailers", "beginner guitar lessons",
        "how to code", "data science tutorial", "machine learning basics", "linux commands",
        "cloud computing guide", "remote work tips", "time management", "resume writing tips",
        "interview preparation", "public speaking tips", "english grammar help", "learn spanish",
        "parenting advice", "mental health resources", "healthy recipes dinner", "keto diet basics",
        "vegetarian meals", "meal prep ideas", "interior design trends", "small apartment ideas",
        "minimalist lifestyle", "decluttering tips", "organization hacks", "productivity apps",
        "calendar tips", "email management", "home workout routine", "bodyweight exercises",
        "marathon training plan", "cycling training", "triathlon tips", "sports nutrition",
        "bitcoin price", "stock market today", "investment strategies", "retirement planning",
        "real estate tips", "home buying guide", "mortgage calculator", "credit score help",
        "resume templates", "cover letter examples", "coding interview questions", "leetcode practice",
        "opencv tutorial", "pandas dataframe examples", "numpy cheatsheet", "visualization with matplotlib",
        "chart examples", "react tutorial", "vuejs guide", "angular introduction", "css grid examples",
        "html accessibility", "seo basics", "content marketing tips", "small business ideas",
        "startup fundraising", "agile methodology", "project management tools", "kanban vs scrum",
        "blockchain explained", "smart contracts", "ethical hacking basics", "cybersecurity tips",
        "password manager", "two factor authentication", "vpn guide", "privacy tools",
        "birdwatching tips", "camping checklist", "kayaking spots", "rock climbing guide",
        "photography composition", "portrait lighting tips", "travel photography tips", "drone rules",
        "classical music recommendations", "podcast suggestions", "audiobook platforms", "language learning apps"
    ]

def load_terms(path):
    try:
        with open(path, encoding="utf-8") as f:
            terms = [line.strip() for line in f if line.strip()]
            return terms or DEFAULT_TERMS
    except Exception as e:
        print(f"Cannot read terms file ({e}), using default list.")
        return DEFAULT_TERMS

def simulate_results(query, n):
    results = []
    for i in range(n):
        title = f"{query} — result {i+1}"
        url = f"https://example.com/search?q={query.replace(' ', '+')}&r={i+1}"
        results.append((title, url))
    return results

def ddg_search_html(query, n):
    if requests is None:
        return simulate_results(query, n)
    try:
        resp = requests.get("https://duckduckgo.com/html/", params={"q": query}, timeout=10)
        text = resp.text
    except Exception:
        return simulate_results(query, n)

    results = []
    parts = text.split('class="result__a"')
    for part in parts[1:]:
        href_idx = part.find('href="')
        if href_idx == -1:
            continue
        href_start = href_idx + len('href="')
        href_end = part.find('"', href_start)
        href = part[href_start:href_end]
        gt = part.find('>')
        end_a = part.find('</a>', gt)
        title_html = part[gt+1:end_a] if (gt != -1 and end_a != -1) else "No title"
        title = unescape(strip_tags(title_html)).strip()
        results.append((title, href))
        if len(results) >= n:
            break

    if not results:
        return simulate_results(query, n)
    return results

def strip_tags(html_snippet):
    out = []
    inside = False
    for ch in html_snippet:
        if ch == '<':
            inside = True
        elif ch == '>':
            inside = False
        elif not inside:
            out.append(ch)
    return ''.join(out)

def choose_term(terms, last):
    if not terms:
        raise ValueError("No search terms available.")
    if len(terms) == 1:
        return terms[0]
    choice = last
    while choice == last:
        choice = random.choice(terms)
    return choice

# silent: perform the search but don't print individual results
def perform_cycle(query, real_search, results_count):
    if real_search:
        _ = ddg_search_html(query, results_count)
    else:
        _ = simulate_results(query, results_count)
    # intentionally silent (no printing of results)

def signal_handler(_sig, _frame):
    print("\nInterrupted by user. Exiting.")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Search noise generator (DuckDuckGo or simulation)")
    parser.add_argument("--mode", choices=["once", "count", "forever"], default="forever",
                        help="Repeat mode: once, count or forever (default: forever)")
    parser.add_argument("--count", type=int, default=10,
                        help="Number of searches (only with --mode count)")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Seconds to wait between searches")
    parser.add_argument("--results", type=int, default=5,
                        help="Number of results to fetch per search")
    parser.add_argument("--real-search", action="store_true", default=True,
                        help="Perform real DuckDuckGo searches (requires requests) (default: on)")
    parser.add_argument("--terms-file", type=str, default=None,
                        help="Path to file with search terms (one per line). Otherwise built-in list.")
    args = parser.parse_args()

    if args.terms_file:
        terms = load_terms(args.terms_file)
    else:
        terms = DEFAULT_TERMS[:]

    if not terms:
        print("No terms found. Exiting.")
        return

    last = None
    iterations = 1 if args.mode == "once" else (args.count if args.mode == "count" else None)

    print(f"Starting search noise: mode={args.mode}, iterations={iterations if iterations is not None else '∞'}, delay={args.delay}s, results={args.results}, real_search={args.real_search}")

    i = 0
    try:
        while True:
            if iterations is not None and i >= iterations:
                break
            term = choose_term(terms, last)
            perform_cycle(term, args.real_search, args.results)
            last = term
            i += 1
            # show only the amount of searches performed (updates in-place)
            print(f"Searches performed: {i}", end="\r", flush=True)
            if iterations is not None and i >= iterations:
                break
            time.sleep(args.delay)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    # print final total on its own line
    print(f"\nTotal searches performed: {i}")
    print("Done.")

if __name__ == "__main__":
    main()