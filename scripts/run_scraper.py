"""
Run Scraper
Main script to scrape all news sources
"""

import sys
import os

# Add parent directory to path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.scraper import NewsScraper

def main():
    """Run the news scraper"""
    print("\n" + "="*60)
    print("📰 MALAYSIAN NEWS SCRAPER")
    print("="*60)
    
    scraper = NewsScraper()
    
    # Scrape all sources
    stats = scraper.scrape_all_sources()
    
    if stats:
        print("\n✅ Scraping successful!")
        print(f"\nSummary:")
        print(f"  • Sources scraped: {stats['sources_scraped']}")
        print(f"  • Articles found: {stats['articles_found']}")
        print(f"  • Articles saved: {stats['articles_saved']}")
        
        # Get database statistics
        print("\n📊 Database Statistics:")
        db_stats = scraper.get_statistics()
        if db_stats:
            print(f"  • Total articles in DB: {db_stats['total_articles']}")
            print(f"  • Active sources: {db_stats['active_sources']}")
        
        return 0
    else:
        print("\n❌ Scraping failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)