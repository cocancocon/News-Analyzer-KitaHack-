"""
Database Operations
Handles all database connections and queries
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from backend.config import db_config

class Database:
    """Database connection and operations manager"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**db_config)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("✓ Connected to database")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✓ Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Query error: {e}")
            return []
    
    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Update error: {e}")
            self.conn.rollback()
            return False
    
    # ========================================
    # SOURCE OPERATIONS
    # ========================================
    
    def get_active_sources(self):
        """Get all active RSS sources"""
        query = """
            SELECT id, name, rss_url, base_url
            FROM sources
            WHERE active = TRUE
            ORDER BY name
        """
        return self.execute_query(query)
    
    def update_source_scraped(self, source_id):
        """Update last_scraped timestamp"""
        query = """
            UPDATE sources
            SET last_scraped = NOW(), error_count = 0
            WHERE id = %s
        """
        return self.execute_update(query, (source_id,))
    
    def increment_source_error(self, source_id):
        """Increment error count for failed scraping"""
        query = """
            UPDATE sources
            SET error_count = error_count + 1
            WHERE id = %s
        """
        return self.execute_update(query, (source_id,))
    
    # ========================================
    # ARTICLE OPERATIONS
    # ========================================
    
    def insert_article(self, article_data):
        """Insert article and return article ID"""
        query = """
            INSERT INTO articles 
            (title, url, description, published_date, source_id, 
             author, category, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                updated_at = NOW()
            RETURNING id
        """
        try:
            self.cursor.execute(query, (
                article_data.get('title'),
                article_data.get('url'),
                article_data.get('description'),
                article_data.get('published_date'),
                article_data.get('source_id'),
                article_data.get('author'),
                article_data.get('category'),
                article_data.get('image_url')
            ))
            self.conn.commit()
            result = self.cursor.fetchone()
            return result['id'] if result else None
        except Exception as e:
            print(f"❌ Error inserting article: {e}")
            self.conn.rollback()
            return None
    
    def get_recent_articles(self, limit=50):
        """Get recent articles"""
        query = """
            SELECT 
                a.id, a.title, a.url, a.description, 
                a.published_date, a.author, a.category,
                s.name as source_name
            FROM articles a
            JOIN sources s ON a.source_id = s.id
            ORDER BY a.published_date DESC
            LIMIT %s
        """
        return self.execute_query(query, (limit,))
    
    # ========================================
    # STATE OPERATIONS
    # ========================================
    
    def get_state_id(self, state_name):
        """Get state ID by name"""
        query = "SELECT id FROM states WHERE name = %s"
        result = self.execute_query(query, (state_name,))
        return result[0]['id'] if result else None
    
    def link_article_to_state(self, article_id, state_id):
        """Create article-state relationship"""
        query = """
            INSERT INTO article_states (article_id, state_id)
            VALUES (%s, %s)
            ON CONFLICT (article_id, state_id) DO NOTHING
        """
        return self.execute_update(query, (article_id, state_id))
    
    def get_state_trends(self, limit=10):
        """Get most mentioned states"""
        query = """
            SELECT 
                s.name, 
                COUNT(ast.article_id) as mention_count
            FROM states s
            LEFT JOIN article_states ast ON s.id = ast.state_id
            GROUP BY s.id, s.name
            HAVING COUNT(ast.article_id) > 0
            ORDER BY mention_count DESC
            LIMIT %s
        """
        return self.execute_query(query, (limit,))
    
    # ========================================
    # STATISTICS
    # ========================================
    
    def get_statistics(self):
        """Get overall statistics"""
        stats = {}
        
        # Total articles
        result = self.execute_query("SELECT COUNT(*) as count FROM articles")
        stats['total_articles'] = result[0]['count'] if result else 0
        
        # Total sources
        result = self.execute_query("SELECT COUNT(*) as count FROM sources WHERE active = TRUE")
        stats['active_sources'] = result[0]['count'] if result else 0
        
        # Articles per source
        query = """
            SELECT s.name, COUNT(a.id) as count
            FROM sources s
            LEFT JOIN articles a ON s.id = a.source_id
            GROUP BY s.name
            ORDER BY count DESC
        """
        stats['articles_per_source'] = self.execute_query(query)
        
        return stats