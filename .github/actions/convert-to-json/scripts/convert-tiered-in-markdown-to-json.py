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
import sys


def convert_markdown_to_json(markdown_file, json_file):
    """
        Converts the administrative-asset info located in the passed Markdown file to JSON, and outputs it to the passed JSON file.

        Args:
            markdown_file(str): the Markdown file to parse from
            json_file(str): the output file to which the converted JSON is exported to

        Returns:
            None

    """
    try:
        json_roles = []
        regex = r"(\[|\]|\(.*\)|\\u26a0\\ufe0f |\*|<br>|`|\\ud83d\\udd70\\ufe0f )"    # strips unwanted content in programmatic form
        
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
                json_role = {
                    "tier": "0", 
                    "assetName": re.sub(regex, '', elements[0].split(']', 1)[0]), 
                    "pathType": elements[1].strip(),
                    "knownShortestPath": re.sub(regex, '', elements[2]).encode('ascii', 'ignore').decode().strip(),
                    "example": re.sub(regex, '', elements[3].strip())
                }

                json_roles.append(json_role)

            # Parsing Tier-1 content
            splitted_tier_1_content = tier_1_content.split('\n| [')[1:]

            for line in splitted_tier_1_content:
                elements = line.split('|')

                if elements [1]:
                    json_role = {
                        "tier": "1", 
                        "assetName": re.sub(regex, '', elements[0].split(']', 1)[0]),
                        "providesFullAccessTo": re.sub(regex, '', elements[1].strip())
                    }
                else:
                    json_role = {
                        "tier": "1", 
                        "assetName": re.sub(regex, '', elements[0].split(']', 1)[0])
                    }

                json_roles.append(json_role)

            # Parsing Tier-2 content
            splitted_tier_2_content = tier_2_content.split('\n| [')[1:]

            for line in splitted_tier_2_content:
                elements = line.split('|')
                json_role = {
                    "tier": "2", 
                    "assetName": re.sub(regex, '', elements[0].split(']', 1)[0]),
                }

                json_roles.append(json_role)

        with open(json_file, "w") as file:
            file.write(json.dumps(json_roles, indent = 4))

    except FileNotFoundError:
        print('FATAL ERROR - Converting markdown to json has failed.')
        exit()


if __name__ == "__main__":
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

    all_markdown_files = [
        entra_roles_markdown_file,
        app_permissions_markdown_file
    ]

    all_json_files =[
        entra_roles_json_file,
        app_permissions_json_file
    ]

    for i in range(len(all_markdown_files)):
        markdown_file = all_markdown_files[i]
        markdown_file_name = markdown_file.rsplit('/', 2)[1]
        json_file = all_json_files[i]
        print (f"Converting for: {markdown_file_name}")
        convert_markdown_to_json(markdown_file, json_file)
