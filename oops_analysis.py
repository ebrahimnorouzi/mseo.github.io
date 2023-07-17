import pickle
import xml.etree.ElementTree as ET
import pandas as pd
import os

def find_entity(name):
    for fname in os.listdir('all_files'):
        print(fname)
        fpath='all_files/'+fname
        if not os.path.isfile(fpath):
            continue
        with open(fpath) as f:
            count=0
            for line in f:
                count+=1
                if '#'+name+"\">" in line:
                    return (fpath,count)

def get_affected_soma_iris(xml_elem):
    #print(xml_elem.findall('{http://www.oeg-upm.net/oops}Code'))
    #if len(xml_elem.findall('{http://www.oeg-upm.net/oops}Code'))>0:
    affects = xml_elem.findall('{http://www.oeg-upm.net/oops}NumberAffectedElements')
    #print(xml_elem.findall('{http://www.oeg-upm.net/oops}NumberAffectedElements'))
    #iris = list(map(lambda x: x.text,
    #    affects.findall('{http://www.oeg-upm.net/oops}AffectedElement')))
    return int(affects[0].text) #list(iris) #list(filter(lambda x: "all_files/periodictable.owl" in x, iris))

def get_resource_names(iris):
    return list(map(lambda x: x.split('#')[1],iris))

def report_pitfall(name,descr,level,iris):
    names = get_resource_names(iris)
    if level=="Important":
        msg_level="warning"
    elif level=="Minor":
        msg_level="warning"
    else:
        msg_level="debug"
    
    print("::"+msg_level+"::["+level+"]("+name+") "+descr)
    print("related iris:", iris)
    print()
    '''
    for name in names:
        needle = find_entity(name)
        if needle!=None:
            (path,line) = needle
            print("::"+msg_level+" file="+path+",line="+str(line)+"::["+level+"]("+name+") "+descr)
        else:
            print("::"+msg_level+" file=SOMA.owl::["+level+"]("+name+") "+descr)
    '''
    
def report_suggestion(name,descr,iris):
    #names = get_resource_names(iris)
    #msg = format_pitfall(name,descr,names)
    print("::info ::"+descr)

def run(xml_file):
    root = ET.parse(xml_file).getroot()
    
    pitfalls = {"Important": [], "Minor": [], "Critical": []}
    for pitfall_xml in root.findall('{http://www.oeg-upm.net/oops}Pitfall'):
        name  = pitfall_xml.findall('{http://www.oeg-upm.net/oops}Code')[0].text
        #descr = pitfall_xml.findall('{http://www.oeg-upm.net/oops}Description')[0].text
        level = pitfall_xml.findall('{http://www.oeg-upm.net/oops}Importance')[0].text
        #try:
        iris = get_affected_soma_iris(pitfall_xml)
        if iris>0:
            pitfalls[level].append((name,iris))
        #except:
            #continue
    
    '''
    print('number of Important pitfalls:', len(pitfalls["Important"]))
    #print('Number of Affected Elements :', pitfalls["Important"][0][0])
    for (name,descr,iris) in pitfalls["Important"]:
        print('Pitfall:', name, 'Number of Affected Elements: ', iris)
        #report_pitfall(name,descr,"Important",iris)
    
    print('number of Minor pitfalls:', len(pitfalls["Minor"]))
    for (name,descr,iris) in pitfalls["Minor"]:
        print('Pitfall:', name, 'Number of Affected Elements: ', iris)
        #report_pitfall(name,descr,"Minor",iris)
    
    print('number of Critical pitfalls:', len(pitfalls["Critical"]))
    for (name,descr,iris) in pitfalls["Critical"]:
        print('Pitfall:', name, 'Number of Affected Elements: ', iris)
        #report_pitfall(name,descr,"Critical",iris)
    
    for suggestion_xml in root.findall('{http://www.oeg-upm.net/oops}Suggestion'):
        name  = suggestion_xml.findall('{http://www.oeg-upm.net/oops}Name')[0].text
        descr = suggestion_xml.findall('{http://www.oeg-upm.net/oops}Description')[0].text
        print(suggestion_xml)

        try:
            iris = get_affected_soma_iris(suggestion_xml)
            if len(iris)>0:
                report_suggestion(name,descr,iris)
        except:
            continue
    '''
    return pitfalls

if __name__ == "__main__":
    df_all = pd.read_csv("output2_mse.csv")
    df_metrics_table = pd.read_excel("metrics_labels.xlsx")
    df_metrics_table = df_metrics_table[["metric_name","metric_code","ontometrics_name","evaluation_criteria"]]
    dic_pitfalls = {}
    
    for index, row in df_all.iterrows():
        url = df_all['mirror_from'][index]
        filename = 'all_files/' + df_all['namespace'][index] + '_oops.xml'
        try:
            dic_pitfalls[df_all['namespace'][index]] = run(filename)
        
        except:# KeyError as e:
            print(filename)
            #print(e)
            continue
    
    print(dic_pitfalls)
    with open("dic_pitfalls.pkl", "wb") as f:
        pickle.dump(dic_pitfalls, f)
