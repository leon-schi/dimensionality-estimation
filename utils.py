import numpy as np

def to_int(x):
    try:
        return int(x)
    except: return 0

class Graph:
    def __init__(self):
        self.adj = {}
        
    # reads from a file in real_world_zenodo/edge_lists_real and uses the maximum node index + 1 as number of nodes
    def read_from_ordered_file(self, file, sep=' '):
        n = 0
        with open(file, 'r') as f:
            for line in f:
                a, b = [to_int(x) for x in line.split(sep)][:2]
                if max(a,b) + 1 > n:
                    n = max(a,b) + 1
        
        self.read(file, sep=sep, n=n) 
    
    def read(self, file, sep=' ', n=None):
        with open(file, 'r') as f:
            for line in f:
                if line[0] == '%' or line[0] == '#': continue
                if n is None:
                    n = [int(x) for x in line.split(sep)][0] + 1
                    f.readline()
                self.adj = {i: [] for i in range(n)}
                for line in f:
                    a, b = [to_int(x) for x in line.split(sep)][:2]
                    self.adj[a].append(b)
                    self.adj[b].append(a)
                    
    def write_ordered(self, filename):
        node_ids = [x for x in self.adj.keys() if len(self.adj[x]) > 0]
        node_id_to_index = {}
        for i, x in enumerate(node_ids):
            node_id_to_index[x] = i
        node_ids = sorted(node_ids)
        with open(filename, 'w') as f:
            for uid in node_ids:
                for vid in self.adj[uid]:
                    f.write(f'{node_id_to_index[uid]} {node_id_to_index[vid]}\n')
    
    def get_degrees(self):
        return np.array([len(l) for l in self.adj.values()])
    
    def get_degree_mode(self):
        degrees = self.get_degrees()
        values, counts = np.unique(degrees, return_counts=True)
        return values[np.argmax(counts[1:]) + 1]
    
    def do_test(self, c=1.33, w0=None, return_H=False):
        degrees = self.get_degrees()
        values, counts = np.unique(degrees, return_counts=True)

        # find interesting vertices as those that have degree [w0, c*cw0] and at least two neighbors with degree in the same range 
        if w0 is None: w0 = values[np.argmax(counts[2:]) + 2]
        def degree_in_range(v):
            return degrees[v] >= w0 and degrees[v] <= c*w0

        H = {}
        for v in range(len(self.adj)):
            if degree_in_range(v):
                interesting_neighbors = [u for u in self.adj[v] if degree_in_range(u)]
                if len(interesting_neighbors) > 1:
                    H[v] = interesting_neighbors

        #compute clustering in the induced graph H of the interesting vertices
        def clustering(v):
            hashtag, total = 0, 0
            for i, s in enumerate(H[v]):
                for t in H[v][i+1:]:
                    total+=1
                    if t in self.adj[s]: hashtag+=1
            return hashtag/total

        result = np.mean([clustering(v) for v in H.keys()])
        if return_H: return result, H
        else: return result
    
    def total_clustering(self):
        def clustering(v):
            hashtag, total = 0, 0
            for i, s in enumerate(self.adj[v]):
                for t in self.adj[v][i+1:]:
                    total+=1
                    if t in self.adj[s]: hashtag+=1
            if total <= 0: return 0
            return hashtag/total
        return np.mean([clustering(v) for v in self.adj.keys()])