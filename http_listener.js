var http_port = process.env.PORT || 5000;

var express = require('express'), app = express()
, http = require('http')
, server = http.createServer(app)
, jade = require('jade');

app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.set("view options", { layout: false });
app.use(express.static(__dirname + '/public'));
app.get('/', function(req, res){
    res.render('home.jade');
});
server.listen(http_port);
console.log("HTTP listening on " + http_port);