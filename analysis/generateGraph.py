# This module is used to generate the graph from the provided Nodes CSV file exported from Gephi
# Values include:
# id, name, genre, followers, component-number, degree, wDegree (weighted degree), ecc (eccentricity), closeness, hcloseness (harmonic closeness), between (betweeness) and eig (eigenvector centrality  

import csv

# Node class for node objects to be imported from Gephi (after data analysis) 
class Node:
	# Constructor for initializing node 
	def __init__(self, id, name, genre, followers, componentnumber, degree, wDegree, ecc, closeness, hcloseness, between, eig):
		self.id = id
		self.genre = genre
		self.name = name
		self.followers = int(followers)
		self.links = []
		self.componentnumber = int(componentnumber)
		self.degree = float(degree)
		self.wDegree = float(wDegree)
		self.ecc = float(ecc)
		self.closeness = float(closeness)
		self.hcloseness = float(hcloseness)
		self.between = float(between)
		self.eig = float(eig)
		
		
	# Connect a node to another node via edge 
	def addLink(self, target, weight):
		self.links.append((target, weight))
	
# Generate Graph from csv files nodestats.csv (exported from Gephi) and final_edges.csv
# Returns dictionary of node accessed by their id as key 
def generateGraph():	
	
	# Opening csv files to read 
	nodesFile = open("files/nodestats.csv", "r")
	edgesFile = open("files/final_edges.csv", "r")
	nodeReader= csv.reader(nodesFile)
	edgeReader = csv.reader(edgesFile)
	nodes = []
	edges = []
	map = {}

	# map out nodes 
	first = True
	for node in nodeReader:
		if first:
			first = False
			continue
		n = Node(node[0], node[3], node[4], node[5], node[6], node[7], node[8], node[9], node[10], node[11], node[12], node[13])
		map[node[0]] = n
	nodesFile.close()
	
	# map out edges
	first = True
	for edge in edgeReader:
		if first:
			first = False
			continue
		source = edge[0]
		target = edge[1]
		weight = edge[2]
		map[source].addLink(target, int(weight))
		map[target].addLink(source, int(weight))
	edgesFile.close()
	
	# return dictionary 
	return map
