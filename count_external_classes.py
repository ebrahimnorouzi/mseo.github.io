from rdflib import Graph
import pandas as pd
from rdflib import RDF, OWL
import pickle

df_all = pd.read_csv("output2_mse.csv")

dic_external = {}

for index, row in df_all.iterrows():
    url = df_all['mirror_from'][index]
    filename = 'all_files/' + df_all['namespace'][index] + '.' + df_all['mirror_from'][index][-3:]
    
    try:
        g = Graph()
        
        if df_all['mirror_from'][index][-3:] == 'owl' or df_all['namespace'][index] == 'EMMO_Datamodel':
            g.parse(filename, format="application/rdf+xml")
        else:
            g.parse(filename, format="ttl")
        
            
        ontology_namespace = None

        for s, p, o in g:
            if p == RDF.type and o == OWL.Ontology:
                ontology_namespace = str(s)
                break
        
        external_classes_count = 0

        for s, p, o in g.triples((None, RDF.type, OWL.Class)):
            if str(s).startswith(ontology_namespace):
                continue  # Skip classes within the ontology namespace
            external_classes_count += 1
        dic_external[df_all['namespace'][index]] = external_classes_count
    
    except:
        print(df_all['namespace'][index])
        

print(dic_external)
# Save the dictionary to a file
with open("dic_external.pkl", "wb") as f:
    pickle.dump(dic_external, f)
