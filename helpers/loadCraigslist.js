var request = require('request');
var url = require('url');
var mkdirp = require('mkdirp');
var fs = require('fs');

function loadCraigslist(craigslistUrl, callback) {
  var httpCraigslistUrl = 'http://' + craigslistUrl.replace(/^https?:\/\//,'');
  var parsedUrl = url.parse(httpCraigslistUrl);
  var requestUrl = parsedUrl.protocol + '//' + parsedUrl.host + parsedUrl.path;
  console.log(requestUrl)
  var fileName = 'craigslist/' + parsedUrl.host.replace(/\..*$/, '') + parsedUrl.path;

  fs.exists(fileName, cachedReadStream);
  
  function cachedReadStream(exists) {
    if (exists) {
      var fileStream = fs.createReadStream(fileName);
    } else {
      mkdirp.sync(fileName.replace(/\/[^\/]*$/,''))

      var headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0"
      };

      var fileStream = request.get({"url":requestUrl,"headers":headers}).pipe(fs.createWriteStream(fileName));
    }
    callback(fileStream);
  }
}

module.exports = loadCraigslist;

loadCraigslist('newyork.craigslist.org/brk/sub/4221657331.html', function(stream) {
  stream.setEncoding('utf8');
  stream.on('data', function(data) {
    console.log(data)
  })
})
