# ❔ Untiered MS Graph application permissions

This project uses some level of automation to detect the addition of new roles and permissions by Microsoft. The latter are reviewed and added to the relevant models as soon as possible, but the reader should keep in mind that **the maintenance of this project is based on best effort**.

## 🔎 Latest detections

The following changes have been detected through automation, **since the last update** of the tier model:

### ➕ Additions

| Detected on | Application permission | Description |
|---|---|---|
| 2025-05-20 | AuditActivity.Read | Read activity audit log from the audit store. |
| 2025-05-20 | AuditActivity.Write | Upload activity audit logs to the audit store. |
| 2025-05-20 | Content.Process.All | Process content for data security, governance and compliance |
| 2025-05-20 | Content.Process.User | Process content for data security, governance and compliance |
| 2025-05-20 | ContentActivity.Read | Read contents activity audit log from the audit store. |
| 2025-05-20 | ContentActivity.Write | Upload content activity audit logs to the audit store. |
| 2025-05-20 | ProtectionScopes.Compute.All | Compute Purview policies at tenant scope |
| 2025-05-20 | ProtectionScopes.Compute.User | Compute Purview policies for an individual user |
| 2025-05-20 | ProvisioningLog.Read.All | Read all provisioning log data |
| 2025-05-20 | SensitivityLabel.Evaluate | Evaluate sensitivity labels |
| 2025-05-20 | SensitivityLabel.Read | Get labels application scope. |
| 2025-05-20 | SensitivityLabels.Read.All | Get labels tenant scope. |
| 2025-05-10 | Storyline.ReadWrite.All | Read and write all Viva Engage storylines |
| 2025-04-30 | Policy.ReadWrite.CrossTenantCapability | Read and write your organization's M365 cross tenant access capabilities |
| 2025-04-16 | WorkforceIntegration.Read.All | Read workforce integrations |
| 2025-03-26 | User.ReadWrite.CrossCloud | Read and write profiles of users that originate from an external cloud. |
| 2025-01-30 | DeviceManagementScripts.ReadWrite.All | Read and write Microsoft Intune Scripts |

### ❌ Removals

| Detected on | Application permission | Description |
|---|---|---|
