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
  posted INTEGER,
  updated INTEGER,
  weekly INTEGER NOT NULL,

  heading TEXT NOT NULL,
  long REAL NOT NULL,
  lat REAL NOT NULL,
  zipcode TEXT NOT NULL,
  address TEXT NOT NULL,

  superbowl INTEGER NOT NULL,
  sxsw INTEGER NOT NULL,
  UNIQUE(url)
);
