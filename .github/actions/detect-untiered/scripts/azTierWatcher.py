"""
    Name: 
        AzTierWatcher
        
    Author: 
        Emilien Socchi

    Description:  
         AzTierWatcher verifies if following have untiered assets, due to new additions and/removals in Microsoft's platform:
            - MS Graph application permissions
            - Entra roles

    Requirements:
        - A service principal with the following granted application permissions:
            1. 'RoleManagement.Read.Directory' (to read Entra role definitions)
            2. 'Application.Read.All' (to read the definitions of application permissions)
        - The credentials are expected to be available to AzTierWatcher via an environment variable with the following name and value:
            SP_CREDENTIALS_ENTRA = {"tenant_id": "__ID__", "client_id": "__ID__", "client_secret": "__SECRET__"}

"""
import datetime
import json
import os
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
    endpoint = 'https://graph.microsoft.com/v1.0/directoryRoleTemplates'
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(endpoint, headers = headers)

    if response.status_code != 200:
        print('FATAL ERROR - The Entra roles could not be retrieved from Graph.')
        exit()

    response_content = response.json()['value']
    return response_content


def get_builtin_entra_role_objects_from_graph_without_deprecated(token):
    """
        Retrieves the current built-in Entra role objects from MS Graph, excluding deprecated roles.

        References: 
            https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#deprecated-roles

        Args:
            str: a valid access token for MS Graph

        Returns:
            list(str): list of built-in Entra-role objects

    """
    current_built_in_role_objects = get_builtin_entra_role_objects_from_graph(token)
    deprecated_entra_roles = {
        'Device Join',
        'Device Managers',
        'Device Users',
        'Email Verified User Creator',
        'Mailbox Administrator',
        'Workplace Device Join'
    }
    current_builtin_roles = [role_object for role_object in current_built_in_role_objects if role_object['displayName'] not in deprecated_entra_roles]

    return current_builtin_roles


def get_builtin_azure_role_objects_from_arm(token):
    """
        Retrieves the current built-in Azure role objects from ARM.

        Args:
            str: a valid access token for ARM

        Returns:
            list(str): list of built-in Azure-role objects

    """
    endpoint = 'https://management.azure.com/providers/Microsoft.Authorization/roleDefinitions?api-version=2022-04-01'
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


def read_json_file(json_file):
    """
         Retrieves the content of the passed JSON file as a dictionary.

        Args:
            json_file(str): path to the local JSON file from which the content is to be retrieved

        Returns:
            dict(): the content of the passed JSON file
    """
    try:
        with open(json_file, 'r') as file:
            file_content = file.read()
            return json.loads(file_content)
    except FileNotFoundError:
        print('FATAL ERROR - The JSON file could not be retrieved.')
        exit()


def update_untiered(untiered_file, added_assets, removed_assets):
    """
        Updates the passed file providing an overview of untiered roles and permissions with the passed administrative assets.

        Args:
            untiered_file(str): the local Markdown file with untiered roles and permissions
            added_assets(list(dict)): the assets to be added to the 'addition' part of the untier file
            removed_assets(list(dict)): the assets to be added to the 'removal' part of the untier file

    """
    try:
        has_content_been_updated = False    
        update_type = untiered_file.rsplit('/', 2)[1]
        page_metadata_content = ''
        additions_content = ''
        removals_content = ''

        with open(untiered_file, 'r') as file:
            file_content = file.read()
            splitter = '###' 
            splitted_content = file_content.split(splitter)
            page_metadata_content = splitted_content[0]
            additions_content = splitter + splitted_content[1]
            removals_content = splitter + splitted_content[2]

        # Add to untiered additions   
        updated_additions_content = ''
        new_additions_content = ''
        splitter = '---|'
        splitted_additions_content = additions_content.rsplit(splitter, 1)
        additions_metadata_content = splitted_additions_content[0] + splitter
        current_additions_content = splitted_additions_content[1]
        current_additions_assets = set(current_additions_content.split('\n|')[1:])

        if current_additions_assets:
            assets_to_add = [asset for asset in added_assets if not str(current_additions_assets).find(asset['name'])]
            has_content_been_updated = True if len(assets_to_add) > 0 else False

            for asset in assets_to_add:
                date = asset['date']
                name = f"[{asset['name']}]({asset['link']})"
                description = asset['description']
                line = f"\n| {date} | {name} | {description} |"
                new_additions_content += line

        updated_additions_content = additions_metadata_content + new_additions_content + current_additions_content

        # Add to untiered removals
        updated_removals_content = ''
        new_removals_content = ''
        splitter = '---|'
        splitted_removals_content = removals_content.rsplit(splitter, 1)
        removals_metadata_content = splitted_removals_content[0] + splitter
        current_removals_content = splitted_removals_content[1]
        current_removals_assets = set(current_removals_content.split('\n|')[1:])

        if current_removals_assets:
            assets_to_remove = [asset for asset in removed_assets if not str(current_removals_assets).find(asset['name'])]

            if not has_content_been_updated:
                has_content_been_updated = True if len(assets_to_remove) > 0 else False      

            for asset in assets_to_remove:
                date = asset['date']
                name = asset['name']
                line = f"\n| {date} | {name} |"
                new_removals_content += line

        updated_removals_content = removals_metadata_content + new_removals_content + current_removals_content

        # Update the untiered file with the new content
        updated_content = page_metadata_content + updated_additions_content + updated_removals_content

        with open(untiered_file, 'w') as file:
            file.write(updated_content)

        if has_content_been_updated:
            print (f"{update_type}: changes have been detected")
        else:
            print (f"{update_type}: no changes")

    except FileNotFoundError:
        print('FATAL ERROR - The untiered file could not be updated.')
        exit()


def request_access_token(resource, tenant_id, client_id, client_secret):
    """
        Requests an access token for the passed resource on behalf of the service principal with the passed information.

        Args:
            resource (str): the resource to authenticate to (only valid values are: 'arm', 'graph')
            tenant_id (str): the id of the service principal's home tenant
            client_id (str): the application id of the service principal
            client_secret (str): a valid secret for the service principal
        
        Returns:
            str: a valid access token for the requested resource

    """
    valid_resources = ['arm', 'graph']

    if resource not in valid_resources:
        return

    endpoint = f"https://login.microsoftonline.com/{tenant_id}"
    body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    if resource == 'arm':
        endpoint += '/oauth2/token'
        body['resource'] = 'https://management.azure.com/'
    else:
        endpoint += '/oauth2/v2.0/token'
        body['scope'] = 'https://graph.microsoft.com/.default'

    response = requests.post(endpoint, body)

    if response.status_code != 200:
        print(f"FATAL ERROR - A token for {resource} could not be retrieved.")
        exit()

    access_token = response.json()['access_token']
    return access_token


if __name__ == "__main__":
    # Get access tokens for ARM and MS Graph
    raw_sp_credentials = os.environ['SP_CREDENTIALS_ENTRA']

    if not raw_sp_credentials:
        print('FATAL ERROR - A service principal with valid access to ARM and MS Graph is required.')
        exit()

    sp_credentials = json.loads(raw_sp_credentials)
    tenant_id = sp_credentials['tenant_id']
    client_id = sp_credentials['client_id']
    client_secret = sp_credentials['client_secret']

    graph_access_token = request_access_token('graph', tenant_id, client_id, client_secret)

    if not graph_access_token:
        print('FATAL ERROR - A valid access token for GRAPH is required.')
        exit()

    # Set Microsoft APIs info
    graph_role_template_base_uri = 'https://graph.microsoft.com/v1.0/directoryRoleTemplates/'
    arm_role_template_base_uri = 'https://management.azure.com'
    arm_role_template_api_version = '2022-04-01'

    # Get current built-in MS Graph application permissions
    current_builtin_msgraph_app_permissions = []
    current_builtin_msgraph_app_permission_objects = get_builtin_msgraph_app_permission_objects_from_graph(graph_access_token)

    for current_builtin_msgraph_app_permission_object in current_builtin_msgraph_app_permission_objects:
        current_builtin_msgraph_app_permissions.append({
            'id': current_builtin_msgraph_app_permission_object['id'],
            'name': current_builtin_msgraph_app_permission_object['value'],
            'description': current_builtin_msgraph_app_permission_object['displayName'],
            'link': f"{graph_role_template_base_uri}{current_builtin_msgraph_app_permission_object['id']}"
        })

    # Get current built-in Entra roles
    current_builtin_entra_roles = []
    current_builtin_entra_role_objects = get_builtin_entra_role_objects_from_graph_without_deprecated(graph_access_token)

    for current_builtin_entra_role_object in current_builtin_entra_role_objects:
        current_builtin_entra_roles.append({
            'id': current_builtin_entra_role_object['id'],
            'name': current_builtin_entra_role_object['displayName'],
            'description': current_builtin_entra_role_object['description'],
            'link': f"{graph_role_template_base_uri}{current_builtin_entra_role_object['id']}"
        })

    # Set local tier files
    github_action_dir_name = '.github'
    absolute_path_to_script = os.path.abspath(sys.argv[0])
    root_dir = absolute_path_to_script.split(github_action_dir_name)[0]
    entra_dir = root_dir + 'Entra roles'
    app_permissions_dir = root_dir + 'Microsoft Graph application permissions'
    entra_roles_tier_file = f"{entra_dir}/tiered-entra-roles.json"
    msgraph_app_permissions_tier_file = f"{app_permissions_dir}/tiered-msgraph-app-permissions.json"

    # Set local untiered files
    entra_roles_untiered_file = f"{entra_dir}/Untiered Entra roles.md"
    msgraph_app_permissions_untiered_file = f"{app_permissions_dir}/Untiered MSGraph application permissions.md"

    # Get tiered built-in roles/permissions from local files
    tiered_builtin_msgraph_app_permissions = read_json_file(msgraph_app_permissions_tier_file)
    tiered_builtin_entra_roles = read_json_file(entra_roles_tier_file)

    # Compare MS Graph application permissions
    current_permission_ids = [permission['id'] for permission in current_builtin_msgraph_app_permissions]
    tiered_permission_ids = [permission['id'] for permission in tiered_builtin_msgraph_app_permissions]
    added_permission_ids = [permission_id for permission_id in current_permission_ids if permission_id not in tiered_permission_ids]
    removed_permission_ids = [permission_id for permission_id in tiered_permission_ids if permission_id not in current_permission_ids]

    if added_permission_ids or removed_permission_ids:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        added_items = []
        removed_items = []

        for added_permission_id in added_permission_ids:
            msgraph_app_permissions_list = [permission for permission in current_builtin_msgraph_app_permissions if permission['id'] == added_permission_id]

            if not len(msgraph_app_permissions_list) == 1:
                print ('FATAL ERROR - Something is wrong with the addition of MS Graph app permissions.')
                exit() 

            msgraph_app_permission = msgraph_app_permissions_list[0]
            enriched_msgraph_app_permission = { 'date': date }
            enriched_msgraph_app_permission.update(msgraph_app_permission)
            added_items.append(enriched_msgraph_app_permission)

        for removed_permission_id in removed_permission_ids:
            msgraph_app_permissions_list = [permission for permission in tiered_builtin_msgraph_app_permissions if permission['id'] == removed_permission_id]

            if not len(msgraph_app_permissions_list) == 1:
                print ('FATAL ERROR - Something is wrong with the removal of MS Graph app permissions.')
                exit() 

            msgraph_app_permission = msgraph_app_permissions_list[0]
            enriched_msgraph_app_permission = { 'date': date }
            enriched_msgraph_app_permission.update(msgraph_app_permission)
            removed_items.append(enriched_msgraph_app_permission)

        update_untiered(msgraph_app_permissions_untiered_file, added_items, removed_items)
    else:
        print ('MS Graph app permissions: no changes')

    # Compare Entra roles
    current_role_ids = [role['id'] for role in current_builtin_entra_roles]
    tiered_role_ids = [role['id'] for role in tiered_builtin_entra_roles]
    added_role_ids = [role_id for role_id in current_role_ids if role_id not in tiered_role_ids]
    removed_role_ids = [role_id for role_id in tiered_role_ids if role_id not in current_role_ids]

    if added_role_ids or removed_role_ids:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        added_items = []
        removed_items = []

        for added_role_id in added_role_ids:
            entra_role_list = [role for role in current_builtin_entra_roles if role['id'] == added_role_id]

            if not len(entra_role_list) == 1:
                print ('FATAL ERROR - Something is wrong with the addition of Entra roles.')
                exit() 

            entra_role = entra_role_list[0]
            enriched_entra_role = { 'date': date }
            enriched_entra_role.update(entra_role)
            added_items.append(enriched_entra_role)

        for removed_role_id in removed_role_ids:
            entra_role_list = [role for role in current_builtin_entra_roles if role['id'] == added_role_id]

            if not len(entra_role_list) == 1:
                print ('FATAL ERROR - Something is wrong with the removal of Entra roles.')
                exit() 

            entra_role = entra_role_list[0]
            enriched_entra_role = { 'date': date }
            enriched_entra_role.update(entra_role)
            removed_items.append(enriched_entra_role)

        update_untiered(entra_roles_untiered_file, added_items, removed_items)
    else:
        print ('Entra roles: no changes')
