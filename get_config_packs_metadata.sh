#!/bin/bash

curl -L https://github.com/awslabs/aws-config-rules/archive/refs/heads/master.zip --output pack.zip
mkdir -p pack/
# Exclude example yaml template and include only yaml files
unzip -o pack.zip "aws-config-rules-master/aws-config-conformance-packs/*.yaml" -d pack/ -x "aws-config-rules-master/aws-config-conformance-packs/custom-conformance-pack.yaml"
cd pack/aws-config-rules-master/aws-config-conformance-packs
curl -L https://raw.githubusercontent.com/awsdocs/aws-config-developer-guide/main/doc_source/managed-rules-by-aws-config.md --output managed_rules.md
python3 ../../../parse_packs.py
# Get Timestamp for updates
echo "{\"date\":\"$(date +"%B %d %Y")\"}" > ../../../src/assets/VERSION.json