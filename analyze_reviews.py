import json
from collections import Counter
import re

def analyze_reviews():
    with open('splitwise_clone_research/splitwise_reviews.json', 'r', encoding='utf-8') as f:
        reviews = json.load(f)

    print(f"Total reviews to analyze: {len(reviews)}")

    # 1. Rating Distribution
    scores = [r['score'] for r in reviews]
    score_counts = Counter(scores)
    print("\n--- Rating Distribution (of reviews < 5 stars) ---")
    for score in sorted(score_counts.keys()):
        print(f"{score} Stars: {score_counts[score]}")

    # 2. Top Issues (Keyword Frequency)
    # Simple keyword checking for common SaaS complaints
    keywords = {
        "limit": 0, "daily": 0, "3 expenses": 0, "subscription": 0, 
        "pay": 0, "pro": 0, "ads": 0, "slow": 0, "crash": 0, 
        "bug": 0, "sync": 0, "currency": 0, "export": 0, "expensive": 0,
        "receipt": 0, "scan": 0, "simplify": 0, "chart": 0, "graph": 0
    }
    
    for r in reviews:
        if r['content'] is None:
            continue
        text = r['content'].lower()
        for k in keywords:
            if k in text:
                keywords[k] += 1
                
    print("\n--- Common Complaint Keywords ---")
    for k, v in sorted(keywords.items(), key=lambda item: item[1], reverse=True):
        print(f"{k}: {v}")

    # 3. Top 15 Most "Helpful" Negative Reviews
    # Sorted by thumbsUpCount descending
    sorted_reviews = sorted(reviews, key=lambda x: x['thumbsUpCount'], reverse=True)
    
    print("\n--- Top 15 Most Thumbed-Up Negative Reviews ---")
    for i, r in enumerate(sorted_reviews[:15]):
        print(f"\n#{i+1} (Score: {r['score']}, Thumbs: {r['thumbsUpCount']})")
        print(f"Content: {r['content']}")

if __name__ == "__main__":
    analyze_reviews()
