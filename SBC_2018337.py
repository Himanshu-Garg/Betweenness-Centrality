#!/usr/bin/env python3

#name - himanshu garg
#roll no. - 2018337
#sec - B
#grp - 2

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "HIMANSHU GARG"
    email = "himanshu18337@iiitd.ac.in"
    roll_num = "2018337"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        self.validate()

    def validate(self):
        """
        Validates if Graph is valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to
            level : used to store min distance

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''
        
        level=0
        lis=[]                 											 #used to store final list containing all sublists level wise
        li=[]                  											 #used to form sub list
        done=[start_node]           							         #used to store the elements which we have visited
        update="n"

        for i in range(len(self.edges)):								#loop is used to add 1st level
            
            if start_node in self.edges[i]:
                update='y'
                index=self.edges[i].index(start_node)
                if index==0:
                    li.append(self.edges[i][1])
                else:
                    li.append(self.edges[i][0])
        if update == "y":
            level=level+1
            lis.append(li)
            done=done+li

            
        while end_node not in done:										#loop is used to add remaining levels and give the last level i.e min distance
            update="n"
            li=[]
            other= -1
            for i in lis[level-1]:
                for j in range(len(self.edges)):
                    other = -1
                    if i in self.edges[j]:
                        index=self.edges[j].index(i)
                        if index==0:
                            other=self.edges[j][1]
                        elif index==1:
                            other=self.edges[j][0]
                        
                    if other not in done:								#update done (elements which are visited are in done)
                        li.append(other)
                        update="y"
                        done.append(other)
            if update=="y":
               	level=level+1
               	lis.append(li)

        self.level=level
        return level 													#return min distance stored in level															



    def all_shortest_paths(self,start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        a=[[start_node]]												#store all the paths from 1 of max length = min_distance + 1
        min_dist=self.level
      
        for i in range(min_dist):
        	
        	for i in range(len(a)):
        		
        		last_digit=a[i][-1]										#used to store last digit of the list within list 'a'
        		for j in range(len(self.edges)):
	        		if last_digit in self.edges[j]:
	        			index=self.edges[j].index(last_digit)
	        			if index==0:
	        				other=self.edges[j][1]
	        			else:
	        				other=self.edges[j][0]
	        			a.append(a[i]+[other])
        b=[]															#used to store list having multiple lists each of length = min_distance + 1 but some have repeating nos
        B=[]
        for i in range(len(a)):
        	if len(a[i]) == min_dist+1:
        		b.append(a[i])

        for i in range(len(b)):
        	if b[i][-1]==end_node:
        		B.append(b[i])

        b=B
        	
        c=[]															#used to store final lists hsving paths of length = min_dist + 1
        for i in range(len(b)):
        	same="n" 													#tells whether a no. repeats in the list or not
        	for j in range(len(b[i])):
        		if b[i][j] in b[i][j+1:]:
        			same="y"
        	if same=="n":
        		c.append(b[i])

        return c


		


    def all_paths(self, start_node, end_node, all_path, num):
        """
        Finds all paths from node to destination with length = dist passing through num

        Args:
            start_node: Node to find path from
            end_node: Node to reach
            all_path: list having all the paths
            num: path having num or not

        Returns:
            List of path, where each path is list ending on destination and passing through num

            Returns 0 if there no paths
        """

        count=0															#used to store no of paths having num
        for i in range(len(all_path)):									#used to count no of paths having num
        	if num in all_path[i]:
        		count=count+1
        return count


    def betweenness_centrality(self):
        """
        Find betweenness centrality of the given node


        Returns:
            final dictionary having central betweeness of all the nodes
        """
        

        ans={}													#dictionary used to store central betweeness of each node
        from copy import deepcopy
        sum=0													#stores sum of all Y/X
        maxx=max(self.vertices)									#stores last vertex
        for i in range(1,maxx+1):
        	sum=0
        	vertices_copy=deepcopy(self.vertices)
        	for xyz in range(len(vertices_copy)):			#used to create a list without i
        		if vertices_copy[xyz]==i:
        			del vertices_copy[xyz]
        			break
        	
        	for j in vertices_copy:
        		for k in vertices_copy:
        			if k > j:
        				node_pair=[j,k] 								#used to give node pair at which we are
        				x=self.min_dist(j,k)
        				XYZ=self.all_shortest_paths(j,k)
        				X=len(XYZ)
        				Y=self.all_paths(j,k,XYZ,i)
        				sum=sum+(Y/X)
        	sum=sum/(((len(self.vertices)-1)*(len(self.vertices)-2))/2)
        	ans[i]=sum
        
        #print(ans)
        return ans




    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List of integer, denoting top k nodes based on betweenness
            centrality.
        """

        dict=self.betweenness_centrality()
        top=[]														#list having nodes with maximum central betweeness
        maxx=max(dict.values())										#maxx having maximum of central betweeness
        for i in dict.keys():										#loop to insert nodes in top having max central betweeness
        	if dict[i]==maxx:
        		top.append(int(i))
        return top


if __name__ == "__main__":
	
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (3, 6), (4, 5), (4, 6)]
    graph = Graph(vertices, edges)
    ans=graph.top_k_betweenness_centrality()
    print("nodes with max centrality are : ", ans)



