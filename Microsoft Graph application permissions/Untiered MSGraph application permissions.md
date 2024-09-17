# ❔ Untiered MSGraph application permissions

This project uses some level of automation to detect the addition of new roles and permissions by Microsoft. The latter are reviewed and added to the relevant models as soon as possible, but the reader should keep in mind that **the maintenance of this project is based on best effort**.

## 🔎 Latest detections

The following changes have been detected through automation, **since the last update** of the tier model:

### ➕ Additions

| Detected on | Application permission | Description | 
|---|---|---|
| 2024-08-27 | [BitlockerKey.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/57f1cf28-c0c4-4ec3-9a30-19a2eaaf2f6e) | Read all BitLocker keys |
| 2024-08-27 | [BitlockerKey.ReadBasic.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/f690d423-6b29-4d04-98c6-694c42282419) | Read all BitLocker keys basic information |
| 2024-08-27 | [MailboxFolder.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/99280d24-a782-4793-93cc-0888549957f6) | Read all the users' mailbox folders |
| 2024-08-27 | [MailboxFolder.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/fef87b92-8391-4589-9da7-eb93dab7dc8a) | Read and write all the users' mailbox folders |
| 2024-08-27 | [MailboxItem.ImportExport.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/76577085-e73d-4f1d-b26a-85fb33892327) | Allows the app to perform backup and restore for all mailbox items |
| 2024-08-27 | [MailboxItem.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/7d9f353d-a7bd-4fbb-822a-26d5dd39a3ce) | Read all the users' mailbox items |
| 2024-08-27 | [ResourceSpecificPermissionGrant.ReadForChat.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/2ff643d8-43e4-4a9b-88c1-86cb4a4b4c2f) | Read resource specific permissions granted on a chat |
| 2024-08-27 | [ResourceSpecificPermissionGrant.ReadForTeam.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/ad4600ae-d900-42cb-a9a2-2415d05593d0) | Read resource specific permissions granted on a team |
| 2024-08-27 | [User-Mail.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/280d0935-0796-47d1-8d26-273470a3f17a) | Read and write all secondary mail addresses for users |
| 2024-08-27 | [User-PasswordProfile.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/cc117bb9-00cf-4eb8-b580-ea2a878fe8f7) | Read and write all password profiles and reset user passwords |
| 2024-08-27 | [User-Phone.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/86ceff06-c822-49ff-989a-d912845ffe69) | Read and write all user mobile phone and business phones |
| 2024-08-27 | [User.DeleteRestore.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/eccc023d-eccf-4e7b-9683-8813ab36cecc) | Delete and restore all users |
| 2024-08-20 | [BackupRestore-Control.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/6fe20a79-0e15-45a1-b019-834c125993a0) | Read the status of the M365 backup service |
| 2024-08-20 | [BackupRestore-Control.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/fb240865-88f8-4a1d-923f-98dbc7920860) | Update or read the status of the M365 backup service |

