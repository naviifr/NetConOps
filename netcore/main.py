import time
import argparse
import core.config as config
import core.engine as engine
import core.formatter.terminal as terminal
import core.formatter.json as json
from plugins.plugins_registry import registry

start = time.time()

scan_config = config.ScanConfig()
default_ports = [80,443,22,23,25,110,143,53,8080]

parser = argparse.ArgumentParser()
parser.add_argument('target')
parser.add_argument('-p','--ports',type=int,nargs='+',default=default_ports)
parser.add_argument('-json', action= 'store_true')

for i in registry:
    parser.add_argument(f'-{i}', action='store_true')

args = parser.parse_args()

ports = args.ports
target = args.target
arg_dict= vars(args)

plugins = []

for i,j in arg_dict.items():
    if i in registry and j is True:
        if i in plugins:
            pass
        else:
            plugins.append(i)

if plugins == []:
    plugins.append('tcp')

# target = "scanme.nmap.org"

scanner = engine.Engine(target, ports, scan_config, plugins)
results = scanner.run()

if args.json:
    json.json_execute(results)
else:
    terminal.print_result(results)

end = time.time()
print(end - start)                          #for calculating the execution time