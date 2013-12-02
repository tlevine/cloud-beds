var request = require('request');

function search3Taps(rpp, apikey, callback){
  var apiUrl = "http://search.3taps.com?auth_token=" + apikey \
    + "&SOURCE=CRAIG&location.state=USA-NY&category=RSUB&retvals=id&rpp=" + rpp;

  requests.get({"url":apiUrl, json:true}, function(err, res, body) {
    if (err) {
      console.log('Error on ' + url);
      console.log(err);
      console.log(res);
      console.log(body);
      console.log('');
    } else {
      return callback(err, res, body);
  })
}

module.exports = search3Taps;
