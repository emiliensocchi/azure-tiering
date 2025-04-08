"""
    Name: 
        convert-markdown-to-json
        
    Author: 
        Emilien Socchi

    Description:  
         convert-markdown-to-json converts roles and permissions already categorized in specific tiers from Markdown to JSON.

    Requirements:
        - A service principal with the following granted MS Graph application permissions:
            1. 'RoleManagement.Read.Directory' (to read Entra role definitions)
            2. 'Application.Read.All' (to read the definitions of application permissions)
        - Valid access tokens for ARM and MS Graph are expected to be available to convert-markdown-to-json via the following environment variables:
            - 'ARM_ACCESS_TOKEN'
            - 'MSGRAPH_ACCESS_TOKEN'

    Note 1:
        During the conversion to JSON, tiered roles and permissions are enriched with their definition Ids, which need to be retrieved
        from the MS Graph and ARM APIs.
    
    Note 2:
        In a tenant with a default configuration, service principals have permissions to read Azure role definitions by default.
        Therefore, the service principal should not require any additional Azure permission.

"""
import json
import os
import re
import requests
import sys


def get_builtin_azure_role_definitions_from_arm(token):
    """
        Retrieves built-in Azure role definitions from ARM.

        Args:
            token(str): a valid access token for ARM

        Returns:
            list(str): list of role definitions

    """
    endpoint = "https://management.azure.com/providers/Microsoft.Authorization/roleDefinitions?$filter=type eq 'BuiltInRole'&api-version=2023-07-01-preview"
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(endpoint, headers = headers)

    if response.status_code != 200:
        print('FATAL ERROR - The Azure roles could not be retrieved from ARM.')
        exit()

    paginated_response = response.json()['value']
    complete_response = paginated_response
    next_page = response.json()['nextLink'] if 'nextLink' in response.json() else ''

    while next_page:
        response = requests.get(next_page, headers = headers)

        if response.status_code != 200:
            print('FATAL ERROR - The Azure roles could not be retrieved from ARM.')
            exit()
        
        paginated_response = response.json()['value']
        next_page = response.json()['nextLink'] if 'nextLink' in response.json() else ''
        complete_response += paginated_response

    return complete_response


def get_builtin_entra_role_definitions_from_graph(token):
    """
        Retrieves built-in Entra role definitions from MS Graph.

        Args:
            str: a valid access token for MS Graph

        Returns:
            list(str): list of built-in Entra-role definitions

    """
    endpoint = 'https://graph.microsoft.com/v1.0/roleManagement/directory/roleDefinitions?$filter=isBuiltIn eq true'
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(endpoint, headers = headers)

    if response.status_code != 200:
        print('FATAL ERROR - The Entra roles could not be retrieved from Graph.')
        exit()

    response_content = response.json()['value']
    return response_content


def get_builtin_application_permission_definitions_from_graph(token):
    """
        Retrieves built-in Microsoft Graph application permission definitions from MS Graph.

        Args:
            str: a valid access token for MS Graph

        Returns:
            list(str): list of built-in MS Graph application permission definitions

    """
    endpoint = "https://graph.microsoft.com/v1.0/servicePrincipals(appId='00000003-0000-0000-c000-000000000000')"
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(endpoint, headers = headers)

    if response.status_code != 200:
        print('FATAL ERROR - The MS Graph application permissions could not be retrieved from Graph.')
        exit()

    response_content = response.json()['appRoles']
    return response_content


def convert_azure_markdown_to_json(azure_markdown_file, azure_json_file, azure_role_ids):
    """
        Converts and outputs the Azure roles tiering information located in the passed Markdown file to JSON.
        The Azure roles tiering data is enriched with the role IDs in the process.

        Args:
            azure_markdown_file(str): the Markdown file containing Azure roles tiering to parse from
            azure_json_file(str): the output file to which the converted JSON is exported to
            azure_role_ids(dict(str:str)): dictionary mapping Azure role names to their respective IDs

        Returns:
            None

    """
    try:
        json_roles = []
        regex = r"(\[|\]|\(https?:\/\/[^\s)]+\)|\(#[a-z\-]*\)|\\u26a0\\ufe0f |\*|<br>|`|\"|\\ud83d\\udd70\\ufe0f )"    # strips unwanted content
        
        with open(azure_markdown_file, 'r') as file:
            file_content = file.read()
            tiered_content = file_content.split('##')[2:]
            tier_0_content = tiered_content[0]
            tier_1_content = tiered_content[1]
            tier_2_content = tiered_content[2]
            tier_3_content = tiered_content[3]

            # Parsing Tier-0 content
            splitted_tier_0_content = tier_0_content.split('\n| [')[1:]

            for line in splitted_tier_0_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = azure_role_ids[asset_name_key] if asset_name_key in azure_role_ids.keys() else ''
                shortest_path = re.sub(regex, '', elements[1]).encode('ascii', 'ignore').decode().strip()
                example = re.sub(regex, '', elements[2].strip())
                json_role = {
                    'tier': "0", 
                    'id': asset_id,
                    'assetName': asset_name, 
                    'shortestPath': shortest_path,
                    'example': example
                }
                json_roles.append(json_role)

            # Parsing Tier-1 content
            splitted_tier_1_content = tier_1_content.split('\n| [')[1:]

            for line in splitted_tier_1_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = azure_role_ids[asset_name_key] if asset_name_key in azure_role_ids.keys() else ''
                shortest_path = re.sub(regex, '', elements[1]).encode('ascii', 'ignore').decode().strip()
                example = re.sub(regex, '', elements[2].strip())
                json_role = {
                    'tier': "1", 
                    'id': asset_id,
                    'assetName': asset_name, 
                    'shortestPath': shortest_path,
                    'example': example
                }
                json_roles.append(json_role)

            # Parsing Tier-2 content
            splitted_tier_2_content = tier_2_content.split('\n| [')[1:]

            for line in splitted_tier_2_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = azure_role_ids[asset_name_key] if asset_name_key in azure_role_ids else ''
                worst_case_scenario = re.sub(regex, '', elements[1].strip())
                json_role = {
                    'tier': '2',
                    'id': asset_id,
                    'assetName': asset_name,
                    'worstCaseScenario': worst_case_scenario
                }
                json_roles.append(json_role)


            # Parsing Tier-3 content
            splitted_tier_3_content = tier_3_content.split('\n| [')[1:]

            for line in splitted_tier_3_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = azure_role_ids[asset_name_key] if asset_name_key in azure_role_ids else ''
                worst_case_scenario = re.sub(regex, '', elements[1].strip())
                json_role = {
                    'tier': '3',
                    'id': asset_id,
                    'assetName': asset_name,
                    'worstCaseScenario': worst_case_scenario
                }
                json_roles.append(json_role)

        with open(azure_json_file, "w") as file:
            file.write(json.dumps(json_roles, indent = 4))

    except FileNotFoundError:
        print('FATAL ERROR - Converting Azure markdown to json has failed.')
        exit()


def convert_entra_markdown_to_json(entra_markdown_file, entra_json_file, entra_role_ids):
    """
        Converts and outputs the Entra roles tiering information located in the passed Markdown file to JSON.
        The Entra roles tiering data is enriched with the role IDs in the process.

        Args:
            entra_markdown_file(str): the Markdown file containing Entra roles tiering to parse from
            entra_json_file(str): the output file to which the converted JSON is exported to
            entra_role_ids(dict(str:str)): dictionary mapping Entra role names to their respective IDs

        Returns:
            None

    """
    try:
        json_roles = []
        regex = r"(\[|\]|\(https?:\/\/[^\s)]+\)|\(#[a-z\-]*\)|\\u26a0\\ufe0f |\*|<br>|`|\"|\\ud83d\\udd70\\ufe0f )"    # strips unwanted content
        
        with open(entra_markdown_file, 'r') as file:
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
                asset_id = entra_role_ids[asset_name_key] if asset_name_key in entra_role_ids.keys() else ''
                path_type = elements[1].strip()
                shortest_path = re.sub(regex, '', elements[2]).encode('ascii', 'ignore').decode().strip()
                example = re.sub(regex, '', elements[3].strip())
                json_role = {
                    'tier': "0", 
                    'id': asset_id,
                    'assetName': asset_name, 
                    'pathType': path_type,
                    'shortestPath': shortest_path,
                    'example': example
                }
                json_roles.append(json_role)

            # Parsing Tier-1 content
            splitted_tier_1_content = tier_1_content.split('\n| [')[1:]

            for line in splitted_tier_1_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = entra_role_ids[asset_name_key] if asset_name_key in entra_role_ids else ''
                provides_full_access_to = re.sub(regex, '', elements[1].strip())
                json_role = {
                    'tier': '1', 
                    'id': asset_id,
                    'assetName': asset_name,
                    'providesFullAccessTo': provides_full_access_to
                }
                json_roles.append(json_role)

            # Parsing Tier-2 content
            splitted_tier_2_content = tier_2_content.split('\n| [')[1:]

            for line in splitted_tier_2_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = entra_role_ids[asset_name_key] if asset_name_key in entra_role_ids else ''
                json_role = {
                    'tier': '2',
                    'id': asset_id,
                    'assetName': asset_name
                }
                json_roles.append(json_role)

        with open(entra_json_file, "w") as file:
            file.write(json.dumps(json_roles, indent = 4))

    except FileNotFoundError:
        print('FATAL ERROR - Converting Entra markdown to json has failed.')
        exit()


def convert_msgraph_markdown_to_json(msgraph_markdown_file, msgraph_json_file, msgraph_permission_ids):
    """
        Converts and outputs the MS Graph permissions tiering information located in the passed Markdown file to JSON.
        The MS Graph permissions tiering data is enriched with the permission IDs in the process.

        Args:
            msgraph_markdown_file(str): the Markdown file containing msgraph permissions tiering to parse from
            msgraph_json_file(str): the output file to which the converted JSON is exported to
            msgraph_permission_ids(dict(str:str)): dictionary mapping MS Graph permission names to their respective IDs

        Returns:
            None

    """
    try:
        json_permissions = []
        regex = r"(\[|\]|\(https?:\/\/[^\s)]+\)|\(#[a-z\-]*\)|\\u26a0\\ufe0f |\*|<br>|`|\"|\\ud83d\\udd70\\ufe0f )"    # strips unwanted content
        
        with open(msgraph_markdown_file, 'r') as file:
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
                asset_id = msgraph_permission_ids[asset_name_key] if asset_name_key in msgraph_permission_ids.keys() else ''
                path_type = elements[1].strip()
                shortest_path = re.sub(regex, '', elements[2]).encode('ascii', 'ignore').decode().strip()
                example = re.sub(regex, '', elements[3].strip())
                json_permission = {
                    'tier': "0", 
                    'id': asset_id,
                    'assetName': asset_name, 
                    'pathType': path_type,
                    'shortestPath': shortest_path,
                    'example': example
                }
                json_permissions.append(json_permission)

            # Parsing Tier-1 content
            splitted_tier_1_content = tier_1_content.split('\n| [')[1:]

            for line in splitted_tier_1_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = msgraph_permission_ids[asset_name_key] if asset_name_key in msgraph_permission_ids else ''
                json_permission = {
                    'tier': '1', 
                    'id': asset_id,
                    'assetName': asset_name
                }
                json_permissions.append(json_permission)

            # Parsing Tier-2 content
            splitted_tier_2_content = tier_2_content.split('\n| [')[1:]

            for line in splitted_tier_2_content:
                elements = line.split('|')
                asset_name = re.sub(regex, '', elements[0].split(']', 1)[0])
                asset_name_key = asset_name.lower().replace(' ', '')
                asset_id = msgraph_permission_ids[asset_name_key] if asset_name_key in msgraph_permission_ids else ''
                json_permission = {
                    'tier': '2',
                    'id': asset_id,
                    'assetName': asset_name
                }
                json_permissions.append(json_permission)

        with open(msgraph_json_file, "w") as file:
            file.write(json.dumps(json_permissions, indent = 4))

    except FileNotFoundError:
        print('FATAL ERROR - Converting MS Graph markdown to json has failed.')
        exit()


if __name__ == "__main__":
    # Get ARM and MS Graph access tokens from environment variables
    arm_access_token = os.environ['ARM_ACCESS_TOKEN']
    graph_access_token = os.environ['MSGRAPH_ACCESS_TOKEN']

    if not arm_access_token:
        print('FATAL ERROR - A valid access token for ARM is required.')
        exit()

    if not graph_access_token:
        print('FATAL ERROR - A valid access token for MS Graph is required.')
        exit()

    # Set local directories
    github_action_dir_name = '.github'
    absolute_path_to_script = os.path.abspath(sys.argv[0])
    root_dir = absolute_path_to_script.split(github_action_dir_name)[0]
    azure_dir = root_dir + 'Azure roles'
    entra_dir = root_dir + 'Entra roles'
    app_permissions_dir = root_dir + 'Microsoft Graph application permissions'
    
    # Set local Markdown files
    azure_roles_markdown_file = f"{azure_dir}/README.md"
    entra_roles_markdown_file = f"{entra_dir}/README.md"
    app_permissions_markdown_file = f"{app_permissions_dir}/README.md"

    # Set local JSON files
    azure_roles_json_file = f"{azure_dir}/tiered-azure-roles.json"
    entra_roles_json_file = f"{entra_dir}/tiered-entra-roles.json"
    app_permissions_json_file = f"{app_permissions_dir}/tiered-msgraph-app-permissions.json"

    # Get built-in Azure roles from ARM
    builtin_azure_roles = {}
    builtin_azure_role_definitions = get_builtin_azure_role_definitions_from_arm(arm_access_token)

    for builtin_azure_role_definition in builtin_azure_role_definitions:
        id = builtin_azure_role_definition['name']
        name = builtin_azure_role_definition['properties']['roleName'].lower().replace(' ', '')
        builtin_azure_roles[name] = id

    # Get built-in Entra roles from MS Graph
    builtin_entra_roles = {}
    builtin_entra_role_definitions = get_builtin_entra_role_definitions_from_graph(graph_access_token)

    for builtin_entra_role_definition in builtin_entra_role_definitions:
        id = builtin_entra_role_definition['id']
        name = builtin_entra_role_definition['displayName'].lower().replace(' ', '')
        builtin_entra_roles[name] = id

    # Get built-in application permissions from MS Graph
    builtin_msgraph_app_permissions = {}
    builtin_msgraph_app_permission_definitions = get_builtin_application_permission_definitions_from_graph(graph_access_token)

    for builtin_msgraph_app_permission_definition in builtin_msgraph_app_permission_definitions:
        id = builtin_msgraph_app_permission_definition['id']
        name = builtin_msgraph_app_permission_definition['value'].lower().replace(' ', '')
        builtin_msgraph_app_permissions[name] = id

    # Convert Markdown content for Azure roles to JSON
    markdown_file_name = azure_roles_markdown_file.rsplit('/', 2)[1]
    print (f"Converting: {markdown_file_name}")
    convert_azure_markdown_to_json(azure_roles_markdown_file, azure_roles_json_file, builtin_azure_roles)

    # Convert Markdown content for Entra roles to JSON
    markdown_file_name = entra_roles_markdown_file.rsplit('/', 2)[1]
    print (f"Converting: {markdown_file_name}")
    convert_entra_markdown_to_json(entra_roles_markdown_file, entra_roles_json_file, builtin_entra_roles)

    # Convert Markdown content for MS Graph application permissions to JSON
    markdown_file_name = app_permissions_markdown_file.rsplit('/', 2)[1]
    print (f"Converting: {markdown_file_name}")
    convert_msgraph_markdown_to_json(app_permissions_markdown_file, app_permissions_json_file, builtin_msgraph_app_permissions)
