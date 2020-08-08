# Import libraries
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
import json.decoder

# Get the username from terminal
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

os.environ["SPOTIPY_CLIENT_ID"]='bfa0f831f2224d2b988ff0807a7cc304'
os.environ["SPOTIPY_CLIENT_SECRET"]='7506bc6293b943b7963b255dd40f3f4b'
os.environ["SPOTIPY_REDIRECT_URI"]='https://www.google.de/'

# Erase cache and ask user for permission
try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f.cache-{username})
    token = util.prompt_for_user_token(username, scope)
    
# Create Spotify object
spotifyObject = spotipy.Spotify(auth=token)

# Display device from which song is played
devices = spotifyObject.devices()
print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id']

# Get track information
track = spotifyObject.current_user_playing_track()
print(json.dumps(track, sort_keys=True, indent=4))
print()
artist = track['item']['artists'][0]['name']
track = track['item']['name']

if artist !="":
    print("Currently playing " + artist + " - " + track)
    
# User information
user = spotifyObject.current_user()
displayName = user['display_name']
follower = user['followers']['total']

# BIS HIER FUNKTIONIERT

# Loop that prints options how to use the script
while True:
    print()
    print(">>> Welcome to Spotify " + displayName + " :)")
    print(">>> You have " + str(follower) + " followers.")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    choice = input("Enter your choice: ")
    
    # Search for artist
    if choice == 0:
        print()
        searchQuery = input("Ok, what's their name?:")
        print()
        
        # Get search results
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")
        
        # Print artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']
        
        # Album details
        trackURIs = []
        trackArt = []
        z = 0
        
        # Extract data from album
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM: " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()
            
        # See album art
        while True:
            songSelection = input("Enter a song number to see the album art: ")
            if songSelection == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIs[int(songSelection)])
            spotifyObject.start_playback(deviceID, None, trackSelectionList)
            webbrowser.open(trackArt[int(songSelection)])
        
    # End program
    if choice == 1:
        break
