# Sponge MC Auth Server

This authentication server is meant to be able to run on a single Heroku dyno, and authenticates users from the Sponge Server database.

When a user joins, a random token is generated and stored along with the UUID.
The authentication is completed when a user enters his username (which is converted to a UUID) and the token on the website.

## Installing

### On your machine
* Make sure you've got python installed
* `pip install -r requirements.txt`
* `./launch.py`  
  **options:**  
  -a \<address to listen on\> *(default 0.0.0.0)*  
  -p \<port to listen on\> *(default 25565)*
* connect to localhost

### Heroku
* heroku create
* heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
* heroku addons:add ruppells-sockets
* git push heroku master
* Get output of: heroku config:get RUPPELLS_SOCKETS_FRONTEND_URI
* Connect to that URI, minus the tcp:// URI identifier.


## Credits
* The Minecraft packet handling and original files are based on the work of [Barney Gale](https://github.com/barneygale) on [Quarry](https://github.com/barneygale/quarry).
* The http_listener.js file is based on the work of [Ruppells](https://bitbucket.org/ruppells) on their [Ruppell's Sockets](https://devcenter.heroku.com/articles/ruppells-sockets) [demo project.](https://bitbucket.org/ruppells/nodejs-tcp-ws-chat-demo/src/539759380487?at=master).
* Migration to using Ruppell's sockets is the work of [Jake0oo0](https://github.com/Jake0oo0).
