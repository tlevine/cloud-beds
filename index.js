var url     = require('url');
var search3Taps = require('./helpers/search3Taps');

function main() {
  var APIKEY
  if (! (APIKEY = process.env.APIKEY)) {
    console.log('You need to set the APIKEY environment variable to your 3Taps API key.');
    process.exit(1);
  } else {
    search3Taps(2, function(){});
  }

}

function downloadCraigslist(craigslistUrl) {
  url.parse(craigslistUrl);
}

main();
