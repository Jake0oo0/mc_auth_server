from quarry.net.server import ServerFactory, ServerProtocol
from random import randrange
from os import environ
from base64 import b64encode
from json import loads as jsondecode
import urllib2

###
### AUTH SERVER
###   ask mojang to authenticate the user
###

def generate_token(length):
    """
    generates a pronouncable token
    """
    cons = 'bcdfghjklmnpqrstvwxyz'
    vows = 'aeiou'
    token = ''
    start = randrange(2) # begin with con or vow?
    for i in range(0, length):
      if i % 2 == start:
        token += cons[randrange(21)]
      else:
        token += vows[randrange(5)]
    return token

class AuthProtocol(ServerProtocol):
    def store_token(self, uuid):
        """
        gets a new token using `generate_token`
        and sends it to the website
        returns the token or None if the request failed
        """
        token = generate_token(10)
        req = urllib2.Request(
            # URL
            environ.get("WEBSITE_URI"),
            # data
            "uuid=%s&token=%s" % (uuid, token),
            # headers
            {
              "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0", # fuck you too, CloudFlare
              "X-Auth-Server-Key": environ.get("WEBSITE_AUTH_KEY")
            }
        )
        try:
            response = urllib2.urlopen(req).read()
            if jsondecode(response) == {"success": True, "errors": {}}:
                self.logger.info("%s registered token %s" % (uuid, token))
                return token
            else:
                raise urllib2.URLError(response)
        except urllib2.URLError, e:
            self.logger.error(e)
            return None


    def player_joined(self):
        # This method gets called when a player successfully joins the server.
        #   If we're in online mode (the default), this means auth with the
        #   session server was successful and the user definitely owns the
        #   username they claim to.

        # Call super. This switches us to "play" mode, marks the player as
        #   in-game, and does some logging.
        ServerProtocol.player_joined(self)

        # Define your own logic here. It could be an HTTP request to an API,
        #   or perhaps an update to a database table.
        username = self.username
        ip_addr  = self.recv_addr.host
        uuid     = str(self.uuid).replace('-', '')
        self.logger.info("[%s (%s) authed with IP %s]" % (username, uuid, ip_addr))

        color_sign = u"\u00A7" # section sign, used for color codes in MC
        token = self.store_token(uuid)
        # Kick the player
        if token:
            self.close(("Thanks &a" + username + "&r, your token is &6" + token).replace("&", color_sign))
        else:
            self.close("&4Error! Please try again later, sorry.".replace("&", color_sign))

class AuthFactory(ServerFactory):
    protocol = AuthProtocol


def main(args):
    # Parse options
    import optparse
    parser = optparse.OptionParser(
        usage="usage: %prog server_auth "
              "[options]")
    parser.add_option("-a", "--host",
                      dest="host", default="0.0.0.0",
                      help="address to listen on")
    parser.add_option("-p", "--port",
                      dest="port", default="25565", type="int",
                      help="port to listen on")
    (options, args) = parser.parse_args(args)

    # Create factory
    factory = AuthFactory()
    factory.motd = "Authentication Server"
    with open("server_icon.png", "rb") as image_file:
      factory.favicon = "data:image/png;base64,%s" % (b64encode(image_file.read()))

    # Listen
    port = int(environ.get('RUPPELLS_SOCKETS_LOCAL_PORT') or options.port)
    factory.listen(options.host, port)
    print("Auth server listening on %s:%s" % (options.host, port))
    factory.run()