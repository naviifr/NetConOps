import time
import config
import engine
import formatter
start = time.time()

scan_config = config.ScanConfig()
ports = [80,443,23,21,25,110,143,53,8080]
target = "google.com" 

scanner = engine.Engine(target, ports, scan_config)
results = scanner.run()
formatter.print_result(results)

end = time.time()
print(end - start)                          #for calculating the execution time