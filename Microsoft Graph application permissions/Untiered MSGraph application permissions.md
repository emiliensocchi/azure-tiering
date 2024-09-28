# ❔ Untiered MSGraph application permissions

This project uses some level of automation to detect the addition of new roles and permissions by Microsoft. The latter are reviewed and added to the relevant models as soon as possible, but the reader should keep in mind that **the maintenance of this project is based on best effort**.

## 🔎 Latest detections

The following changes have been detected through automation, **since the last update** of the tier model:

### ➕ Additions

| Detected on | Application permission | Description | 
|---|---|---|
| 2024-09-28 | [CallEvents-Emergency.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/f0a35f91-2aa6-4a99-9d5a-5b6bcb66204e) | Read all emergency call events |
| 2024-09-24 | [SecurityIdentitiesUserActions.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/3e5d0bee-973f-4736-a123-4e1ab146f3a8) | Read all identity security available user actions |
| 2024-09-24 | [SecurityIdentitiesUserActions.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/b4146a3a-dd4f-4af4-8d91-7cc0eef3d041) | Read and perform all identity security available user actions |
| 2024-09-17 | [AiEnterpriseInteraction.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/839c90ab-5771-41ee-aef8-a562e8487c1e) | Read all AI enterprise interactions. |
| 2024-09-17 | [ApprovalSolution.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/9f265de7-8d5e-4e9a-a805-5e8bbc49656f) | Read all approvals |
| 2024-09-17 | [ApprovalSolution.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/45583558-1113-4d06-8969-e79a28edc9ad) | Read all approvals and manage approval subscriptions |
| 2024-09-17 | [Bookings.Manage.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/6b22000a-1228-42ec-88db-b8c00399aecb) | Manage bookings information |
| 2024-09-17 | [Bookings.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/0c4b2d20-7919-468d-8668-c54b09d4dee8) | Read and write bookings information |
| 2024-09-17 | [Policy.Read.DeviceConfiguration](https://graph.microsoft.com/v1.0/directoryRoleTemplates/bdba4817-6ba1-4a7c-8a01-be9bc7c242dd) | Read your organization's device configuration policies |
| 2024-09-17 | [Policy.ReadWrite.DeviceConfiguration](https://graph.microsoft.com/v1.0/directoryRoleTemplates/230fb2d5-aa21-49c1-bfa7-ae1be179d867) | Read and write your organization's device configuration policies |
| 2024-09-17 | [PrivilegedAssignmentSchedule.Remove.AzureADGroup](https://graph.microsoft.com/v1.0/directoryRoleTemplates/55d1104b-3821-413d-b3ca-e2393d333cd3) | Delete assignment schedules for access to Azure AD groups |
| 2024-09-17 | [PrivilegedEligibilitySchedule.Remove.AzureADGroup](https://graph.microsoft.com/v1.0/directoryRoleTemplates/55745561-7572-4314-a737-a2c2a1b0dd2e) | Delete eligibility schedules for access to Azure AD groups |
| 2024-09-17 | [RoleAssignmentSchedule.Remove.Directory](https://graph.microsoft.com/v1.0/directoryRoleTemplates/d3495511-98b7-4df3-b317-4e35c19f6129) | Delete all active role assignments of your company's directory |
| 2024-09-17 | [RoleEligibilitySchedule.Remove.Directory](https://graph.microsoft.com/v1.0/directoryRoleTemplates/79c7e69c-0d9f-4eff-97a8-49170a5a08ba) | Delete all eligible role assignments of your company's directory |
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

### ❌ Removals

| Detected on | Application permission | Description | 
|---|---|---|
| 2024-09-17 | Directory.Write.Restricted |
