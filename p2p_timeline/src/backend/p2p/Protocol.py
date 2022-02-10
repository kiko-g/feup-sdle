import random
from asyncio import sleep

from p2p.DHTEntry import DHTEntry
from p2p.Message import Message


async def gossiping(peer):
    while peer.alive:
        await gossiping_myself(peer)
        await gossiping_neighbours(peer)
        await gossiping_timelines(peer)
        await sleep(round(random.uniform(0, 1), 3))


async def gossiping_myself(peer):
    if not peer.time_counter.can_gossip_entity():
        return

    for neighbour in peer.neighbours:

        if neighbour in peer.zombies:
            continue

        try:
            peer.send_message(neighbour.host_ip, neighbour.data_port,
                              Message.create_ping_msg(peer.identifier, peer.username, peer.identifier, peer.host_ip,
                                                      peer.data_port))
            await sleep(0.1)
        except:
            peer.logger.print_neighbour_died(neighbour)
            peer.zombies.append(neighbour)

    for following in peer.followings:

        if following in peer.zombies:
            continue

        try:
            peer.send_message(following.host_ip, following.data_port,
                              Message.create_ping_msg(peer.identifier, peer.username, peer.identifier, peer.host_ip,
                                                      peer.data_port))
            await sleep(0.1)
        except:
            peer.logger.print_neighbour_died(following)
            peer.zombies.append(following)


async def gossiping_neighbours(peer):
    if not peer.time_counter.can_gossip_test():
        return

    if len(peer.neighbours) == 0:
        return

    for i in range(3):

        neighbour_destiny = random.choice(peer.neighbours)

        if neighbour_destiny in peer.zombies:
            continue

        neighbour_to_share = random.choice(peer.neighbours)

        if neighbour_destiny == neighbour_to_share:
            continue

        if neighbour_to_share in peer.zombies:
            continue
        try:
            peer.send_message(neighbour_destiny.host_ip, neighbour_destiny.data_port,
                              Message.create_share_entity_msg(peer.identifier,
                                                              neighbour_to_share.identifier,
                                                              neighbour_to_share.username,
                                                              neighbour_to_share.host_ip,
                                                              neighbour_to_share.data_port))
            await sleep(1)
        except:
            peer.logger.print_neighbour_died(neighbour_destiny)
            peer.zombies.append(neighbour_destiny)


async def gossiping_timelines(peer):
    if not peer.time_counter.can_gossip_timelines():
        return

    # No Data to Share
    if len(peer.timelines.keys()) == 1 and len(peer.timelines[peer.identifier].list_tweets) == 0:
        return

    for follower in peer.followers:

        for key in peer.timelines:

            # Dont send timelines to authors
            if key == follower.identifier:
                continue
            try:
                peer.send_message(follower.host_ip, follower.data_port,
                                  Message.create_timeline_msg(peer.identifier, peer.username, peer.timelines[key]))
            except:
                peer.logger.print_neighbour_died(follower)
                peer.zombies.append(follower)
