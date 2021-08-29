# Course: CS261 - Data Structures
# Author: Xiuzhu Shao
# Assignment: Assignment 6, Part 2
# Description: Implementation of directed graph class, including Dijkstra's algorithm. Utilizes skeleton code
# provided by the course as well as pseudocode from the course. Utilizes the wikipedia article on topological
# sorting "https://en.wikipedia.org/wiki/Topological_sorting" to implement cycle detection.

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a vertex to the graph and returns an integer representing the
        number of vertices in the graph.
        """
        # Creates list of zeros representing the new vertex's connection to
        # the other vertices in the graph.
        vertex_list = [0] * (self.v_count + 1)

        # Increments v_count for new vertex
        self.v_count += 1

        # Adds 0 to each existing list in the graph, representing the connection
        # to the new vertex.
        for val in self.adj_matrix:
            val.append(0)

        # Adds the list representing new vertex to the graph.
        self.adj_matrix.append(vertex_list)
        return self.v_count


    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Takes in two integers representing vertices "src" and "dst", as
        well as an integer weight. Adds an edge from "src" to "dst"
        with the given weight. If one or both vertices do not exist, if
        weight is not positive, or if "src" and "dst" refers to the same
        vertex, this method does nothing. If the edge already exists in the
        graph, updates its weight.
        """

        # One or both vertices do not exist, return immediately.
        if src < 0 or src > self.v_count - 1 or dst < 0 or dst > self.v_count - 1:
            return

        # Invalid weight, return immediately.
        if weight < 1:
            return

        # Vertices are the same, do nothing
        if src == dst:
            return

        # Adds edge between vertices
        self.adj_matrix[src][dst] = weight



    def remove_edge(self, src: int, dst: int) -> None:
        """
        Takes in two integers representing vertices "src" and "dst".
        Removes the edge from "src" to "dst". If one or both vertices do not exist
        or if there is no edge between them , the method does nothing.
        """

        # One or both vertices do not exist, return immediately.
        if src < 0 or src > self.v_count - 1 or dst < 0 or dst > self.v_count - 1:
            return

        # Vertices are the same, do nothing
        if src == dst:
            return

        # Deletes edge between vertices, if edge exists
        self.adj_matrix[src][dst] = 0


    def get_vertices(self) -> []:
        """
        Returns a list containing the vertices in the graph.
        """
        vertex_list = []
        for vertex in range(self.v_count):
            vertex_list.append(vertex)

        return vertex_list


    def get_edges(self) -> []:
        """
        Returns a list of the edges in the graph. Each edge is
        represented as a tuple of two incident vertex indices and weight.
        Tuple representation: (source vertex, destination vertex, weight).
        """
        return_list = []
        for row in range(self.v_count):
            for column in range(self.v_count):
                if self.adj_matrix[row][column] != 0:
                    return_list.append((row,column,self.adj_matrix[row][column]))
        return return_list

    def is_valid_path(self, path: []) -> bool:
        """
        Takes in a list of integer vertices. Returns True if the list
        represents a valid path in the graph, and False otherwise. A
        valid path is defined as being able to travel from the first vertex
        in the list to the last vertex in the list, at each step traversing over
        an edge in the graph. And empty path is considered valid.
        """
        # Empty path, returns True.
        if path == []:
            return True

        # Iterates through the list "path". If any any point there is not
        # a weighted edge from current index in path to the next index in path,
        # returns False immediately. Returns True if iteration successfully completes.
        for num in range(len(path) - 1):
            index = path[num]
            next_index = path[num + 1]
            if self.adj_matrix[index][next_index] == 0:
                return False
        return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Takes in a required parameter v_start which is an integer that
        represents the starting vertex of the search.
        Performs a depth-first search (DFS) in the graph and returns
        a list of vertices visited during the search, in order visited.
        User can input optional parameter v_end to stipulate the 'end'
        vertex that will stop the search once it is reached.
        If starting vertex does not exist in the graph, returns empty list.
        If end vertex does not exist in the graph, search is performed as
        though no end vertex input was provided.
        When multiple vertices are available for traversal during the search,
        vertices will be traversed in ascending order.
        """

        # If starting vertex is not in graph, returns empty list.
        if v_start < 0 or v_start > self.v_count - 1:
            return []

        # If a non-existent ending vertex is provided, ignores it.
        if v_end and (v_end < 0 or v_end > self.v_count - 1):
            v_end = None

        # Initializes list for storing visited vertices, and to_visit
        # stack for storing vertices not yet visited.
        visited = []
        to_visit = deque()
        to_visit.append(v_start)

        # While stack is not empty (aka v_end has not been reached, if
        # it is defined, and there are still vertices to traverse):
        while to_visit:
            # Pops current vertex off of top of stack. If it is v_end,
            # and v_end has been provided by the user as a valid vertex,
            # returns visited list immediately.
            curr_vertex = to_visit.pop()
            if v_end and curr_vertex == v_end:
                visited.append(curr_vertex)
                return visited
            # If current vertex has been previously traversed, immediately
            # continues on to popping the next vertex off of the stack.
            if curr_vertex not in visited:
                visited.append(curr_vertex)
            else:
                continue
            # Stores vertices adjacent to current vertex in a new list, in
            # reverse alphabetical order.
            curr_vertex_list = []
            curr_row = self.adj_matrix[curr_vertex]
            for column in range(len(curr_row)):
                if curr_row[column] != 0:
                    curr_vertex_list.append(column)
            curr_vertex_list.sort(reverse = True)
            # Adds vertices in the sorted vertices list to the top of the stack.
            # This way, vertices are put onto the stack in descending lexicographical
            # order such that the lowest value vertex is at the top of the stack.
            for value in curr_vertex_list:
                to_visit.append(value)
        return visited


    def bfs(self, v_start, v_end=None) -> []:
        """
        Takes in a required parameter v_start which is an integer that
        represents the starting vertex of the search.
        Performs a breadth-first search (BFS) in the graph and returns
        a list of vertices visited during the search, in order visited.
        User can input optional parameter v_end to stipulate the 'end'
        vertex that will stop the search once it is reached.
        If starting vertex does not exist in the graph, returns empty list.
        If end vertex does not exist in the graph, search is performed as
        though no end vertex input was provided.
        When multiple vertices are available for traversal during the search,
        vertices will be traversed in ascending order.
        """

        # If starting vertex is not in graph, returns empty list.
        if v_start < 0 or v_start > self.v_count - 1:
            return []

        # If a non-existent ending vertex is provided, ignores it.
        if v_end and (v_end <0 or v_end > self.v_count - 1):
            v_end = None

        # Initializes list for storing visited vertices, and to_visit
        # queue for storing vertices not yet visited.
        visited = []
        to_visit = deque()
        to_visit.append(v_start)

        # While stack is not empty (aka v_end has not been reached, if
        # it is defined, and there are still vertices to traverse):
        while to_visit:
            # Pops current vertex off of left end of queue. If it is v_end,
            # and v_end has been provided by the user as a valid vertex,
            # returns visited list immediately.
            curr_vertex = to_visit.popleft()
            if v_end and curr_vertex == v_end:
                visited.append(curr_vertex)
                return visited
            # If current vertex has been previously traversed, immediately
            # continues on to popping the next vertex off of the stack.
            if curr_vertex not in visited:
                visited.append(curr_vertex)
            else:
                continue
            # Stores vertices adjacent to current vertex in a new list, in
            # reverse alphabetical order.
            curr_vertex_list = []
            curr_row = self.adj_matrix[curr_vertex]
            for column in range(len(curr_row)):
                if curr_row[column] != 0:
                    curr_vertex_list.append(column)
            curr_vertex_list.sort()
            # Adds vertices in the sorted vertices list to the right end of the queue.
            # This way, vertices are put into the queue in ascending lexicographical
            # order such that the lowest value vertex towards the left of the queue.
            for value in curr_vertex_list:
                to_visit.append(value)
        return visited

    def has_cycle(self) -> bool:
        """
        Takes no input and returns True if the graph contains at least one
        cycle, and False otherwise.
        Utilizes Kahn's Algorithm.
        """

        # Finds all edges and all vertices in graph
        all_edges = self.get_edges()
        all_vertices = self.get_vertices()

        # Initializes and populates a list containing
        # the number of degrees (vertices pointing to this
        # vertex) for all vertices.
        degree_list = [0] * len(all_vertices)
        for edge in all_edges:
            degree_list[edge[1]] += 1

        # Initializes a queue for traversing vertices with
        # 0 degree. Iterates through degree_list and appends
        # all vertices with 0 degrees to the queue.
        no_dependency_queue = deque()
        for val in range(len(degree_list)):
            if degree_list[val] == 0:
                no_dependency_queue.append(val)

        # While queue is not empty, pop vertex from left of queue.
        # For each destination vertex that this vertex points to,
        # subtract 1 from the degree of the destination vertex. If
        # the destination vertex now has 0 degrees, appends it to the
        # queue. Continues until no more vertices are left in the queue.
        # At this point, any vertex with a degree > 0 is in a cycle, where
        # in order to remove vertex A, vertex B must be removed, but vertex B
        # points to vertex A.
        while no_dependency_queue:
            curr_vertex = no_dependency_queue.popleft()
            for edge in all_edges:
                if edge[0] == curr_vertex:
                    degree_list[edge[1]] -= 1
                    if degree_list[edge[1]] == 0:
                        no_dependency_queue.append(edge[1])
        # If any vertex has a degree > 0 , cycle exists, returns True
        for val in range(len(degree_list)):
            if degree_list[val] != 0:
                return True
        return False


    def dijkstra(self, src: int) -> []:
        """
        Takes in an integer "src" representing the starting vertex, and
        returns a list with one value per each vertex in the graph, where
        the value at index 0 is the length of the shortest path from vertex
        src to vertex 0, vertex 1, etc...
        If a vertex is not reached from src, the return value is INFINITY.
        Note that src is assumed to be a valid index.
        """
        # Dictionary to store visited vertices. Stored in the key/value form
        # vertex/distance
        visited = dict()

        # Creates minheap priority queue. Push tuple (src,distance) onto queue
        # where distance = 0.
        to_visit = []
        heapq.heappush(to_visit,(src,0))

        # While queue is not empty, pop vertex and distance pair off of queue.
        while to_visit:
            curr = heapq.heappop(to_visit)
            vertex = curr[0]
            distance = curr[1]

            # If vertex has not yet been visited, or if a shorter distance
            # from src to vertex has been found, replace distance value in
            # dictionary with new shorter distance.
            if vertex not in visited or visited[vertex] > distance:
                visited[vertex] = distance
                # For each adjacent vertex, push the adjacent vertex and the
                # distance from src to adjacent vertex onto queue.
                for col in range(self.v_count):
                    di = self.adj_matrix[vertex][col]
                    if 0 < di:
                        heapq.heappush(to_visit, (col, di + distance))

        # Initializes a return list representing all vertices in the graph and fill
        # with infinity. Traverse visited dictionary and fill return list with the
        # shortest distance from src to each vertex. Each index in return list will represent a
        # vertex, and the value at the index will represent the shortest path from src
        # to the index.
        return_list = [float('inf')] * self.v_count
        for vertex in visited:
            return_list[vertex] = visited[vertex]
        return return_list



if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0, 99)]
    for src, dst, *weight in edges_to_add:
        g.add_edge(src, dst, *weight)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
