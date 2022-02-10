import asyncio
import json
import logging
import pickle

from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

peer = None


def set_peer(peer_received):
    global peer
    peer = peer_received


@app.route('/entities', methods=["GET"])
def entities():
    global peer
    if not peer:
        return json.dumps([])
    
    toFollow = []
    for neighbour in peer.neighbours:
        toFollow.append(neighbour.to_dict())
    
    followers = []
    for follower in peer.followers:
        followers.append(follower.to_dict())
    
    followings = []
    for following in peer.followings:
        followings.append(following.to_dict())
    
    return json.dumps([followers, followings, toFollow])


@app.route('/timeline', methods=['GET'])
def fetch_timelines():
    if not peer:
        return json.dumps([])

    to_json_list = []

    for key in peer.timelines.keys():
        if len(peer.timelines[key].list_tweets) > 0:
            to_json_list.append(peer.timelines[key].to_dict())

    return json.dumps(to_json_list)


@app.route('/subscribe', methods=["POST"])
async def subscribe():  # put application's code here
    await peer.subscribe(request.get_json())
    return Response(status=200)


@app.route('/unsubscribe', methods=["POST"])
async def unsubscribe():  # put application's code here
    await peer.unsubscribe(request.get_json())
    return Response(status=200)


@app.route('/tweet', methods=["POST"])
async def tweet():  # put application's code here
    await peer.tweet(request.get_json())
    return Response(status=200)


@app.route('/logout', methods=["POST"])
def logout():
    peer.logout()
    return Response(status=200)
