"""
Database Setup Script
Creates tables and inserts initial data
"""

import psycopg2
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_config():
    """Get database configuration from .env"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME', 'news_analyzer'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
    }

def run_sql_file(cursor, filepath):
    """Execute SQL file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql = f.read()
            cursor.execute(sql)
        print(f"  ✓ Executed: {filepath}")
        return True
    except FileNotFoundError:
        print(f"  ❌ File not found: {filepath}")
        return False
    except Exception as e:
        print(f"  ❌ Error executing {filepath}: {e}")
        return False

def setup_database():
    """Main setup function"""
    print("\n" + "="*60)
    print("🔧 SETTING UP DATABASE")
    print("="*60)
    
    db_config = get_db_config()
    
    try:
        # Connect to PostgreSQL
        print(f"\n📡 Connecting to database: {db_config['database']}")
        conn = psycopg2.connect(**db_config)
        conn.autocommit = True
        cursor = conn.cursor()
        print("  ✓ Connected to database")
        
        # Run schema
        print("\n📋 Creating database schema...")
        if not run_sql_file(cursor, 'database/schema.sql'):
            print("\n❌ Failed to create schema")
            print("Make sure database/schema.sql exists!")
            return False
        print("  ✓ Database schema created")
        
        # Run seed data
        print("\n🌱 Inserting seed data...")
        if not run_sql_file(cursor, 'database/seed_data.sql'):
            print("\n❌ Failed to insert seed data")
            print("Make sure database/seed_data.sql exists!")
            return False
        print("  ✓ Seed data inserted")
        
        # Verify setup
        print("\n🔍 Verifying setup...")
        cursor.execute("SELECT COUNT(*) FROM states")
        state_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sources")
        source_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sources WHERE active = TRUE")
        active_count = cursor.fetchone()[0]
        
        print(f"  ✓ States: {state_count}")
        print(f"  ✓ Sources: {source_count}")
        print(f"  ✓ Active sources: {active_count}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("="*60)
        print("\n📝 Next steps:")
        print("  1. Test scraper: python scripts/test_scraper.py")
        print("  2. Run scraper: python scripts/run_scraper.py")
        print("="*60 + "\n")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Database connection error: {e}")
        print("\n🔍 Troubleshooting:")
        print("  1. PostgreSQL is running?")
        print("  2. Database exists?")
        print("  3. Correct credentials in .env?")
        return False
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)