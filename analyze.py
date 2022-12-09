# This module conducts least path analysis and outputs best paths to output file 


from generateGraph import *
import csv


# Generate graph 
map = generateGraph()

# Set up weights of eig influence, degree centrality influence and maximum path length
eig_influence = 0.5
central_influence = 0.5
max_path = 10

# Helper method that checks if element is in list 
def inList(elem, lis):
	for l in lis:
		if (elem in l) or (l in elem):
			return True
	return False

# Get target artest and starting collaborators 
def getLists():
	
	# Get top 100 artists based on number of followers, as well as their genres
	ids = list(map.keys())
	ids.sort(key=lambda id: map[id].followers, reverse=True)
	popular_artists = ids[0:100]
	genres = [map[id].genre for id in popular_artists]
	
	# Get starting artists by filtering out artists with more than 4000 followers
	# Then we get rank these by eigenvector centrality and betweenness (both have equal influence on ranking)
	starting_artists = list(ids)
	starting_artists = filter(lambda id: (map[id].followers <= 4000), starting_artists)
	starting_artists = list(starting_artists)
	starting_artists.sort(key=lambda id: (eig_influence*map[id].eig) + ((1-eig_influence)*map[id].between), reverse=True)
	starting_artists = list(starting_artists)
	
		# Then we filter out the artists in this list who do not belong to the genres of the top 100 artists
	starting_artists = filter(lambda id: inList(map[id].genre, genres), starting_artists)
	starting_artists = list(starting_artists)

	
	# Then we get top 50% of these artists as our starting collaborators 
	length = len(starting_artists)
	middle = length//2
	starting_artists = starting_artists[0:middle]
	
	# Return starting collaborators and target artists 
	return (starting_artists, popular_artists)
	
	
# Use dfs to generate all least paths (with a maximum size of 10) between each starting artist and any of the target artists
def getAllPaths(start, end):
	res = []
	hasVisited = {}
	for key in map:
		hasVisited[key] = False

	# Initialize stack 
	stack = [start]
	paths = [[start]]
	hasVisited[start] = True
	pathDicts = [hasVisited]
		
	# DFS traversal through graph 
	while stack:
		artist = stack.pop(-1)
		artist = map[artist]
		path = paths.pop(-1)
		pathDict = pathDicts.pop(-1)
		
		if (artist.id in end):
			res.append(path)
			continue
		
		if len(path) > max_path:
			continue
		
		# As traversing through graph, only visit artists who have not been visited as part of that path (to avoid cycles)
		# Only visit artists who have shared genre 
		children = artist.links
		for child in children:
			(target, weight) = child
			if (map[target].genre in artist.genre) or (artist.genre in map[target].genre):
				if (pathDict[target] == False):
					stack.append(target)
					newPath = list(path)
					newPath.append(target)
					paths.append(newPath)
					newPathDict = dict(pathDict)
					newPathDict[target] = True
					pathDicts.append(newPathDict)
	
	# Return paths 
	return res


# Helper method to score each path based on sum of inverse of each edge's weight 
def scorePath(path):
	score = 0.0
	for i in range(0, len(path)-1):
		result = [child[0] for child in map[path[i]].links].index(path[i+1])
		score += (1/float(map[path[i]].links[result][1]))
	return score

# Helper method to score each path based on sum of weighted degrees
def scoreCentrality(path):
	scoreCentral = 0.0
	for id in path:
		scoreCentral += map[id].wDegree
	return central_influence


def getPathStr(path):
	res = ""
	for i in range(0, len(path)):
		at = map[path[i]]
		res += 	at.name + "; " + str(at.followers)
		if (i < len(path)-1):
			res += 	" =======> " 
	return res
		

res = getLists()
(starts, ends) = res
allPaths = []
for start in starts:
	paths = getAllPaths(start, ends)
	for path in paths:
		allPaths.append(path)

# Sort paths based on highest sum of inverted edge weights
# Get bottom 50% of these paths
allPaths.sort(key=lambda path: scorePath(path), reverse=False)
length = len(allPaths)
middle = length//2
allPaths = allPaths[0:middle]

# Sort paths based on highest sum of weighted degrees
# Get top 50% of these paths
allPaths.sort(key=lambda path: scoreCentrality(path), reverse=True)
allPaths.pop(0)

# Create file to output best paths 
a = open("files/best_paths.csv", "w")
writer = csv.writer(a)
writer.writerow(["paths"])
for path in allPaths:
	writer.writerow(path)

a.close()

# Create file to output best path scores
b = open("best_paths_scores.csv", "w")
writer = csv.writer(b)
writer.writerow(["inverted weights score", "sum centralities score"])
for path in allPaths:
	writer.writerow([scorePath(path), scoreCentrality(path)])
b.close()











				
			
			
			
			
		

