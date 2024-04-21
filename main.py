from utils import Graph
import numpy as np
import os
from tqdm import tqdm
import joblib

Graphs = {}
names = os.listdir('supplementary_data')

print("reading graphs...")
for name in tqdm(names):
    G = Graph()
    G.read_from_ordered_file(f'supplementary_data/{name}')
    Graphs[name] = G
    
# do the test
test_results = {}
ws = list(range(2, 301))

i = 1
for name in names:
    G = Graphs[name]
    test_results[name] = {"test_values": [], "sizes": []}
    print(f"doing test for {name} with size {len(G.adj)} ({i}/{len(names)})")
    i += 1
    for w in tqdm(ws):
        result, H = G.do_test(w0=w, return_H=True)
        test_results[name]["test_values"].append(result)
        test_results[name]["sizes"].append(len(H))
        
joblib.dump(test_results, 'results/results.pkl')