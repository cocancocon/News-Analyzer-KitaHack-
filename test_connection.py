"""
Simple Database Connection Test
Run this to check if Python can connect to PostgreSQL
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("="*60)
print("🔌 TESTING DATABASE CONNECTION")
print("="*60)

# Step 1: Check if .env file exists
if not os.path.exists('.env'):
    print("\nERROR: .env file not found!")
    print("\nCreate .env file with:")
    print("""
DB_HOST=localhost
DB_PORT=5432
DB_NAME=news_scraper
DB_USER=postgres
DB_PASSWORD=your_password_here
    """)
    exit(1)

# Step 2: Load database config from .env
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}

print("\n📋 Configuration from .env:")
print(f"  Host: {db_config['host']}")
print(f"  Port: {db_config['port']}")
print(f"  Database: {db_config['database']}")
print(f"  User: {db_config['user']}")
print(f"  Password: {'*' * len(db_config['password']) if db_config['password'] else 'NOT SET'}")

# Step 3: Check if password is set
if not db_config['password']:
    print("\nERROR: DB_PASSWORD not set in .env file!")
    print("\nEdit your .env file and set DB_PASSWORD=your_actual_password")
    exit(1)

# Step 4: Try to import psycopg2
print("\n📦 Checking psycopg2 installation...")
try:
    import psycopg2
    print(" psycopg2 is installed")
except ImportError:
    print(" psycopg2 not installed!")
    print("\n  Install with: pip install psycopg2-binary")
    exit(1)

# Step 5: Try to connect
print("\n🔌 Attempting to connect to database...")
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    print("  ✅ CONNECTION SUCCESSFUL!")
    
    # Test query
    print("\n🧪 Running test query...")
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"  ✅ PostgreSQL version: {version.split(',')[0]}")
    
    # Check if database exists
    cursor.execute("SELECT current_database();")
    db_name = cursor.fetchone()[0]
    print(f"  ✅ Connected to database: {db_name}")
    
    # Close connection
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE CONNECTION TEST PASSED!")
    print("="*60)
    print("\nYou're ready for next steps:")
    print("  1. Create database tables: python scripts/setup_database.py")
    print("  2. Test the scraper: python scripts/test_scraper.py")
    print("="*60 + "\n")
    
except psycopg2.OperationalError as e:
    error_msg = str(e).lower()
    print("  ❌ CONNECTION FAILED!")
    print(f"\n  Error: {e}")
    
    print("\n🔍 Troubleshooting:")
    
    if "password authentication failed" in error_msg:
        print("\n  ❌ WRONG PASSWORD!")
        print("  → Check DB_PASSWORD in your .env file")
        print("  → Make sure it matches your PostgreSQL password")
        
    elif "database" in error_msg and "does not exist" in error_msg:
        print("\n  ❌ DATABASE DOESN'T EXIST!")
        print("  → Open pgAdmin")
        print("  → Create database 'news_scraper'")
        
    elif "connection refused" in error_msg or "could not connect" in error_msg:
        print("\n  ❌ POSTGRESQL IS NOT RUNNING!")
        print("  → Open Services (Win + R, type 'services.msc')")
        print("  → Find 'postgresql-x64-18' (or similar)")
        print("  → Make sure Status = 'Running'")
        print("  → If not, right-click and select 'Start'")
    
    else:
        print("\n  Check:")
        print("  1. PostgreSQL is running (check Services)")
        print("  2. Database 'news_scraper' exists (check pgAdmin)")
        print("  3. Password is correct in .env file")
    
except Exception as e:
    print(f"  ❌ Unexpected error: {e}")
    print(f"\n  Error type: {type(e).__name__}")