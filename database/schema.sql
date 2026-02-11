DROP TABLE IF EXISTS article_keywords CASCADE;
DROP TABLE IF EXISTS keywords CASCADE;
DROP TABLE IF EXISTS article_states CASCADE;
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS states CASCADE;
DROP TABLE IF EXISTS sources CASCADE;

CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    rss_url TEXT NOT NULL,
    base_url TEXT,
    active BOOLEAN DEFAULT TRUE,
    last_scraped TIMESTAMP,
    error_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE sources IS 'RSS news sources to scrape from';
COMMENT ON COLUMN sources.error_count IS 'Track failed scraping attempts';

CREATE TABLE states (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    code VARCHAR(3) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE states IS 'Malaysian states for trend analysis';

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    description TEXT,
    published_date TIMESTAMP,
    source_id INT REFERENCES sources(id) ON DELETE CASCADE,
    
    -- Optional metadata
    author VARCHAR(200),
    category VARCHAR(100),
    image_url TEXT,
    
    -- Timestamps
    scraped_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE articles IS 'Scraped news articles with metadata';

CREATE TABLE article_states (
    article_id INT REFERENCES articles(id) ON DELETE CASCADE,
    state_id INT REFERENCES states(id) ON DELETE CASCADE,
    mention_count INT DEFAULT 1,
    PRIMARY KEY (article_id, state_id)
);

COMMENT ON TABLE article_states IS 'Links articles to mentioned states';

CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) UNIQUE NOT NULL,
    total_count INT DEFAULT 0,
    last_seen TIMESTAMP DEFAULT NOW()
);

CREATE TABLE article_keywords (
    article_id INT REFERENCES articles(id) ON DELETE CASCADE,
    keyword_id INT REFERENCES keywords(id) ON DELETE CASCADE,
    frequency INT DEFAULT 1,
    PRIMARY KEY (article_id, keyword_id)
);

CREATE INDEX idx_articles_published ON articles(published_date DESC);
CREATE INDEX idx_articles_source ON articles(source_id);
CREATE INDEX idx_articles_scraped ON articles(scraped_at DESC);
CREATE INDEX idx_article_states_state ON article_states(state_id);
CREATE INDEX idx_article_states_article ON article_states(article_id);
CREATE INDEX idx_keywords_word ON keywords(word);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_updated_at
    BEFORE UPDATE ON articles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER sources_updated_at
    BEFORE UPDATE ON sources
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

COMMENT ON FUNCTION update_updated_at() IS 'Auto-update updated_at timestamp';