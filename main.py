import asyncio
import httpx

from fastmcp import FastMCP
import json
import os


from fastmcp.server.openapi import RouteMap, MCPType


async def load_custom_mappings_from_json(json_data: str | list[dict]) -> list[RouteMap]:
    """
    Convert JSON-formatted route mappings into a list of RouteMap objects.

    Args:
        json_data: JSON string or already-parsed list of dicts

    Returns:
        List[RouteMap]
    """
    if isinstance(json_data, str):
        mappings = json.loads(json_data)
    else:
        mappings = json_data

    route_maps = []
    for mapping in mappings:
        methods = mapping.get("methods", "*")
        pattern = mapping["pattern"]
        mcp_type_str = mapping["mcp_type"].upper()

        try:
            mcp_type = MCPType[mcp_type_str]
        except KeyError:
            raise ValueError(f"Invalid MCP type: {mcp_type_str}")

        route_maps.append(RouteMap(methods=methods, pattern=pattern, mcp_type=mcp_type))

    return route_maps

async def load_json(filepath):
    
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)        
        return data


async def test_client(http_client):
    response = await http_client.get("/categories/")
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Success: Categories fetched")
        print("Response JSON:", response.json())
    else:
        print("Failed")
        print("Response:", response.text)
    response2 = await http_client.request(
    method="GET",
    url="/categories/")
    print("Status Code:=========================", response2.status_code)
    if response2.status_code == 200:
        print("Success: Categories fetched")
        print("Response JSON:", response.json())
    else:
        print("Failed")
        print("Response:", response.text)

    headers = {'authorization': 'Bearer xxx'}

    headers2 ={'connection': 'keep-alive',                     
                             'accept': '*/*', 'accept-language': '*', 'sec-fetch-mode': 'cors',               
                             'user-agent': 'python-httpx/0.28.1', 'pragma': 'no-cache',                       
                             'cache-control': 'no-cache', 'accept-encoding': 'gzip, deflate',                 
                             'authorization': 'Bearer xxx'}
    response3 = await http_client.request(
    method="GET", headers=headers2,
    url="/categories/")
    print("Response 3 Status Code:=========================", response3.status_code)
    
    if response3.status_code == 200:
        print("Success: Categories fetched")
        print("Response JSON:", response.json())
    else:
        print("Failed")
        print("Response:", response.text)    


async def test_client_now(http_client):
    headers ={'host': '0.0.0.0:9000', 'connection': 'keep-alive',                     
                             'accept': '*/*', 'accept-language': '*', 'sec-fetch-mode': 'cors',               
                             'user-agent': 'python-httpx/0.28.1', 'pragma': 'no-cache',                       
                             'cache-control': 'no-cache', 'accept-encoding': 'gzip, deflate',                 
                             'authorization': 'Bearer xxx'}
    response = await http_client.request(
                    method="GET",
                    url="/venues/217773319/events/",
                    params={},
                    headers=headers,
                    json=None,
                    timeout=None,
                )
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Success: Categories fetched")
        print("Response JSON:", response.json())
    else:
        print("Failed")
        print("Response:", response.text)

async def main():
    filepath="spec_openapi/eventbrite-openapi.json"
    openapi_spec = await load_json(filepath)
    
    api_key_header: str = "Authorization"
    server_config = await load_json("config/server_config.json")

    headers = {}
    if server_config["auth"]["token"]:
        headers[api_key_header] = f"Bearer {server_config["auth"]["token"]}"

    print(headers)
    
    
    server_url = openapi_spec["servers"][0]["url"]
    http_client = httpx.AsyncClient(base_url=server_url, headers=headers)
    
    # test client 
    await test_client(http_client)
    #await test_client_now(http_client)
    
    config_mapping = await load_json("config/custom_mapping.json")
    print(config_mapping)
    route_maps = await load_custom_mappings_from_json(config_mapping)
    
    # You can now pass this to your tool generator
    mcp = FastMCP.from_openapi(openapi_spec, 
                               client=http_client, 
                               route_maps=route_maps)
    
    # Start MCP with SSE transport
    await mcp.run_sse_async(
        host="127.0.0.1",
        port=9000,
        log_level="debug"
    )


if __name__ == "__main__":
    print("\n--- Starting FastMCP Server for via __main__ ---")
    asyncio.run(main())