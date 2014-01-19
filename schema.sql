CREATE TABLE IF NOT EXISTS searches (
  id INTEGER PRIMARY KEY,
  rpp INTEGER NOT NULL,
  min_price INTEGER NOT NULL,
  max_price INTEGER NOT NULL,
  region TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS results (
  search INTEGER NOT NULL,
  date DATE NOT NULL,
  json JSON TEXT NOT NULL,
  UNIQUE (search, date),
  FOREIGN KEY search REFERENCES searches.id
);
