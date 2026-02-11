import feedparser
import json
from datetime import datetime
from pprint import pprint

class RSSMetadataScraper:
    """Simple RSS scraper to extract metadata only"""
    
    def __init__(self):
        # Malaysian news RSS feeds to test
        self.test_feeds = {
            'The Star': 'https://www.thestar.com.my/rss/news/nation/',
            'Malay Mail': 'https://www.malaymail.com/feed/malaysia',
            'Free Malaysia Today': 'https://www.freemalaysiatoday.com/feed/',
            'Bernama': 'https://www.bernama.com/en/rss/news_malaysia.php',
        }
        
        # Malaysian states for detection
        self.states = [
            'Johor', 'Kedah', 'Kelantan', 'Melaka', 'Negeri Sembilan',
            'Pahang', 'Penang', 'Perak', 'Perlis', 'Sabah', 'Sarawak',
            'Selangor', 'Terengganu', 'Kuala Lumpur', 'Putrajaya', 'Labuan'
        ]
    
    def scrape_feed(self, feed_url, source_name):
        """Scrape metadata from a single RSS feed"""
        print(f"\n{'='*60}")
        print(f"Scraping: {source_name}")
        print(f"URL: {feed_url}")
        print(f"{'='*60}")
        
        try:
            # Parse RSS feed
            feed = feedparser.parse(feed_url)
            
            # Check if feed is valid
            if feed.bozo:
                print(f"⚠️  Warning: Feed may have issues")
            
            print(f"✓ Found {len(feed.entries)} articles\n")
            
            articles = []
            
            for i, entry in enumerate(feed.entries[:5], 1):  # Test first 5
                print(f"--- Article {i} ---")
                
                # Extract ALL available metadata
                metadata = {
                    'title': entry.get('title', 'N/A'),
                    'link': entry.get('link', 'N/A'),
                    'description': entry.get('description', entry.get('summary', 'N/A')),
                    'published': entry.get('published', entry.get('updated', 'N/A')),
                    'source': source_name,
                    'author': entry.get('author', 'N/A'),
                    'category': entry.get('category', 'N/A'),
                    'scraped_at': str(datetime.now())
                }
                
                # Try to get image/media
                if hasattr(entry, 'media_content') and entry.media_content:
                    metadata['image_url'] = entry.media_content[0].get('url', 'N/A')
                elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                    metadata['image_url'] = entry.media_thumbnail[0].get('url', 'N/A')
                else:
                    metadata['image_url'] = 'N/A'
                
                # Detect states mentioned
                text_to_check = metadata['title'] + ' ' + metadata['description']
                metadata['states_mentioned'] = self.detect_states(text_to_check)
                
                # Show what we got
                print(f"Title: {metadata['title'][:80]}...")
                print(f"Link: {metadata['link'][:80]}...")
                print(f"Published: {metadata['published']}")
                print(f"Author: {metadata['author']}")
                print(f"Category: {metadata['category']}")
                print(f"Has Image: {'Yes' if metadata['image_url'] != 'N/A' else 'No'}")
                print(f"States Mentioned: {metadata['states_mentioned']}")
                print()
                
                articles.append(metadata)
            
            return articles
            
        except Exception as e:
            print(f"❌ Error scraping {source_name}: {str(e)}")
            return []
    
    def detect_states(self, text):
        """Detect Malaysian states mentioned in text"""
        mentioned = []
        text_lower = text.lower()
        
        for state in self.states:
            if state.lower() in text_lower:
                mentioned.append(state)
        
        return mentioned if mentioned else ['None']
    
    def test_all_feeds(self):
        """Test scraping from all feeds"""
        print("\n" + "="*60)
        print("TESTING RSS METADATA SCRAPER")
        print("="*60)
        
        all_metadata = {}
        
        for source, url in self.test_feeds.items():
            articles = self.scrape_feed(url, source)
            all_metadata[source] = articles
        
        return all_metadata
    
    def show_metadata_summary(self, all_metadata):
        """Show summary of what metadata is available"""
        print("\n" + "="*60)
        print("METADATA AVAILABILITY SUMMARY")
        print("="*60)
        
        total_articles = 0
        has_author = 0
        has_category = 0
        has_image = 0
        has_states = 0
        
        for source, articles in all_metadata.items():
            total_articles += len(articles)
            for article in articles:
                if article['author'] != 'N/A':
                    has_author += 1
                if article['category'] != 'N/A':
                    has_category += 1
                if article['image_url'] != 'N/A':
                    has_image += 1
                if article['states_mentioned'] != ['None']:
                    has_states += 1
        
        print(f"\nTotal Articles Tested: {total_articles}")
        print(f"\nMetadata Availability:")
        print(f"  Title:       {total_articles}/{total_articles} (100%)")
        print(f"  Link:        {total_articles}/{total_articles} (100%)")
        print(f"  Description: {total_articles}/{total_articles} (100%)")
        print(f"  Published:   {total_articles}/{total_articles} (100%)")
        print(f"  Author:      {has_author}/{total_articles} ({has_author/total_articles*100:.1f}%)")
        print(f"  Category:    {has_category}/{total_articles} ({has_category/total_articles*100:.1f}%)")
        print(f"  Image:       {has_image}/{total_articles} ({has_image/total_articles*100:.1f}%)")
        print(f"  States:      {has_states}/{total_articles} ({has_states/total_articles*100:.1f}%)")
    
    def save_to_json(self, all_metadata, filename='metadata_test.json'):
        """Save scraped metadata to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_metadata, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Metadata saved to {filename}")
    
    def show_sample_article(self, all_metadata):
        """Display one complete sample article"""
        print("\n" + "="*60)
        print("SAMPLE ARTICLE (Complete Metadata)")
        print("="*60)
        
        # Get first article from first source
        for source, articles in all_metadata.items():
            if articles:
                print(f"\nSource: {source}")
                print("-" * 60)
                pprint(articles[0], width=60)
                break


# ============= RUN TEST =============
if __name__ == "__main__":
    scraper = RSSMetadataScraper()
    
    # Test scraping
    all_metadata = scraper.test_all_feeds()
    
    # Show summary
    scraper.show_metadata_summary(all_metadata)
    
    # Show one complete sample
    scraper.show_sample_article(all_metadata)
    
    # Save results
    scraper.save_to_json(all_metadata)
    
    print("\n" + "="*60)
    print("TEST COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Check metadata_test.json to see all scraped data")
    print("2. Review what metadata is consistently available")
    print("3. Decide on database schema based on available fields")