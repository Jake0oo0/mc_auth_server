from quarry.net.server import ServerFactory, ServerProtocol
from random import randrange
from postgres import Postgres
from os import environ
from time import strftime
from base64 import b64encode

###
### AUTH SERVER
###   ask mojang to authenticate the user
###

db = None
dburi = environ.get("WEBSITE_POSTGRES_URI")
if dburi:
  db = Postgres(dburi)

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
        token = generate_token(10)
        # Delete any eventual existing tokens
        self.logger.info(uuid)
        self.logger.info(type(uuid))
        if db:
          db.run("DELETE FROM registration_tokens WHERE CAST(uuid as text) = %(uuid)s", {"uuid": str(uuid.replace('-', ''))})
          db.run("INSERT INTO registration_tokens (uuid, token, created_at) VALUES (%(uuid)s, %(token)s, %(created_at)s)", {"uuid": str(uuid.replace('-', '')), "token": token, "created_at": strftime('%Y-%m-%d %H:%M:%S')})
        self.logger.info("%s registered token %s" % (uuid, token))
        return token


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
        uuid     = self.uuid
        self.logger.info("[%s (%s) authed with IP %s]" % (username, uuid, ip_addr))

        # Kick the player.
        color_sign = u"\u00A7"
        self.close("Thanks " + color_sign + "a" + username + color_sign + "r, your token is " + color_sign + "6" + self.store_token(uuid))


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
    factory.motd = "Sponge Authentication Server"
    with open("server_icon.png", "rb") as image_file:
      factory.favicon = "data:image/png;base64,%s" % (b64encode(image_file.read()))

    # Listen
    factory.listen(options.host, port = int(environ.get('RUPPELLS_SOCKETS_LOCAL_PORT') or options.port))
    factory.run()