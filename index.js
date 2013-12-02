var request = require('request')
  , url     = require('url')

function main() {
  var APIKEY
  if (! (APIKEY = process.env.APIKEY)) {
    console.log('You need to set the APIKEY environment variable to your 3Taps API key.')
    process.exit(1)
  } else {
    search3Taps(2, )
  }

}

function search3Taps(rpp, callback){
  var apiUrl = "http://search.3taps.com?auth_token=" + APIKEY + \
    "&SOURCE=CRAIG&location.state=USA-NY&category=RSUB&retvals=id&rpp=" + rpp

  requests.get({"url":apiUrl, json:true}, function(err, res, body) {
    if (err) {
      console.log('Error on ' + url)
      console.log(err)
      console.log(res)
      console.log(body)
      console.log('')
    } else {
      return callback(err, res, body)
  })
}

function downloadCraigslist(craigslistUrl) {
  url.parse(craigslistUrl)
}

main()
