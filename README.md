# MC Auth Server

This server authenticates users via Minecraft and can run on a single Heroku dyno.

### How it works:

0. User joins the Auth Server
0. User receives a token (password) and is disconnected
0. The UUID and token are sent to your website  
   You store this pair for a short while
0. User enters their token on your website
0. You compare this token with the stored one  
   Authentication is complete when the tokens match

Tokens are pronouncable and thus memorable.  
Only paid accounts are accepted by MC Auth Server.

See [here](https://github.com/Jake0oo0/SpongeDev/blob/0fff10d0c8c50d405acd9e2af2d7ca4da6a23c71/app/controllers/authentications_controller.rb#L27) for an example server-side implementation.


### UX

Inside Minecraft:  
![server demo gif](https://i.imgur.com/GNTtNsf.gif)

On your website:  
![web demo gif](https://i.imgur.com/0dl3nHg.gif)

## Installing

#### Environment variables

* `WEBSITE_URI`: The full URI where uuid + token are POSTed to
* `WEBSITE_AUTH_KEY`: The `X-AUTH-SERVER-KEY` HTTP Header

#### On your machine
* Make sure you've got python installed
* `pip install -r requirements.txt`
* `./launch.py`  
  **options:**  
  -a \<address to listen on\> *(default 0.0.0.0)*  
  -p \<port to listen on\> *(default 25565)*
* connect to localhost

#### On Heroku
* `heroku create`
* `heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git`
* `heroku addons:add ruppells-sockets`
* `git push heroku master`
* Get output of `heroku config:get RUPPELLS_SOCKETS_FRONTEND_URI`
* Connect to that URI, minus the tcp:// URI identifier.


## Credits
* The Minecraft packet handling and original files are based on the work of [@barneygale](https://github.com/barneygale) on [Quarry](https://github.com/barneygale/quarry).
* The http_listener.js file is based on the work of [Ruppells](https://bitbucket.org/ruppells) on their [Ruppell's Sockets](https://devcenter.heroku.com/articles/ruppells-sockets) [demo project.](https://bitbucket.org/ruppells/nodejs-tcp-ws-chat-demo/src/539759380487?at=master).
* Migration to using Ruppell's sockets is the work of [@Jake0oo0](https://github.com/Jake0oo0).
* Token generation and website connection was added by [@jomo](https://github.com/jomo).