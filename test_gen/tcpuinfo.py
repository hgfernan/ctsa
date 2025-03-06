import json
from cpuinfo import get_cpu_info 

info = get_cpu_info() 

print(json.dumps(info, indent=4))

