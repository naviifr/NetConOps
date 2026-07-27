def get_results(result_queue):
    
    result_list= []
    while  not result_queue.empty():
        result_list.append(result_queue.get())
    
    result_list = sorted(result_list, key=lambda x: x.port)  #sorting the results based on port number
    return result_list

def print_result(result_list):
    for i in result_list:
        print(i.port, ":", i.status.value, f"| Banner: {i.banner}" if i.banner else "", f"({i.error})" if i.error else "",)
