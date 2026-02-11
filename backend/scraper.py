"""
RSS News Scraper
Scrapes metadata from RSS feeds and saves to database
"""

import feedparser
from datetime import datetime
from dateutil import parser as date_parser
from backend.database import Database
from backend.config import Config

class NewsScraper:
    """RSS news scraper with database integration"""
    
    def __init__(self):
        self.db = Database()
        self.states = Config.MALAYSIAN_STATES
    
    def detect_states(self, text):
        """Detect Malaysian states mentioned in text"""
        if not text:
            return []
        
        mentioned = []
        text_lower = text.lower()
        
        for state in self.states:
            if state.lower() in text_lower:
                mentioned.append(state)
        
        return mentioned
    
    def parse_date(self, date_string):
        """Parse various date formats to datetime"""
        if not date_string:
            return None
        try:
            return date_parser.parse(date_string)
        except:
            return None
    
    def scrape_feed(self, rss_url, source_name, source_id):
        """
        Scrape one RSS feed
        
        Returns: List of article dictionaries
        """
        print(f"\n📰 Scraping: {source_name}")
        
        try:
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            if feed.bozo:
                print(f"  ⚠️  Feed may have issues")
            
            articles = []
            max_articles = Config.MAX_ARTICLES_PER_SOURCE
            
            for entry in feed.entries[:max_articles]:
                # Extract metadata
                article = {
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'description': entry.get('description', entry.get('summary', '')),
                    'published': entry.get('published', entry.get('updated', '')),
                    'author': entry.get('author', None),
                    'category': entry.get('category', None),
                    'source_id': source_id,
                    'source_name': source_name
                }
                
                # Parse published date
                article['published_date'] = self.parse_date(article['published'])
                
                # Get image
                if hasattr(entry, 'media_content') and entry.media_content:
                    article['image_url'] = entry.media_content[0].get('url')
                elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                    article['image_url'] = entry.media_thumbnail[0].get('url')
                else:
                    article['image_url'] = None
                
                # Detect states
                text_to_check = f"{article['title']} {article['description']}"
                article['states_mentioned'] = self.detect_states(text_to_check)
                
                articles.append(article)
            
            print(f"  ✓ Found {len(articles)} articles")
            return articles
            
        except Exception as e:
            print(f"  ❌ Error scraping {source_name}: {e}")
            return []
    
    def save_article_to_db(self, article):
        """Save article and its relationships to database"""
        try:
            # Insert article
            article_id = self.db.insert_article(article)
            
            if not article_id:
                return False
            
            # Link to states
            for state_name in article['states_mentioned']:
                state_id = self.db.get_state_id(state_name)
                if state_id:
                    self.db.link_article_to_state(article_id, state_id)
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error saving article: {e}")
            return False
    
    def scrape_all_sources(self):
        """
        Main function: Scrape all active sources and save to database
        
        Returns: Statistics about scraping session
        """
        print("\n" + "="*60)
        print("🚀 STARTING NEWS SCRAPING")
        print("="*60)
        
        # Connect to database
        if not self.db.connect():
            print("❌ Cannot connect to database")
            return None
        
        try:
            # Get active sources
            sources = self.db.get_active_sources()
            print(f"\n📊 Found {len(sources)} active sources")
            
            stats = {
                'sources_scraped': 0,
                'articles_found': 0,
                'articles_saved': 0,
                'errors': 0
            }
            
            # Scrape each source
            for source in sources:
                source_id = source['id']
                source_name = source['name']
                rss_url = source['rss_url']
                
                # Scrape feed
                articles = self.scrape_feed(rss_url, source_name, source_id)
                
                if articles:
                    stats['sources_scraped'] += 1
                    stats['articles_found'] += len(articles)
                    
                    # Save articles
                    saved_count = 0
                    for article in articles:
                        if self.save_article_to_db(article):
                            saved_count += 1
                        else:
                            stats['errors'] += 1
                    
                    stats['articles_saved'] += saved_count
                    
                    # Update source timestamp
                    self.db.update_source_scraped(source_id)
                    
                    print(f"  💾 Saved {saved_count}/{len(articles)} articles")
                else:
                    # Increment error count
                    self.db.increment_source_error(source_id)
                    stats['errors'] += 1
            
            # Print summary
            print("\n" + "="*60)
            print("✅ SCRAPING COMPLETE")
            print("="*60)
            print(f"Sources scraped: {stats['sources_scraped']}/{len(sources)}")
            print(f"Articles found: {stats['articles_found']}")
            print(f"Articles saved: {stats['articles_saved']}")
            print(f"Errors: {stats['errors']}")
            print("="*60)
            
            return stats
            
        except Exception as e:
            print(f"\n❌ Scraping failed: {e}")
            return None
        finally:
            self.db.disconnect()
    
    def get_statistics(self):
        """Get overall database statistics"""
        if not self.db.connect():
            return None
        
        try:
            stats = self.db.get_statistics()
            return stats
        finally:
            self.db.disconnect()


if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.scrape_all_sources()