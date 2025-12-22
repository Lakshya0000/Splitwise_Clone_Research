import json
from google_play_scraper import reviews_all, Sort

APP_ID = 'com.Splitwise.SplitwiseMobile'

def fetch_and_filter_reviews():
    print(f"Fetching ALL reviews for {APP_ID}...")
    
    # Fetch everything
    all_reviews = reviews_all(
        APP_ID,
        sleep_milliseconds=0,
        lang='en',
        country='us',
        sort=Sort.MOST_RELEVANT
    )
    
    print(f"Total reviews fetched: {len(all_reviews)}")
    
    # Filter: Keep only reviews with score < 5
    # Select: Only keep 'content', 'score', 'thumbsUpCount'
    filtered_reviews = [
        {
            'content': r['content'],
            'score': r['score'],
            'thumbsUpCount': r['thumbsUpCount']
        }
        for r in all_reviews
        if r['score'] < 5
    ]
    
    print(f"Filtered down to {len(filtered_reviews)} reviews (Score < 5).")
    
    # Save to JSON
    filename = 'splitwise_reviews.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(filtered_reviews, f, indent=4)
        
    print(f"Filtered reviews saved to {filename}")

if __name__ == "__main__":
    fetch_and_filter_reviews()
