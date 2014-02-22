library(ggplot2)

s <- read.csv('/tmp/sublets.csv', stringsAsFactors = FALSE, na.strings = '')
candidates <- subset(s, !is.na(s$start) & subdomain == 'austin' & section == 'sub' & end <= 4)
candidates <- candidates[order(candidates$posted),]
print(candidates[c('price','start','end','url')])
