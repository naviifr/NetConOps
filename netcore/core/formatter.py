def get_results(result_queue):
    
    a = []
    while  not result_queue.empty():
        a.append(result_queue.get())
    
    a = sorted(a, key=lambda x: x.port)  #sorting the results based on port number
    return a

def print_result(result_list):
    for i in result_list:
        print(i.port, ":", i.status.value, f"({i.error})" if i.error else "")
