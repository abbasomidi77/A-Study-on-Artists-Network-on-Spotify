import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv


# Helper method to check if element is in list, returns matching element from list
def inList(elem, tmps):
	for tmp in tmps:
		if (elem in tmp) or (tmp in elem):
			return tmp
	return None

# Use token to use Spotify's developer APIs
auth_manager = SpotifyClientCredentials('40cd9cd27c7c4689bc36774f5aac188b','10d3a4b01aea4976ac89c831db901a6d')
sp = spotipy.Spotify(auth_manager=auth_manager)

# Iterate through Spotify playlists and get their IDs 
playlists = sp.user_playlists('spotify')
playlist_ids = []
while playlists:
	for playlist in playlists['items']:
		playlist_ids.append(playlist['id'])
	if playlists['next']:
		playlists = sp.next(playlists)
	else:
		playlists = None


# Get all tracks in the playlists 		
tracklist = []
for playlist_id in playlist_ids:
	tracks = sp.playlist_tracks(playlist_id, limit = 100)
	tracklist.append(tracks['items'])
	while tracks['next']:
		tracks = sp.next(tracks)
		tracklist.append(tracks['items'])


# Get all artists of tracks which feature more than one artist 
trackstoAristsMap = {}

for listOfTracks in tracklist:
	for trackItem in listOfTracks:
		track = trackItem['track']
		if track is None:
			continue
		track_artists = track['artists']
		if len(track_artists) > 1:
			collect_artists = []
			for artist in track_artists:
				collect_artists.append(artist['id'])
			trackstoAristsMap[track['id']] = collect_artists


# Map out collaborations between artists 
collab_map = {}
for collab_artists in trackstoAristsMap.values():
	collab_artists.sort()
	for i in range(0, len(collab_artists)):
		for j in range(i+1, len(collab_artists)):
			if str(collab_artists[0] + ',' + collab_artists[1]) in collab_map:
				collab_map[str(collab_artists[0] + ',' + collab_artists[1])]+=1
			else:
				collab_map[str(collab_artists[0] + ',' + collab_artists[1])] = 1
			

# Node and edge generation 
covered_artist = {}
nodes_list = []
edge_list = []


# Get name, genres and number of followers per artist  for each node
# Create edge for  collaboration between artist pairs 
for artistpair in collab_map.keys():
	artistpair = artistpair.split(",")
	if artistpair[0] not in covered_artist:
		artist = sp.artist(artistpair[0])
		row = [artist['id'], artist['name'], artist['genres'], artist['followers']['total']]
		nodes_list.append(row)
		covered_artist[artistpair[0]] = True
	if artistpair[1] not in covered_artist:
		artist = sp.artist(artistpair[1])
		row = [artist['id'], artist['name'], artist['genres'], artist['followers']['total']]
		nodes_list.append(row)
		covered_artist[artistpair[1]] = True
	edgerow = [artistpair[0], artistpair[1], collab_map[",".join(artistpair)]]
	edge_list.append(edgerow)


# Preprocessing and cleaning of data

# Get occurrences of genre
genreOccurences = {}
for node  in nodes_list:
	genres = node[2]
	for genre in genres:
		if genre not in genreOccurences:
			genreOccurences[genre] = 0
		genreOccurences[genre] = genreOccurences[genre] + 1


# For each artist, assign dominant genre out of genres list, remove artists with no genres
# Remove artists who belong to a genre with less than 10 other artists in the network 
tmp = []
for node in nodes_list:
	genres = node[2]
	if len(genres) == 0:
		continue
	genres.sort(key=lambda genre: genreOccurences[genre], reverse=True)
	if genreOccurences[genres[0]] < 10:
		continue
	node[2] = genres[0]
	tmp.append(node)
nodes_list = tmp


# Combine subgenres into genres
tmp2 = []
for node in nodes_list:
	genre= node[2]
	genres = genre.split(" ")
	if len(genres) < 2:
		continue
	genres = filter(lambda genre: genre in genreOccurences,  genres)
	genres = list(genres)
	genres.sort(key= lambda genre: genreOccurences[genre], reverse=True)
	if len(genres) > 0:
		node[2] = genres[0]
	tmp2.append(node)
nodes_list = tmp2

topGenres = ["pop", "edm", "rap", "classical", "country", "rock", "jazz", "r&b", "soul", "punk", "funk"]

tmp3 = []
for node in nodes_list:
	genre = inList(node[2], topGenres)
	if genre is not None:
		node[2] = genre
	tmp3.append(node)
nodes_list = tmp3
	
# Output nodes and edges to csv files 			
nodes_file = open('analysis/files/final_nodes.csv.csv', 'w')
edges_file = open('analysis/files/final_edges.csv.csv', 'w')
nodes_writer = csv.writer(nodes_file)
edges_writer = csv.writer(edges_file)

nodes_writer.writerow(["id", "name", "genre", "followers"])
edges_writer.writerow(["source", "target", "weight"])

for node_row in nodes_list:
	nodes_writer.writerow(node_row)

	
for edge_row in edge_list:
	edges_writer.writerow(edge_row)
		

# Close files
nodes_file.close()
edges_file.close()







