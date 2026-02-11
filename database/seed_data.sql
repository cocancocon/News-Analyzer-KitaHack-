INSERT INTO states (name, code) VALUES
    ('Johor', 'JHR'),
    ('Kedah', 'KDH'),
    ('Kelantan', 'KTN'),
    ('Melaka', 'MLK'),
    ('Negeri Sembilan', 'NSN'),
    ('Pahang', 'PHG'),
    ('Penang', 'PNG'),
    ('Perak', 'PRK'),
    ('Perlis', 'PLS'),
    ('Sabah', 'SBH'),
    ('Sarawak', 'SWK'),
    ('Selangor', 'SGR'),
    ('Terengganu', 'TRG'),
    ('Kuala Lumpur', 'KUL'),
    ('Putrajaya', 'PJY'),
    ('Labuan', 'LBN')
ON CONFLICT (name) DO NOTHING;

-- INSERT NEWS SOURCES
INSERT INTO sources (name, rss_url, base_url, active) VALUES
    (
        'The Star',
        'https://www.thestar.com.my/rss/news/nation/',
        'https://www.thestar.com.my',
        TRUE
    ),
    (
        'Free Malaysia Today',
        'https://www.freemalaysiatoday.com/feed/',
        'https://www.freemalaysiatoday.com',
        TRUE
    ),
    (
        'Malay Mail',
        'https://www.malaymail.com/feed/malaysia',
        'https://www.malaymail.com',
        TRUE
    ),
    (
        'Bernama',
        'https://www.bernama.com/en/rss/news_malaysia.php',
        'https://www.bernama.com',
        TRUE
    ),
    (
        'New Straits Times',
        'https://www.nst.com.my/rss',
        'https://www.nst.com.my',
        TRUE
    ),
    (
        'Malaysiakini',
        'https://www.malaysiakini.com/rss',
        'https://www.malaysiakini.com',
        TRUE
    ),
    (
        'The Edge Markets',
        'https://www.theedgemarkets.com/rss/my',
        'https://www.theedgemarkets.com',
        FALSE
    ),
    (
        'Berita Harian',
        'https://www.bharian.com.my/rss',
        'https://www.bharian.com.my',
        TRUE
    )
ON CONFLICT (name) DO NOTHING;

-- VERIFICATION QUERIES
-- Check states
SELECT COUNT(*) as total_states FROM states;

-- Check sources
SELECT name, active FROM sources ORDER BY name;

-- Summary
SELECT 
    (SELECT COUNT(*) FROM states) as total_states,
    (SELECT COUNT(*) FROM sources) as total_sources,
    (SELECT COUNT(*) FROM sources WHERE active = TRUE) as active_sources;