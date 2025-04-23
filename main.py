import json
import datetime

from parser import parse_job_description
from scraper import search_candidates_google
from ranker import rank_candidate

HISTORY_FILE = "history.json"

def save_to_history(job, candidates):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "job_description": job,
        "candidates": candidates
    }
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def main():
    job_description = input("Paste job description:\n")

    # 1. Parse the job description
    parsed = parse_job_description(job_description)
    print("\nParsed Job Details:\n", parsed)

    # 2. Search LinkedIn profiles using DuckDuckGo
    try:
        links = search_candidates_google(parsed['job_title'], parsed['skills'])
        print("\nFound Profiles:\n", links)
    except Exception as e:
        print(f"An error occurred during candidate search: {e}")
        links = []

    # 3. Evaluate and rank candidates
    candidates = []
    for link in links:
        print(f"\nRanking candidate: {link}")
        result = rank_candidate(job_description, link)
        print(result)
        candidates.append({"url": link, "evaluation": result})

    # 4. Save to history
    save_to_history(job_description, candidates)

    # 5. Print ranked candidates
    print("\n=== Ranked Candidates ===")
    for c in sorted(candidates, key=lambda x: json.loads(x["evaluation"])["score"], reverse=True):
        summary = json.loads(c["evaluation"])
        print(f"{c['url']}: Score {summary['score']} – {summary['reason']}")

if __name__ == "__main__":
    main()
