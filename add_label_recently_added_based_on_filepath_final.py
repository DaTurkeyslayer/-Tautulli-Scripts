#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description: Automatically add a label to recently added items in 
                your Plex library, based on a list of names and if the 
                media's filepath contains one of those names an assigns the label dynamically.
Author:    /u/SwiftPanda16 + DaTurkeyslayer
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

def add_label_parent(plex, rating_key, names):
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

    # Get the filepath and extract names
    filepath = item.locations[0].path if item.locations else None
    
    # Loop through each name to check if it is in the filepath
    for name in names:
        # Check if the name is in the filepath
        if name.lower() in filepath.lower():
            # Use the found name to dynamically assign the label
            dynamic_label = name + "'s"
            
            # Check if the label already exists
            existing_labels = [label.tag for label in mediaRecord.labels]
            
            if dynamic_label not in existing_labels:
                # Create the label if it doesn't exist
                mediaRecord.addLabel(dynamic_label)
                print(f"Adding label '{dynamic_label}' to '{mediaRecord.title}' ({mediaRecord.ratingKey})")
            break  # Exit the loop after the first match
    else:
        print(f"No matching names found in the filepath for '{mediaRecord.title}' ({mediaRecord.ratingKey})")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rating_key', required=True, type=int)
    parser.add_argument('--namesList', type=str, required=True, help='Comma-separated list of names')
    opts = parser.parse_args()

    # Parse comma-separated names
    names = [name.strip() for name in opts.namesList.split(',')] if opts.namesList else []

    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    add_label_parent(plex, **vars(opts))
