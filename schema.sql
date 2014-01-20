CREATE TABLE IF NOT EXISTS searches (
  url TEXT NOT NULL,
  date DATE NOT NULL,
  tier INTEGER NOT NULL,
  page INTEGER NOT NULL,
  result JSON TEXT NOT NULL,
  UNIQUE (url, date, tier, page)
);

CREATE TABLE IF NOT EXISTS results (
  url TEXT NOT NULL,
  price INTEGER,
  start INTEGER,
  end INTEGER,
  furnished INTEGER NOT NULL,
  UNIQUE(url)
);
