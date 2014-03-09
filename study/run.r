library(httr)
library(sqldf)

db.url <- parse_httr(sys.getenv('CLOUD_BEDS_DB'))
