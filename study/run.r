library(httr)
library(sqldf)

db.credentials <- parse_url(Sys.getenv('CLOUD_BEDS_DB'))
options(sqldf.RPostgreSQL.user = db.credentials$username, 
        sqldf.RPostgreSQL.password = db.credentials$password,
        sqldf.RPostgreSQL.dbname = db.credentials$path,
        sqldf.RPostgreSQL.host = db.credentials$hostname, 
        sqldf.RPostgreSQL.port = db.credentials$port)

