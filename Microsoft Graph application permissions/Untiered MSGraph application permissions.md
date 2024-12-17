# ❔ Untiered MSGraph application permissions

This project uses some level of automation to detect the addition of new roles and permissions by Microsoft. The latter are reviewed and added to the relevant models as soon as possible, but the reader should keep in mind that **the maintenance of this project is based on best effort**.

## 🔎 Latest detections

The following changes have been detected through automation, **since the last update** of the tier model:

### ➕ Additions

| Detected on | Application permission | Description | 
|---|---|---|
| 2024-12-17 | [RiskPreventionProviders.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/2a6baefd-edea-4ff6-b24e-bebcaa27a50d) | Read all identity risk prevention providers |
| 2024-12-17 | [RiskPreventionProviders.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/7fc7225d-eb37-4c39-90f3-a33a57cf1081) | Read and write all identity risk prevention providers |
| 2024-12-17 | [TeamsAppInstallation.ManageSelectedForChat.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/22b74aab-d9e4-46f7-9424-f24b42307227) | Manage installation and permission grants of selected Teams apps in all chats |
| 2024-12-17 | [TeamsAppInstallation.ManageSelectedForTeam.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/b448d252-1f26-4227-b6ff-21ab510975a2) | Manage installation and permission grants of selected Teams apps in all teams |
| 2024-12-17 | [TeamsAppInstallation.ManageSelectedForUser.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/e97a9235-5b3c-43c4-b37d-6786a173fae4) | Manage installation and permission grants of selected Teams apps for all user accounts |
| 2024-12-17 | [TeamsAppInstallation.ReadSelectedForChat.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/53d40ddb-9b27-4c97-b800-985be6041990) | Read selected installed Teams apps in all chats |
| 2024-12-17 | [TeamsAppInstallation.ReadSelectedForTeam.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/93c6a289-70fd-489e-a053-6cf8f7d772f6) | Read selected installed Teams apps in all teams |
| 2024-12-17 | [TeamsAppInstallation.ReadSelectedForUser.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/44fb0e7c-1f9a-47f1-bb9e-7f92d48ed288) | Read selected installed Teams apps for all users |
| 2024-12-17 | [TeamsAppInstallation.ReadWriteSelectedForChat.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/25bbeaad-04be-4207-83ed-a263aae76ddf) | Manage selected installed Teams apps in all chats |
| 2024-12-17 | [TeamsAppInstallation.ReadWriteSelectedForTeam.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/7b5823ae-d0f2-424d-b90c-d843ffada7d9) | Manage selected installed Teams apps in all teams |
| 2024-12-17 | [TeamsAppInstallation.ReadWriteSelectedForUser.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/650a76ec-4118-4b25-9d3a-1f98048a5ee0) | Manage selected Teams apps installed for all users |
| 2024-12-14 | [DeviceTemplate.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/dd9febb5-0c6d-419f-b256-3afe12c6adeb) | Read all device templates |
| 2024-12-14 | [DeviceTemplate.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/9fadb66e-6421-4744-aede-4ab6fb98a884) | Read and write all device templates |
| 2024-12-14 | [MutualTlsOauthConfiguration.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/6daaff82-2880-496d-9d80-57e8e31195e2) | Read all configurations used for mutual-TLS client authentication. |
| 2024-12-14 | [MutualTlsOauthConfiguration.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/78bbf8cf-07d8-45ba-b0eb-1a7b48efbcf1) | Read and write all configurations used for mutual-TLS client authentication. |
| 2024-11-23 | [FileIngestion.Ingest](https://graph.microsoft.com/v1.0/directoryRoleTemplates/65891b00-2fd9-4e33-be27-04a53132e3df) | Ingest SharePoint and OneDrive content to make it available in the search index |
| 2024-11-23 | [FileIngestionHybridOnboarding.Manage](https://graph.microsoft.com/v1.0/directoryRoleTemplates/766c601b-c009-4438-8290-c8b05fa00c4b) | Manage onboarding for a Hybrid Cloud tenant |
| 2024-11-23 | [RoleManagement.Read.Defender](https://graph.microsoft.com/v1.0/directoryRoleTemplates/4d6e30d1-e64e-4ae7-bf9d-c706cc928cef) | Read M365 Defender RBAC configuration |
| 2024-11-23 | [RoleManagement.ReadWrite.Defender](https://graph.microsoft.com/v1.0/directoryRoleTemplates/8b7e8c0a-7e9d-4049-97ec-04b5e1bcaf05) | Read M365 Defender RBAC configuration |
| 2024-11-23 | [UserAuthMethod-Passkey.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/72e00c1d-3e3d-43bb-a0b9-c435611bb1d2) | Read all users' passkey authentication methods |
| 2024-11-23 | [UserAuthMethod-Passkey.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/0400e371-7db1-4338-a269-96069eb65227) | Read and write all users' passkey authentication methods |
| 2024-10-23 | [ChangeManagement.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/418dae40-2b65-4819-900c-519a04e4d278) | Read Change Management items |
| 2024-10-16 | [CustomSecAttributeProvisioning.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/9fd1f8bf-a443-4df6-bc2a-5d00c5ec7828) | Read the provisioning configuration of all active custom security attributes |
| 2024-10-16 | [CustomSecAttributeProvisioning.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/1db69e9c-8d0a-498d-a5df-11fd0b68ceab) | Read and edit the provisioning configuration of all active custom security attributes |
| 2024-10-05 | [DeviceManagementCloudCA.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/315b6e8c-d92a-4691-919d-00ce76d1344a) | Read Microsoft Cloud PKI objects |
| 2024-10-05 | [DeviceManagementCloudCA.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/f15eb2ba-ef8a-4f70-991d-da5d045154e2) | Read and write Microsoft Cloud PKI objects |
| 2024-10-05 | [OnlineMeetingAiInsight.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/c0cf7895-985f-42d4-a693-b618f36674ad) | Read all AI Insights for online meetings. |
| 2024-10-05 | [OnlineMeetingAiInsight.Read.Chat](https://graph.microsoft.com/v1.0/directoryRoleTemplates/01892c31-3b66-4bcf-b5f5-bf0a03d5ed9f) | Read all AI Insights for online meetings where the Teams application is installed. |
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
