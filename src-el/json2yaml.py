import sys, json, yaml
with open(sys.argv[1]) as f:
   out = open("out.yaml","w")
   out.write(yaml.safe_dump(json.load(f), default_flow_style=False))


