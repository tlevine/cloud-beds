library(ggplot2)

if (!('s' %in% ls())) {
}
s <- read.csv('/tmp/sublets.csv', stringsAsFactors = FALSE, na.strings = '')
subset(s, !is.na(s$start))
