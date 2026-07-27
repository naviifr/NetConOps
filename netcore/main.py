import time
import core.config as config
import core.engine as engine
import core.formatter as formatter

start = time.time()

scan_config = config.ScanConfig()
ports = [80,443,22,23,25,110,143,53,8080]
target = "google.com" 
# target = "scanme.nmap.org"
plugins = ["tcp","banner"]

scanner = engine.Engine(target, ports, scan_config, plugins)
results = scanner.run()
formatter.print_result(results)

end = time.time()
print(end - start)                          #for calculating the execution time