#!/usr/bin/env python

import os
import sys
import requests
import subprocess
import urllib.request
import os.path
import pandas as pd


OOPS_URL="https://oops.linkeddata.es/rest"

def oops(owl_file):
	#
	f = open(owl_file, 'r')
	content = f.read()
	f.close()
	#
	xml_content = ("""
    <?xml version="1.0" encoding="UTF-8"?>
    <OOPSRequest>
      <OntologyUrl></OntologyUrl>
      <OntologyContent><![CDATA[
%s      
]]></OntologyContent>
          <Pitfalls></Pitfalls>
          <OutputFormat>XML</OutputFormat>
    </OOPSRequest>
	""" % content).encode("UTF-8")
	headers = {'Content-Type': 'application/xml',
	           'Connection': 'Keep-Alive'
	}
	return requests.post(OOPS_URL, data=xml_content, headers=headers).text

if __name__ == "__main__":
	# read arguments
     df_all = pd.read_csv("output2_mse.csv")    
     for index, row in df_all.iterrows():
          url = df_all['mirror_from'][index]
          filename = 'all_files/' + df_all['namespace'][index] + '.' + df_all['mirror_from'][index][-3:]
    
          out_dir = 'all_files/' + df_all['namespace'][index] + '_oops.xml'
          print(filename)
          xml_data = oops(filename)
          # write file
          #print(xml_data)
          out_file = os.path.join(out_dir)#,'oops.xml')
          f = open(out_file, "w")
          f.write(xml_data)
          f.close()
	


