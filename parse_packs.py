import yaml
import glob
import os
import json
import re
directory = os.getcwd() + '/*.yaml'

list_files = glob.glob(directory, recursive=True)
data = []
# Parse Managed Rules
file_content_md = ''
rule_count=0
headers= []
with open('managed_rules.md') as f:
    file_content_md = f.read()
list_rules = file_content_md.split('+')
regex = r'\[(.*)]'
for rule in list_rules:
    val = re.search(regex,rule)
    if val:
        headers.append(val.group(1).replace('\\','').replace('-','_').upper())
        rule_count+=1

print(f'Total Managed Rule count {rule_count}')
with open('../../../src/assets/data_headers.json', 'w+') as output:
    output.write(json.dumps(headers, indent=4))
# Parse Config Packs

for file in list_files:
    with open(file) as f:
        file_content = yaml.load(f, Loader=yaml.FullLoader)
    pack_name = os.path.basename(f.name).replace('Operational-Best-Practices-for-','').replace('.yaml','')
    for i in file_content.items():
        data_elem = {}
        data_elem['NAME'] = pack_name
        if i[0] == 'Resources':
            for w in i[1]:
                if i[1][w]['Type'] == 'AWS::Config::ConfigRule': 
                    if i[1][w]['Properties']['Source']['Owner'] == 'AWS':              
                        data_elem[(i[1][w]['Properties']['Source']['SourceIdentifier'])] = 'X'
                    else:
                         raise Exception('Error in managed config rules')
            TOTAL_RULES = len(data_elem)
            data_elem["TOTAL_RULES"] = TOTAL_RULES
            data.append(data_elem)             
with open('../../../src/assets/data.json', 'w+') as output:
    output.write(json.dumps(data, indent=4))



