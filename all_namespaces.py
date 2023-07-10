from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import NamespaceManager
import pandas as pd
import subprocess
import urllib.request
import os.path

df_all = pd.read_csv("output1_mse.csv")
df_robot = pd.read_csv("output.csv")

onts_robot = []
for index, row in df_robot.iterrows():
    ont_list = [nspace.lower().strip() for nspace in df_robot['namespace'][index].split(',')]
    onts_robot.extend(ont_list)        

for index, row in df_all.iterrows():
    url = df_all['mirror_from'][index]
    namespace = df_all['namespace'][index]
    filename = 'all_files/' + df_all['namespace'][index] + '.' + df_all['mirror_from'][index][-3:]
    
    # create a rdflib Graph object and parse the ontology file
    g = Graph()
    try:
        if df_all['mirror_from'][index][-3:] == 'owl':
            g.parse(filename, format="application/rdf+xml")
        else:
            g.parse(filename, format="ttl")
    except:
        continue


    # Get all the namespace prefixes used in the file
    prefixes = [str(ns[1]) for ns in g.namespaces()]
    prefixes_ns = [str(ns[0]) for ns in g.namespaces() if not ns[0].startswith(('ns', 'rdf', 'rdfs', 'owl', 'xsd'))]
    #prefixes_ns = [str(ns[0]) for ns in g.namespaces() if isinstance(ns[0], str) and not ns[0].startswith('ns')]
    ns_mgr = NamespaceManager(g)
    # Get all the URIs in the file
    uris = set()
    for triple in g:
        for term in triple:
            if isinstance(term, URIRef):
                uris.add(str(term))

    # Check which URIs are not in the namespace prefixes
    unrecognized_uris = []
    for uri in uris:
        if not any(uri.startswith(prefix) for prefix in prefixes) or not any(uri.startswith(prefix[:-1]) for prefix in prefixes) or not any(uri.startswith(prefix) for prefix in prefixes_ns):
            try:
                if ns_mgr.compute_qname(uri)[0] not in prefixes_ns and not ns_mgr.compute_qname(uri)[0].startswith('ns'):
                    uri_ref = str(ns_mgr.compute_qname(uri)[0])
                elif ns_mgr.compute_qname(uri)[1] not in prefixes:
                    uri_ref = str(ns_mgr.compute_qname(uri)[1])
            except:
                uri_ref = uri
            if uri_ref not in unrecognized_uris and uri_ref not in prefixes+prefixes_ns+['https://', 'http://', 'owl', 'rdf', 'rdfs', 'xsd', 'http://www.w3.org/ns/']:
                unrecognized_uris.append(uri_ref)
                #dict[ontology_name].append(uri_ref)
    new_data = ''
    new_data = ', '.join(unrecognized_uris)# + prefixes_ns)
    df_all.at[index, 'all_namespaces'] = new_data

df_all[['namespace', 'all_namespaces']].to_csv("all_namespaces_mse.csv")