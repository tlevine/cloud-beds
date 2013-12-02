var request = require('request');

function downloadCraigslist(craigslistUrl) {
  craigslistUrl.sub(/^https?:\/\//, '')
}

module.exports = downloadCraigslist
