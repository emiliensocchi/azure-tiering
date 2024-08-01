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


def get_tiered_from_markdown(tier_file):
    """
         Retrieves the tiered roles or permissions from the passed file.

        Args:
            tier_file(str): the local file from which tiered roles/permissions are to be retrieved

        Returns: 
            list(str): the list of tiered roles or permissions

    """
    try:
        tiered_assets = []
        
        with open(tier_file, 'r') as file:
            file_content = file.read()
            tiered_content = ''.join(file_content.split('##')[2:])
            splitted_tiered_content = tiered_content.split('\n| [')[1:]

            for line in splitted_tiered_content:
                elements = line.split('|')
                asset_name = elements[0].split(']', 1)[0].strip('`')
                tiered_assets.append(asset_name)

        return tiered_assets
    except FileNotFoundError:
        print('FATAL ERROR - Retrieving tiered files has failed.')
        exit()


def update_untiered(untiered_file, added_assets, removed_assets):
    """
        Updates the passed file providing an overview of untiered roles and permissions with the passed administrative assets.

        Args:
            untiered_file(str): the local Markdown file with untiered roles and permissions
            added_assets(list(dict)): the assets to be added to 'addition' part the untier file
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
        assets_to_add = [asset for asset in added_assets if not asset['name'].split('[')[1].split(']')[0] in current_additions_assets]
        has_content_been_updated = True if len(assets_to_add) > 0 else False

        for asset in assets_to_add:
            date = asset['date']
            name = asset['name']
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
        assets_to_remove = [asset for asset in removed_assets if not asset['name'].split('[')[1].split(']')[0] in current_removals_assets] 
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

    # Get current built-in roles/permissions from APIs
    current_builtin_msgraph_app_permission_objects = get_builtin_msgraph_app_permission_objects_from_graph(graph_access_token)
    current_builtin_entra_role_objects = get_builtin_entra_role_objects_from_graph_without_deprecated(graph_access_token)
    current_builtin_msgraph_app_permissions = sorted([permission_object['value'] for permission_object in current_builtin_msgraph_app_permission_objects])
    current_builtin_entra_roles = sorted([role_object['displayName'] for role_object in current_builtin_entra_role_objects])

    # Set local tier files
    github_action_dir_name = '.github'
    absolute_path_to_script = os.path.abspath(sys.argv[0])
    root_dir = absolute_path_to_script.split(github_action_dir_name)[0]
    entra_dir = root_dir + 'Entra roles'
    app_permissions_dir = root_dir + 'Microsoft Graph application permissions'
    entra_roles_tier_file = f"{entra_dir}/README.md"
    msgraph_app_permissions_tier_file = f"{app_permissions_dir}/README.md"

    # Set local untiered files
    entra_roles_untiered_file = f"{entra_dir}/Untiered Entra roles.md"
    msgraph_app_permissions_untiered_file = f"{app_permissions_dir}/Untiered MSGraph application permissions.md"

    # Get tiered built-in roles/permissions from local files
    tiered_builtin_entra_roles = sorted(get_tiered_from_markdown(entra_roles_tier_file))
    tiered_builtin_msgraph_app_permissions = sorted(get_tiered_from_markdown(msgraph_app_permissions_tier_file))

    # Compare MS Graph application permissions
    current_permissions = set(current_builtin_msgraph_app_permissions)
    tiered_permissions = set(tiered_builtin_msgraph_app_permissions)
    added_permissions= [permission for permission in current_builtin_msgraph_app_permissions if permission not in tiered_permissions]
    removed_permissions = [permission for permission in tiered_builtin_msgraph_app_permissions if permission not in current_permissions]

    if added_permissions or removed_permissions:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        added_items = []
        removed_items = []

        for added_permission in added_permissions:
            msgraph_app_permission_object_list = [permission_object for permission_object in current_builtin_msgraph_app_permission_objects if permission_object['value'] == added_permission]

            if not len(msgraph_app_permission_object_list) == 1:
                print ('FATAL ERROR - Something is wrong with the addition of MS Graph app permissions.')
                exit() 

            msgraph_app_permission_object = msgraph_app_permission_object_list[0]
            name = msgraph_app_permission_object['value']
            link = f"https://graph.microsoft.com/v1.0/directoryRoleTemplates/{msgraph_app_permission_object['id']}"
            hyperlinked_name = f"[`{name}`]({link})"

            added_item = {
                'date': date,
                'name': hyperlinked_name,
                'description': msgraph_app_permission_object['displayName']
            }

            added_items.append(added_item)

        for removed_permission in removed_permissions:
            added_item = {
                'date': date,
                'name': f"`{removed_permission}`",
                'description': ''
            }
            
            removed_items.append(added_item)

        update_untiered(msgraph_app_permissions_untiered_file, added_items, removed_items)
    else:
        print ('MS Graph app permissions: no changes')

    # Compare Entra roles
    current_roles = set(current_builtin_entra_roles)
    tiered_roles = set(tiered_builtin_entra_roles)
    added_roles = [role for role in current_builtin_entra_roles if role not in tiered_roles]
    removed_roles = [role for role in tiered_builtin_entra_roles if role not in current_roles]

    if added_roles or removed_roles:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        added_items = []
        removed_items = []

        for added_role in added_roles:
            entra_role_object_list = [role_object for role_object in current_builtin_entra_role_objects if role_object['displayName'] == added_role]

            if not len(entra_role_object_list) == 1:
                print ('FATAL ERROR - Something is wrong with the addition of Entra roles.')
                exit() 

            entra_role_object = entra_role_object_list[0]
            name = entra_role_object['displayName']
            link = f"https://graph.microsoft.com/v1.0/directoryRoleTemplates/{entra_role_object['id']}"
            hyperlinked_name = f"[{name}]({link})"

            added_item = {
                'date': date,
                'name': hyperlinked_name,
                'description': entra_role_object['description']
            }

            added_items.append(added_item)

        for removed_role in removed_roles:
            added_item = {
                'date': date,
                'name': removed_role,
                'description': ''
            }
            
            removed_items.append(added_item)

        update_untiered(entra_roles_untiered_file, added_items, removed_items)
    else:
        print ('Entra roles: no changes')
