#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description: Takes an item rating_key and assigns the "Other" label to it.
Author:    /u/DaTurkeyslayer
Requires:   plexapi
Usage:
  python add_label_recently_added.py --rating_key 1234 --label "Label" --names John,Jane,Alice

Tautulli script trigger:
  * Notify on recently added
Tautulli script conditions:
  * Filter which media to add labels to using conditions. Examples:
    [ Media Type | is | movie ]
    [ Show Name | is | Game of Thrones ]
    [ Album Name | is | Reputation ]
    [ Video Resolution | is | 4k ]
    [ Genre | contains | horror ]
Tautulli script arguments:
  * Recently Added:
    --rating_key {rating_key} --namesList John,Jane,Alice
'''

import argparse
import os
import plexapi
from plexapi.server import PlexServer

# ## OVERRIDES - ONLY EDIT IF RUNNING SCRIPT WITHOUT TAUTULLI ##

PLEX_URL = ''
PLEX_TOKEN = ''

# Environmental Variables
PLEX_URL = PLEX_URL or os.getenv('PLEX_URL', PLEX_URL)
PLEX_TOKEN = PLEX_TOKEN or os.getenv('PLEX_TOKEN', PLEX_TOKEN)

def add_label_Other(plex, rating_key):
    item = plex.fetchItem(rating_key)

    if item.type in ('movie', 'show', 'album'):
        mediaRecord = item
    elif item.type in ('season', 'episode'):
        mediaRecord = item.show()
    elif item.type == 'track':
        mediaRecord = item.album()
    else:
        print(f"Cannot add label to '{item.title}' ({item.ratingKey}): Invalid media type '{item.type}'")
        return


    mediaRecord.addLabel('Other')
    
    print(f"Adding label 'Other' to '{mediaRecord.title}' ({mediaRecord.ratingKey})")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rating_key', required=True, type=int)
    opts = parser.parse_args()

    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    add_label_parent(plex, **vars(opts))
