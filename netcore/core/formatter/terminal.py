
def get_results(result_queue):
    
    result_list= []
    while  not result_queue.empty():
        result_list.append(result_queue.get())
    
    result_list = sorted(result_list, key=lambda x: x.port)  #sorting the results based on port number
    return result_list

def print_rec(dict_data: dict, indent_level: int = 0):     #recursive function for printing nested dictionaries

            indent = "\t" * indent_level
            for key, value in dict_data.items():

                if isinstance(value, dict):
                    print(f"{indent}{key}:", end= "\n")
                    print_rec(value, indent_level + 1)

                else:
                    print(f"{indent}{key}: {value}")


def print_result(result_list:list):

    for i in result_list:

        print(f"{i.port}", f"{i.status.value}",
        f"".join((f" | {k}: {v}"  for k, v in i.error.items())) if i.error else "")

        if i.plg_data:
                    print_rec(i.plg_data)


