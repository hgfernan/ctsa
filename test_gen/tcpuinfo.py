import sys # argv
import json

from typing import Dict

from cpuinfo import get_cpu_info

if len(sys.argv) < 2:
    info = get_cpu_info()

else:
    info = json.load(open(sys.argv[1]))

print(json.dumps(info, indent=4, sort_keys=True))

digest : Dict[str, str] = {}

# "arch": "X86_64",
# "bits": 64,
# "count": 8,
# "arch_string_raw": "AMD64",
# "vendor_id_raw": "GenuineIntel",
# "brand_raw": "11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz",
# "hz_actual_friendly": "2.8030 GHz",
    
for key in ['arch', 'arch_string_raw', 'bits', 'brand_raw', 'count', 
            'hz_actual_friendly', 'vendor_id_raw']: 
    digest[key] = info[key]

print(json.dumps(digest, indent=4, sort_keys=True))

print(digest)
