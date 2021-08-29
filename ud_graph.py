# Course: CS 261
# Author: Xiuzhu Shao
# Assignment: Assignment 6, Part 1
# Description: Implementation of undirected graph class. Utilizes skeleton code
# provided by the course as well as pseudocode from the course.

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Takes in a string "v" representing a vertex
        and adds it to the graph. If the vertex already
        exists, does nothing.
        """
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Takes in two strings "u" and "v" representing two
        vertices and creates a edge between them. If either or
        both of the vertices do not yet exist in the graph, add
        the vertex/vertices and then create the edge. If an edge
        already exists in the graph, or if "u" and "v" refer to the
        same vertex, does nothing.
        """
        if u == v: # If two vertices are the same, do nothing.
            return

        # If either/both vertices do not yet exist, add them
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        # If an edge already exists between the two vertices, do nothing
        # and return.
        if u in self.adj_list[v]:
            return

        # Adds edge between u and v by adding the vertices to each other's
        # lists in the dictionary.
        u_vertex = self.adj_list[u]
        v_vertex = self.adj_list[v]

        u_vertex.append(v)
        v_vertex.append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Takes in two strings "u" and "v" representing two
        vertices and removes the edge between them. If either
        or both vertices do not exist in the graph, or if there
        is not an edge between them, does nothing.
        """
        # If either or both vertices does not exist.
        if v not in self.adj_list or u not in self.adj_list:
            return

        # If no edge exists between them, does nothing.
        if u not in self.adj_list[v]:
            return

        # Removes edge
        u_vertex = self.adj_list[u]
        v_vertex = self.adj_list[v]

        u_vertex.remove(v)
        v_vertex.remove(u)


    def remove_vertex(self, v: str) -> None:
        """
        Takes in a string "v" representing a vertex. Removes
        this vertex and all edges incident to it from the graph.
        If the vertex does not exist, does nothing.
        """
        # If vertex does not exist, does nothing.
        if v not in self.adj_list:
            return

        # Removes vertex value from the list of each
        # adjacent vertex.
        removed_vertex = self.adj_list.pop(v)
        for other_vertex in removed_vertex:
            curr_vertex = self.adj_list[other_vertex]
            curr_vertex.remove(v)


    def get_vertices(self) -> []:
        """
        Returns a list containing the vertices in the graph. Note
        that the list is unordered.
        """
        # Empty list containing vertices.
        return_list = []

        # Iterates through dictionary and
        # adds vertex values to return list.
        for key in self.adj_list:
            return_list.append(key)
        return return_list
       

    def get_edges(self) -> []:
        """
        Returns a list containing the edges in the graph. Note
        that the list is unordered. Each edge is returned as
        a tuple of two incident vertex names. Note that the
        two vertices in each tuple are also unordered.
        """
        # Empty list containing edges.
        return_list = []
        # List containing vertices already traversed.
        no_go = []

        # Iterates through dictionary and
        # adds edges to the return list
        for key in self.adj_list:
            curr_list = self.adj_list[key]
            for value in curr_list:
                if value not in no_go:
                    return_list.append((key,value))
            no_go.append(key)
        return return_list

    def is_valid_path(self, path: []) -> bool:
        """
        Takes in a list "path" containing vertex names.
        Returns true if the sequence of vertices represents
        a valid path in the graph, and False otherwise. Note that
        a valid path is defined as being able to travel from the
        first vertex in the list to the last vertex, at each step
        traversing over an edge in the graph. An empty path is
        valid.
        """
        # Finds number of vertices in the path
        path_length = len(path)

        # If path is empty, it is valid.
        if path_length == 0:
            return True

        # Iterates through path to ensure all vertices
        # are valid.
        for key in path:
            if key not in self.adj_list:
                return False

        # Iterates through the path and finds the current
        # vertex as well as the next vertex.
        # Looks at the dictionary list stored under the current
        # vertex key. If next vertex is not in the list at
        # any point, returns False.
        for index in range(path_length - 1):
            curr_vertex, next_vertex = path[index], path[index + 1]
            if next_vertex not in self.adj_list[curr_vertex]:
                return False
        # All vertices in list have been examined and no False condition
        # has been triggered, return True.
        return True



    def dfs(self, v_start, v_end=None) -> []:
        """
        Takes in a required parameter v_start which is a string that
        represents the starting vertex of the search.
        Performs a depth-first search (DFS) in the graph and returns
        a list of vertices visited during the search, in alphabetical order.
        User can input optional parameter v_end to stipulate the 'end'
        vertex that will stop the search once it is reached.
        If starting vertex does not exist in the graph, returns empty list.
        If end vertex does not exist in the graph, search is performed as
        though no end vertex input was provided.
        When multiple vertices are available for traversal during the search,
        vertices will be traversed in ascending lexicographical order.
        """

        # If starting vertex is not in graph, returns empty list.
        if v_start not in self.adj_list:
            return []

        # If a non-existent ending vertex is provided, ignores it.
        if v_end and v_end not in self.adj_list:
            v_end = None

        # Initializes list for storing visited vertices, and to_visit
        # stack for storing vertices not yet visited.
        visited = []
        to_visit = deque(v_start)

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
            for value in self.adj_list[curr_vertex]:
                curr_vertex_list.append(value)
            curr_vertex_list.sort(reverse = True)
            # Adds vertices in the sorted vertices list to the top of the stack.
            # This way, vertices are put onto the stack in descending lexicographical
            # order such that the lowest value vertex is at the top of the stack.
            for value in curr_vertex_list:
                to_visit.append(value)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Takes in a required parameter v_start which is a string that
        represents the starting vertex of the search.
        Performs a breadth-first search (BFS) in the graph and returns
        a list of vertices visited during the search, in alphabetical order.
        User can input optional parameter v_end to stipulate the 'end'
        vertex that will stop the search once it is reached.
        If starting vertex does not exist in the graph, returns empty list.
        If end vertex does not exist in the graph, search is performed as
        though no end vertex input was provided.
        When multiple vertices are available for traversal during the search,
        vertices will be traversed in ascending lexicographical order.
        """

        # If starting vertex is not in graph, returns empty list.
        if v_start not in self.adj_list:
            return []

        # If a non-existent ending vertex is provided, ignores it.
        if v_end and v_end not in self.adj_list:
            v_end = None

        # Initializes list for storing visited vertices, and to_visit
        # queue for storing vertices not yet visited.
        visited = []
        to_visit = deque(v_start)

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
            for value in self.adj_list[curr_vertex]:
                curr_vertex_list.append(value)
            curr_vertex_list.sort()
            # Adds vertices in the sorted vertices list to the right end of the queue.
            # This way, vertices are put into the queue in ascending lexicographical
            # order such that the lowest value vertex towards the left of the queue.
            for value in curr_vertex_list:
                to_visit.append(value)
        return visited


    def count_connected_components(self) -> int:
        """
        Takes no input and returns an integer representing
        the number of connected components in the graph.
        """
        # If the graph has no vertices, return 0.
        if not self.adj_list:
            return 0

        # Initializes list containing all vertices in the
        # graph. Begins BFS. For each search conducted, increments
        # the number of components by 1 (components initializes at 0).
        # Removes the vertices traverses via BFS from the list of
        # all vertices and repeats until the all vertices list is empty.
        # Returns the number of components.
        all_vertices = self.get_vertices()
        num_components = 0
        while all_vertices != []:
            return_list = self.dfs(all_vertices[0])
            num_components += 1
            for vertex in return_list:
                if vertex in all_vertices:
                    all_vertices.remove(vertex)
        return num_components

    def has_cycle(self) -> bool:
        """
        Takes no input and returns True if the graph contains at least one
        cycle, and False otherwise.
        """
        # Initializes to_visit stack for storing vertices not yet visited.
        to_visit = deque()

        # A list to track all vertices in the graph.
        all_vertices = self.get_vertices()

        # Sets first_vertex to a random vertex in the graph and the first parent to None.
        first_vertex = all_vertices[0]
        parent = None

        # To_visit stack will contain parent/vertex pairs. The first item off the stack is
        # the parent, followed by the vertex.
        to_visit.append(first_vertex)
        to_visit.append(parent)

        # While stack is not empty and not all vertices have been visited:
        while to_visit or len(all_vertices) != 0:
            # If the stack is empty but there are still vertices not yet
            # visited (aka at least two sections of the graph are not connected
            # by an edge), take another random vertex from the all_vertices list
            # to populate the to_visit stack.
            if not to_visit:
                to_visit.append(all_vertices[0])
                to_visit.append(None)

            # Pops current parent/vertex pair off of top of stack.
            parent = to_visit.pop()
            curr_vertex = to_visit.pop()

            # Removes current vertex from the list of all vertices.
            if curr_vertex in all_vertices:
                all_vertices.remove(curr_vertex)

            # Initializes list curr_vertex_list to store all adjacent
            # vertices of the current vertex and sorts the list so it
            # is in descending order.
            curr_vertex_list = []
            for value in self.adj_list[curr_vertex]:
                curr_vertex_list.append(value)
            curr_vertex_list.sort(reverse=True)

            # Iterates through the adjacent vertices list. If any any point
            # we encounter an adjacent vertex "value" that has already been
            # visited and who is not the current vertex's parent,
            # we know that a cycle has been found. Returns True immediately.
            for value in curr_vertex_list:
                if value not in all_vertices:
                    if value != parent:
                        return True
                    else:
                        continue
                # No cycle found, append adjacent vertex and parent pair to
                # to_visit stack.
                else:
                    to_visit.append(value)
                    to_visit.append(curr_vertex)
        return False
   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
