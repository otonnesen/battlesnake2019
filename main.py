#!/home/ec2-user/.local/share/virtualenvs/battlesnake-vCwZ-LYW/bin/python3
# This is a hack. Oh well.

import json
import os
import bottle

from api import ping_response, start_response, move_response, end_response
from ai import logic

@bottle.post('/ping')
def ping():
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json
    #color = "#f1f1f1"
    color = "#ff0000"
    return start_response(color)

@bottle.post('/move')
def move():
    data = bottle.request.json
    direction = logic(data)
    return move_response(direction)

@bottle.post('/end')
def end():
    data = bottle.request.json
    return end_response()

application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '80'),
        debug=os.getenv('DEBUG', True)
    )
