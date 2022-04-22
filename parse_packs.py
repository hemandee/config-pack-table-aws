import yaml
import glob
import os
import json
import re
directory = os.getcwd() + '/*.yaml'

list_files = glob.glob(directory, recursive=True)
data = []
# Map markdown file names with AWS Config Identifier
change_map = {
    "EC2_INSTANCE_MANAGED_BY_SYSTEMS_MANAGER": "EC2_INSTANCE_MANAGED_BY_SSM",
    "CLOUDTRAIL_ENABLED": "CLOUD_TRAIL_ENABLED",
    "RESTRICTED_SSH": "INCOMING_SSH_DISABLED",
    "EC2_INSTANCES_IN_VPC": "INSTANCES_IN_VPC",
    "MULTI_REGION_CLOUDTRAIL_ENABLED": "MULTI_REGION_CLOUD_TRAIL_ENABLED",
    "RESTRICTED_COMMON_PORTS": "RESTRICTED_INCOMING_TRAFFIC"
}


def format(item):
    print(item)
    val = {}
    val["NAME"] = item[0]
    for elem in item[1]:
        val[elem] = "X"
    return val


# Parse Managed Rules
file_content_md = ''
rule_count = 0
headers = []
with open('managed_rules.md') as f:
    file_content_md = f.read()
list_rules = file_content_md.split('+')
regex = r'\[(.*)]'
for rule in list_rules:
    val = re.search(regex, rule)
    if val:
        headers.append(val.group(1).replace(
            '\\', '').replace('-', '_').upper())
        rule_count += 1

print(f'Total Managed Rule count {rule_count}')
headers = list(map(lambda item: change_map.get(item) or item, headers))
# with open('../../../src/assets/data_headers.json', 'w+') as output:
#     output.write(json.dumps(headers, indent=4))
# Parse Config Packs
rule_set = {}
config_process_check_list = {}
for file in list_files:
    with open(file) as f:
        file_content = yaml.load(f, Loader=yaml.FullLoader)
    pack_name = os.path.basename(f.name).replace(
        'Operational-Best-Practices-for-', '').replace('.yaml', '')
    for i in file_content.items():
        data_elem = {}
        data_elem['NAME'] = pack_name
        data_elem[
            'URL'] = f'https://raw.githubusercontent.com/awslabs/aws-config-rules/master/aws-config-conformance-packs/{os.path.basename(f.name)}'
        if i[0] == 'Resources':
            for w in i[1]:
                if i[1][w]['Type'] == 'AWS::Config::ConfigRule':
                    if i[1][w]['Properties']['Source']['Owner'] == 'AWS' and i[1][w]['Properties']['Source']['SourceIdentifier'] == 'AWS_CONFIG_PROCESS_CHECK':
                        rule_name = (
                            i[1][w]['Properties']['ConfigRuleName'].replace('-', '_').upper() + "_PROCESS_CHECK")
                        data_elem[rule_name] = 'X'
                        # if not any(d['NAME'] == 'ACCESS_KEYS_ROTATED' for d in rule_set):
                        # rule_set.append({'NAME': rule_name})
                        if not rule_name in rule_set:
                            rule_set[rule_name] = []
                        rule_set[rule_name].append(pack_name)
                        config_process_check_list[rule_name] = {
                            "Description": i[1][w]['Properties'].get('Description', 'empty description'),
                            "ConfigName": i[1][w]['Properties']['ConfigRuleName']
                        }
                    elif i[1][w]['Properties']['Source']['Owner'] == 'AWS':
                        rule_name = (i[1][w]['Properties']
                                     ['Source']['SourceIdentifier'])
                        data_elem[rule_name] = 'X'
                        # if not any(d['NAME'] == 'ACCESS_KEYS_ROTATED' for d in rule_set):
                        # rule_set.append({'NAME': rule_name})
                        if not rule_name in rule_set:
                            rule_set[rule_name] = []
                        rule_set[rule_name].append(pack_name)
                        # rule_set.append({'NAME': rule_name, pack_name: 'X'})
                    else:
                        raise Exception('Error in managed config rules')
            TOTAL_RULES = len(data_elem)
            data_elem["TOTAL_RULES"] = TOTAL_RULES
            data.append(data_elem)
with open('../../../src/assets/data.json', 'w+') as output:
    output.write(json.dumps(data, indent=4))
list_rule_set = list(rule_set.items())
map_rule_set = list(map(format, list_rule_set))
with open('../../../src/assets/data_rule_set.json', 'w+') as output:
    output.write(json.dumps(map_rule_set, indent=4))
with open('../../../src/assets/data_headers_rule_set.json', 'w+') as output:
    output.write(json.dumps(list(rule_set.keys()), indent=4))
with open('../../../src/assets/data_headers.json', 'w+') as output:
    output.write(json.dumps(
        headers + list(config_process_check_list.keys()), indent=4))
with open('../../../src/assets/ruleset_parse.json', 'w+') as output:
    w = open("../../../src/assets/data_headers.json")
    ruleset = json.load(w)
    # ruleset = ruleset + config_process_check_list
    w.close()
    ruleSetLoc = {}
    for i in ruleset:
        if "_PROCESS_CHECK" in i:
            ruleSetLoc[i] = json.dumps(config_process_check_list[i])
        elif i == 'EC2_INSTANCE_MANAGED_BY_SYSTEMS_MANAGER':
            ruleSetLoc[i] = f'https://s3.amazonaws.com/aws-configservice-us-east-1/cloudformation-templates-for-managed-rules/EC2_INSTANCE_MANAGED_BY_SSM.template'
        elif i == 'CLOUDTRAIL_ENABLED':
            ruleSetLoc[
                i] = f'https://s3.amazonaws.com/aws-configservice-us-east-1/cloudformation-templates-for-managed-rules/CLOUD_TRAIL_ENABLED.template'
        elif i == 'RESTRICTED_SSH':
            ruleSetLoc[
                i] = f'https://s3.amazonaws.com/aws-configservice-us-east-1/cloudformation-templates-for-managed-rules/INCOMING_SSH_DISABLED.template'
        elif i == 'EC2_INSTANCES_IN_VPC':
            ruleSetLoc[
                i] = f'https://s3.amazonaws.com/aws-configservice-us-east-1/cloudformation-templates-for-managed-rules/INSTANCES_IN_VPC.template'
        elif i == 'MULTI_REGION_CLOUDTRAIL_ENABLED':
            ruleSetLoc[
                i] = f'https://s3.amazonaws.com/aws-configservice-us-east-1/cloudformation-templates-for-managed-rules/MULTI_REGION_CLOUD_TRAIL_ENABLED.template'
        elif i == 'RESTRICTED_COMMON_PORTS':
            ruleSetLoc[
                i] = f'https://s3.amazonaws.com/aws-configservice-us-east-1/cloudformation-templates-for-managed-rules/RESTRICTED_INCOMING_TRAFFIC.template'
        else:
            ruleSetLoc[
                i] = f'https://s3.amazonaws.com/aws-configservice-us-east-1/cloudformation-templates-for-managed-rules/{i}.template'
    output.write(json.dumps(ruleSetLoc, indent=4))
print(f'Completed Output')
