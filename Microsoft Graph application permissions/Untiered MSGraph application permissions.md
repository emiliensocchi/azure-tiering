# ❔ Untiered MSGraph application permissions

This project uses some level of automation to detect the addition of new roles and permissions by Microsoft. The latter are reviewed and added to the relevant models as soon as possible, but the reader should keep in mind that **the maintenance of this project is based on best effort**.

## 🔎 Latest detections

The following changes have been detected through automation, **since the last update** of the tier model:

### ➕ Additions

| Detected on | Application permission | Description |
|---|---|---|
| 2025-03-26 | ConfigurationMonitoring.Read.All | Read all Configuration Monitoring entities |
| 2025-03-26 | ConfigurationMonitoring.ReadWrite.All | Read and write all Configuration Monitoring entities |
| 2025-03-26 | User.ReadWrite.CrossCloud | Read and write profiles of users that originate from an external cloud. |
| 2025-03-18 | EngagementConversation.Migration.All | Read and write all Viva Engage conversations |
| 2025-03-18 | EngagementRole.Read.All | Read all Viva Engage roles and role memberships |
| 2025-03-18 | EngagementRole.ReadWrite.All | Modify Viva Engage role membership |
| 2025-03-01 | [TeamsTelephoneNumber.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/39b17d18-680c-41f4-b9c2-5f30629e7cb6) | Read Tenant-Acquired Telephone Number Details |
| 2025-03-01 | [TeamsTelephoneNumber.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/0a42382f-155c-4eb1-9bdc-21548ccaa387) | Read and Modify Tenant-Acquired Telephone Number Details |
| 2025-01-30 | [DeviceManagementScripts.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/9255e99d-faf5-445e-bbf7-cb71482737c4) | Read and write Microsoft Intune Scripts |

### ❌ Removals

| Detected on | Application permission | Description |
|---|---|---|
