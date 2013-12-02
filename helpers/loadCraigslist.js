var request = require('request');
var url = require('url')

function loadCraigslist(craigslistUrl, callback) {
  var parsedUrl = url.parse(craigslistUrl);
  var requestUrl = parsedUrl.protocol + '//' + parsedUrl.host + parsedUrl.path
  var fileName = parsedUrl.host.sub(/\..*$/, '') + parsedUrl.path

  var headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0"
  };

  fs.exists(fileName, function(exists) {
    if (exists) {
      var fs.fileStream = fs.createReadStream(fileName);
    } else {
      var fileStream = request.get({"url":requestUrl,"headers":headers}).pipe(fs.createWriteStream(fileName));
    }
    callback(fileStream);
  }
}

module.exports = loadCraigslist;
