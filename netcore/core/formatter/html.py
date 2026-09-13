from html import escape

def render_value(data): 

        html= ""
            
        if isinstance(data, dict):
            html+= "<ul>"
            for key, value in data.items():
                html+= f"<li><strong>{escape(str(key))}:</strong>"
                html+= render_value(value) 
                html+= "</li>"
            html+= "</ul>"
            return html

        if isinstance(data, list):
            html+= "<ul>"
            for value in data:
                html+= "<li>"
                html+= render_value(value)
                html+= "</li>"
            html+= "</ul>"
            return html

        else:
            html+= " "
            html+= escape(str(data))

        return html

def html_result(result_list):
    target = result_list[0].target if result_list else ""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NetConOps Report - {escape(target)}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 30px;
            }}

            .container {{
                width: 80%;
                max-width: 1100px;
                margin: auto;
                background-color: white;
                padding: 30px;
            }}

            h1 {{
                text-align: center;
            }}

            h2 {{
                margin-top: 30px;
                border-bottom: 1px solid #ccc;
                padding-bottom: 5px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}

            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}

            th {{
                background-color: #eee;
            }}

            .host-data {{
                margin-top: 20px;
            }}
        </style>
    </head>

    <body>
    
    <div class="container">

        <h1>NetConOps Report</h1>
        <h2>Target: {escape(target)}</h2>
    """
    host_result = []
    port_result = []
    service= False
    
    for result in result_list:

        if result.port is None:
            host_result.append(result)
        else:
            port_result.append(result)

    service = any(
        'service' in result.plg_data
        for result in port_result
        )

    if host_result:

        html += "<h2>Host Information</h2>"

        for result in host_result:

            if result.error:
                html += "<h3>Errors</h3>"
                html += render_value(result.error)

            if result.plg_data:
                html += "<h3>Info Gathered</h3>"
                html += render_value(result.plg_data)

    if port_result:

        html += """
        <h2>Ports</h2>

        <table>
            <tr>
                <th>Port</th>
                <th>Status</th>
        """

        if service:
            html+= """<th>Service</th>
                      <th>Confidence</th> 
                    </tr>"""
            
        for result in port_result:

            status = (
                result.status.value
                if result.status is not None
                else ""
            )

            html += f"""
            <tr>
                <td>{escape(str(result.port))}</td>
                <td>{escape(status)}</td>
            """
            if service:
                html+= f""" 
                            <td>{escape(result.plg_data["service"]["service"]) if 'service' in result.plg_data else "-"}</td>
                            <td>{escape(result.plg_data["service"]['confidence']) if 'service' in result.plg_data else "-"}</td>
                        </tr>
                            """

        html += """
        </table>
        """

        # Plugin data for each port
        for result in port_result:

            if result.error:
                html += f"<h3>Port {escape(str(result.port))} Errors</h3>"
                html += render_value(result.error)

            if result.plg_data:
                html += f"<h3>Port {escape(str(result.port))} Data</h3>"
                html += render_value(result.plg_data)

    html += """
    </div>
    </body>
    </html>
    """

    return html

def html_write(html, target):

    with open(f"../results/result_{target}.html", "w", encoding="utf-8") as file:
        file.write(html)

def html_execute(result_list: list):

    html = html_result(result_list)
    target = result_list[0].target if result_list else "unknown"
    html_write(html, target)