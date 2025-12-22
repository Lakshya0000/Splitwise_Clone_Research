import json
from collections import Counter
import re

def deep_analyze_reviews():
    with open('splitwise_clone_research/splitwise_reviews.json', 'r', encoding='utf-8') as f:
        reviews = json.load(f)

    print(f"Analyzing {len(reviews)} reviews...")

    # --- Categories for Deep Analysis ---
    categories = {
        "Monetization (Limits/Ads)": ["limit", "daily", "3 expenses", "subscription", "pay", "pro", "ads", "premium", "greedy", "money"],
        "Technical (Sync/Crash)": ["sync", "crash", "bug", "slow", "server", "connection", "offline", "load", "glitch", "hang"],
        "Authentication (Login/Signup)": ["login", "sign in", "password", "email", "verification", "code", "otp", "account"],
        "UX/UI (Design/Flow)": ["complicated", "confusing", "hard to use", "interface", "design", "navigate", "cluttered", "font"],
        "Missing Features": ["search", "export", "receipt", "scan", "chart", "graph", "dark mode", "widget", "calculator"]
    }

    stats = {cat: 0 for cat in categories}
    specific_issues = Counter()

    # --- Processing All Reviews ---
    for r in reviews:
        if not r['content']:
            continue
        text = r['content'].lower()
        
        # Categorize
        for cat, keywords in categories.items():
            for k in keywords:
                if k in text:
                    stats[cat] += 1
                    # We break to avoid double counting a category for the same review (e.g. "pay" and "money")
                    break
        
        # Track specific keywords for finer detail
        all_keywords = [k for cat in categories.values() for k in cat]
        for k in all_keywords:
            if k in text:
                specific_issues[k] += 1

    # --- Output Analysis Data ---
    print("\n--- Category Breakdown ---")
    for cat, count in stats.items():
        print(f"{cat}: {count} reviews ({count/len(reviews)*100:.1f}%)")

    print("\n--- Specific Keyword Frequency (Top 20) ---")
    for k, v in specific_issues.most_common(20):
        print(f"{k}: {v}")

    # --- Generate 'impactful_reviews.md' ---
    # Top 50 reviews by thumbsUpCount
    sorted_reviews = sorted(reviews, key=lambda x: x['thumbsUpCount'], reverse=True)[:50]
    
    with open('splitwise_clone_research/impactful_reviews.md', 'w', encoding='utf-8') as f:
        f.write("# Top 50 Most Impactful Negative Reviews\n\n")
        f.write("These reviews are selected based on 'Thumbs Up' count, indicating high user agreement.\n\n")
        for i, r in enumerate(sorted_reviews):
            f.write(f"## Review #{i+1}\n")
            f.write(f"**Thumbs Up:** {r['thumbsUpCount']} | **Rating:** {r['score']}/5\n\n")
            f.write(f"> {r['content']}\n\n")
            f.write("---\n")
            
    print("\nSuccessfully generated 'splitwise_clone_research/impactful_reviews.md'")

if __name__ == "__main__":
    deep_analyze_reviews()
