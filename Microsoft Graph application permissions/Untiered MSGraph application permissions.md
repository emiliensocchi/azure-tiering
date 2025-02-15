# ❔ Untiered MSGraph application permissions

This project uses some level of automation to detect the addition of new roles and permissions by Microsoft. The latter are reviewed and added to the relevant models as soon as possible, but the reader should keep in mind that **the maintenance of this project is based on best effort**.

## 🔎 Latest detections

The following changes have been detected through automation, **since the last update** of the tier model:

### ➕ Additions

| Detected on | Application permission | Description |
|---|---|---|
| 2025-02-15 | [CallDelegation.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/5aa33e77-b893-495e-bdc5-4bf6f27d42a0) | Read delegation settings |
| 2025-02-15 | [CallDelegation.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/8d06abce-e69b-4122-ba60-4f901bb1db2f) | Read and write delegation settings |
| 2025-02-15 | [LicenseAssignment.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/e2f98668-2877-4f38-a2f4-8202e0717aa1) | Read all license assignments. |
| 2025-02-15 | [LifecycleWorkflows-CustomExt.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/2cb19e7d-9012-40bf-9a22-69fc776af8b0) | Read all Lifecycle workflows custom task extensionss |
| 2025-02-15 | [LifecycleWorkflows-CustomExt.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/3351c766-bacc-4d93-94fa-f2c8b1986ee7) | Read and write all Lifecycle workflows custom task extensions |
| 2025-02-15 | [LifecycleWorkflows-Reports.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/fe615156-48b5-4c83-b613-e6e31a43c446) | Read all Lifecycle workflows reports |
| 2025-02-15 | [LifecycleWorkflows-Workflow.Activate](https://graph.microsoft.com/v1.0/directoryRoleTemplates/3a87a643-13d2-47aa-8d6a-b0a8377cb03b) | Run workflows on-demand in Lifecycle workflows |
| 2025-02-15 | [LifecycleWorkflows-Workflow.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/03b0ad3e-fc2b-4ef1-b0ff-252e865cb608) | Read all workflows in Lifecycle workflows |
| 2025-02-15 | [LifecycleWorkflows-Workflow.ReadBasic.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/021ea6db-c06b-45c6-8c9c-c1cd9a37a483) | List all workflows in Lifecycle workflows |
| 2025-02-15 | [LifecycleWorkflows-Workflow.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/94c88098-1d9d-4c42-a356-4d5a95312554) | Read and write all workflows in Lifecycle workflows |
| 2025-02-15 | [Sites.Archive.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/e3530185-4080-478c-a4ab-39322704df58) | Archive/reactivate Site Collections without a signed in user. |
| 2025-02-05 | [IndustryData-Run.Start](https://graph.microsoft.com/v1.0/directoryRoleTemplates/7e429772-5b5e-47c0-8fd6-7279294c8033) | View and start runs |
| 2025-02-05 | [SynchronizationData-User.Upload.OwnedBy](https://graph.microsoft.com/v1.0/directoryRoleTemplates/25c32ff3-849a-494b-b94f-20a8ac4e6774) | Upload user data to the identity sync service for apps that this application creates or owns |
| 2025-01-30 | [DeviceManagementScripts.Read.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/c7a5be92-2b3d-4540-8a67-c96dcaae8b43) | Read Microsoft Intune Scripts |
| 2025-01-30 | [DeviceManagementScripts.ReadWrite.All](https://graph.microsoft.com/v1.0/directoryRoleTemplates/9255e99d-faf5-445e-bbf7-cb71482737c4) | Read and write Microsoft Intune Scripts |
| 2025-01-30 | [DeviceTemplate.Create](https://graph.microsoft.com/v1.0/directoryRoleTemplates/abf6441f-0772-4932-96e7-0191478dd73a) | Create device template |

### ❌ Removals

| Detected on | Application permission | Description |
|---|---|---|
