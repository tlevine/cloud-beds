library(ggplot2)

s <- read.csv('/tmp/sublets.csv', stringsAsFactors = FALSE, na.strings = '')

candidates <- subset(s, !is.na(s$start) & subdomain == 'austin' & section == 'sub' & start >= 2 & end <= 4 & !is.na(updated))
for (col in c('posted','updated')) {
  candidates[,col] <- as.POSIXct(candidates[,col])
}
candidates <- candidates[order(candidates$updated - candidates$posted),]
print(candidates[c('posted', 'price','start','end','url')])
