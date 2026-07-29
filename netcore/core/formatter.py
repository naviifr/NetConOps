def get_results(result_queue):
    
    result_list= []
    while  not result_queue.empty():
        result_list.append(result_queue.get())
    
    result_list = sorted(result_list, key=lambda x: x.port)  #sorting the results based on port number
    return result_list

def print_result(result_list):
    for i in result_list:
        print(f"{i.port}", f"\n{i.status.value}",
        f"".join((f"| {k}: {v}"  for k, v in i.error.items())) if i.error else "")

        if i.plg_data:
            for k, v in i.plg_data.items():

                if type(v) is dict:
                    print(f"{k}:", end= "")
                    for p, q in v.items():
                          print(f"\t{p}: {q}")
                else:
                    print(f"{k}: {v}")

        