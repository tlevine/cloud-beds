var request = require('request')

function main() {
  var APIKEY
  if (! (APIKEY = process.env.APIKEY)) {
    console.log('You need to set the APIKEY environment variable to your 3Taps API key.')
    process.exit(1)
  }
}

"http://search.3taps.com?auth_token=$APIKEY&location.state=USA-NY&category=RSUB"

main()
