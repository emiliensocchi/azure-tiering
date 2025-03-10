"""
    Name: 
        ConvertTieredInMarkdownToJson
        
    Author: 
        Emilien Socchi

    Description:  
         ConvertTieredInMarkdownToJson converts roles and permissions already categorized in specific tiers from Markdown to JSON

"""
import json
import os
import re
import requests
import sys


def get_builtin_msgraph_app_permission_objects_from_graph(token):
    """
        Retrieves the current built-in Microsoft Graph application permission objects from MS Graph.

        Args:
            str: a valid access token for MS Graph

        Returns:
            list(str): list of built-in MS Graph application permission objects

    """
    endpoint = "https://graph.microsoft.com/v1.0/servicePrincipals(appId='00000003-0000-0000-c000-000000000000')"
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(endpoint, headers = headers)

    if response.status_code != 200:
        print('FATAL ERROR - The MS Graph application permissions could not be retrieved from Graph.')
        exit()

    response_content = response.json()['appRoles']
    return response_content


def get_builtin_entra_role_objects_from_graph(token):
    """
        Retrieves the current built-in Entra role objects from MS Graph.

        Args:
            str: a valid access token for MS Graph

        Returns:
            list(str): list of built-in Entra-role objects

    """
    endpoint = 'https://graph.microsoft.com/v1.0/roleManagement/directory/roleDefinitions?$filter=isBuiltIn eq true'
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(endpoint, headers = headers)

    if response.status_code != 200:
        print('FATAL ERROR - The Entra roles could not be retrieved from Graph.')
        exit()

    response_content = response.json()['value']
    return response_content


def convert_markdown_to_json(markdown_file, json_file, asset_ids):
    """
        Converts the administrative-asset info located in the passed Markdown file to JSON, and outputs it to the passed JSON file.
        The data of the administrative asset is enriched with the asset's ID in the process.

        Args:
            markdown_file(str): the Markdown file to parse from
            json_file(str): the output file to which the converted JSON is exported to
            asset_ids(dict(str:str)): dictionary mapping asset names to their respective IDs

        Returns:
            None

    """
    try:
        json_roles = []
        regex = r"(\[|\]|\(.*\)|\\u26a0\\ufe0f |\*|<br>|`|\\ud83d\\udd70\\ufe0f )"    # strips unwanted content
        
        with open(markdown_file, 'r') as file:
            file_content = file.read()

            tiered_content = file_content.split('##')[2:]
            tier_0_content = tiered_content[0]
            tier_1_content = tiered_content[1]
            tier_2_content = tiered_content[2]

            # Parsing Tier-0 content
            splitted_tier_0_content = tier_0_content.split('\n| [')[1:]

            for line in splitted_tier_0_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = asset_ids[asset_name_key] if asset_name_key in asset_ids.keys() else ''
                path_type = elements[1].strip()
                known_shortest_path = re.sub(regex, '', elements[2]).encode('ascii', 'ignore').decode().strip()
                example = re.sub(regex, '', elements[3].strip())

                json_role = {
                    "tier": "0", 
                    "id": asset_id,
                    "assetName": asset_name, 
                    "pathType": path_type,
                    "knownShortestPath": known_shortest_path,
                    "example": example
                }

                json_roles.append(json_role)

            # Parsing Tier-1 content
            splitted_tier_1_content = tier_1_content.split('\n| [')[1:]

            for line in splitted_tier_1_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = asset_ids[asset_name_key] if asset_name_key in asset_ids else ''
                provides_full_access_to = re.sub(regex, '', elements[1].strip())

                if elements [1]:
                    json_role = {
                        "tier": "1", 
                        "id": asset_id,
                        "assetName": asset_name,
                        "providesFullAccessTo": provides_full_access_to
                    }
                else:
                    json_role = {
                        "tier": "1", 
                        "id": asset_id,
                        "assetName": asset_name
                    }

                json_roles.append(json_role)

            # Parsing Tier-2 content
            splitted_tier_2_content = tier_2_content.split('\n| [')[1:]

            for line in splitted_tier_2_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = asset_ids[asset_name_key] if asset_name_key in asset_ids else ''
                json_role = {
                    "tier": "2",
                    "id": asset_id,
                    "assetName": asset_name
                }

                json_roles.append(json_role)

        with open(json_file, "w") as file:
            file.write(json.dumps(json_roles, indent = 4))

    except FileNotFoundError:
        print('FATAL ERROR - Converting markdown to json has failed.')
        exit()


if __name__ == "__main__":
    # Get MS Graph access token from environment variable
    graph_access_token = os.environ['MSGRAPH_ACCESS_TOKEN']

    if not graph_access_token:
        print('FATAL ERROR - A valid access token for MS Graph is required.')
        exit()

    # Set local directories
    github_action_dir_name = '.github'
    absolute_path_to_script = os.path.abspath(sys.argv[0])
    root_dir = absolute_path_to_script.split(github_action_dir_name)[0]
    entra_dir = root_dir + 'Entra roles'
    app_permissions_dir = root_dir + 'Microsoft Graph application permissions'
    
    # Set local Markdown files
    entra_roles_markdown_file = f"{entra_dir}/README.md"
    app_permissions_markdown_file = f"{app_permissions_dir}/README.md"

    # Set local JSON files
    entra_roles_json_file = f"{entra_dir}/tiered-entra-roles.json"
    app_permissions_json_file = f"{app_permissions_dir}/tiered-msgraph-app-permissions.json"

    # Get current built-in Entra roles from MS Graph
    current_builtin_entra_roles = {}
    current_builtin_entra_role_objects = get_builtin_entra_role_objects_from_graph(graph_access_token)

    for current_builtin_entra_role_object in current_builtin_entra_role_objects:
        id = current_builtin_entra_role_object['id']
        name = current_builtin_entra_role_object['displayName'].lower().replace(' ', '')
        current_builtin_entra_roles[name] = id

    # Get current built-in MS Graph application permissions from MS Graph
    current_builtin_msgraph_app_permissions = {}
    current_builtin_msgraph_app_permission_objects = get_builtin_msgraph_app_permission_objects_from_graph(graph_access_token)

    for current_builtin_msgraph_app_permission_object in current_builtin_msgraph_app_permission_objects:
        id = current_builtin_msgraph_app_permission_object['id']
        name = current_builtin_msgraph_app_permission_object['value'].lower().replace(' ', '')
        current_builtin_msgraph_app_permissions[name] = id

    # Convert Markdown content for Entra roles to JSON
    markdown_file_name = entra_roles_markdown_file.rsplit('/', 2)[1]
    print (f"Converting for: {markdown_file_name}")
    convert_markdown_to_json(entra_roles_markdown_file, entra_roles_json_file, current_builtin_entra_roles)

    # Convert Markdown content for MS Graph application permissions to JSON
    markdown_file_name = app_permissions_markdown_file.rsplit('/', 2)[1]
    print (f"Converting for: {markdown_file_name}")
    convert_markdown_to_json(app_permissions_markdown_file, app_permissions_json_file, current_builtin_msgraph_app_permissions)
