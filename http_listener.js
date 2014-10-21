var http_port = process.env.PORT || 5000;

var express = require('express'), app = express()
, http = require('http')
, server = http.createServer(app)
, jade = require('jade');

var sockjs = require('sockjs');
var chatSocket = sockjs.createServer();
chatSocket.installHandlers(server, {prefix:'/chat'});


app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.set("view options", { layout: false });
app.configure(function() {
    app.use(express.static(__dirname + '/public'));
});
app.get('/', function(req, res){
    var tcpURI = null;
    if ( tcp ) {
        tcpURI = process.env.RUPPELLS_SOCKETS_FRONTEND_URI;
    }
    res.render('home.jade', { 'tcpURI': tcpURI });
});
server.listen(http_port);
console.log("HTTP listening on " + http_port);
chatSocket.on('connection', function(conn) {
    var name = "HTTP -> " + conn.remoteAddress + ":" + conn.remotePort;
    peeps[name] = {
        'send' : function (message, sender) { conn.write(JSON.stringify({ 'message' : message, 'name' : sender })); }
    };
    conn.write(JSON.stringify({ 'message' : "Welcome " + name, 'name' : "Server"}));
    joined(name);
    conn.on('data', function (message) {
        broadcast(message, name);
    });
    conn.on('disconnect', function () {
        left(name);
    });

    conn.on('data', function(message) {
        conn.write(message);
    });
    conn.on('close', function() {});
});