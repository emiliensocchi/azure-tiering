# 🌩️ Azure administrative tiering

Collection of personal tier models for Azure, Entra and Microsoft Graph administrative assets, **based on known attack paths**.


## 📌 Overview

| Available tier models | 
|---|
| ☁️ [Azure roles tiering](Azure%20roles) |
| 👤 [Entra roles tiering](Entra%20roles) |
| 🤖 [MS Graph application permissions tiering](Microsoft%20Graph%20application%20permissions) |


## 🎯 Objectives

> [!NOTE]
> See the [release post](https://www.emiliensocchi.io/tiering-entra-roles-and-application-permissions-based-on-attack-paths/) for full information

#### Objective 1: provide a better understanding of security implications

This project attempts to categorize roles and permissions within Azure and Microsoft Graph, **based on known attack paths**. The objective is to provide a better understanding of what a threat actor with those administrative permissions can do in terms of privilege escalation and other abuses, while providing a better understanding of the security implications of those assets.

#### Objective 2: provide a base for further development

The definition of a "tier" and its content is highly dependent on the business requirements, risk appetite and governance strategy of a company. The second objective of this project is to provide a base that can be adapted to develop company-specific tier models based on the same philosophy, but answering different requirements.


## 📃 Tier definitions

### ☁️ <u>[Azure roles](Azure%20roles/README.md)</u>

| Color | Tier | Name | Definition |
|---|---|---|---|
| 🔴 | 0 | [Family of privilege ascenders](Azure%20roles/README.md#tier-0) | Roles with a risk of privilege escalation via one or multiple resource types in scope. |
| 🟠 | 1 | [Family of lateral navigators](Azure%20roles/README.md#tier-1) | Roles with a risk of lateral movement via data-plane access to a specific resource type in scope, but with a limited risk for privilege escalation. |
| 🟡 | 2 | [Family of data explorers](Azure%20roles/README.md#tier-2) | Roles with data-plane access to a specific resource type in scope, but with a limited risk for lateral movement and without a risk for privilege escalation. |
| 🟢 | 3 | [Family of unprivileged Azure users](Azure%20roles/README.md#tier-3) | Roles with little to no security implications. | 

### 👤 <u>[Entra roles](Entra%20roles/README.md)</u>

| Color | Tier | Name | Definition |
|---|---|---|---|
| 🔴 | 0 | [Family of Global Admins](Entra%20roles/README.md#tier-0) | Roles with a risk of having a direct or indirect path to Global Admin and full tenant takeover. |
| 🟠 | 1 | [Family of M365 and restricted Entra Admins](Entra%20roles/README.md#tier-1) | Roles with full access to individual Microsoft 365 services, limited administrative access to Entra ID, or global read access across services, but <u>without</u> a known path to Global Admin. |
| 🟢 | 2 | [Family of unprivileged administrators](Entra%20roles/README.md#tier-2) | Roles with little to no security implications. |

### 🤖 <u>[MS Graph application permissions](Microsoft%20Graph%20application%20permissions/README.md)</u>

| Color | Tier | Name | Definition | 
|---|---|---|---|
| 🔴 | 0 | [Family of Global Admins](Microsoft%20Graph%20application%20permissions/README.md#tier-0) | Permissions with a risk of having a direct or indirect path to Global Admin and full tenant takeover. |
| 🟠 | 1 | [Family of restricted Graph permissions](Microsoft%20Graph%20application%20permissions/README.md#tier-1) | Permissions with write access to MS Graph scopes or read access to sensitive scopes (e.g. email content), but <u>without</u> a known path to Global Admin. |
| 🟢 | 2 | [Family of unprivileged Graph permissions](Microsoft%20Graph%20application%20permissions/README.md#tier-2) | Permissions with read access to MS Graph scopes and little to no security implications. |


## 🧱 Opiniated design

> [!NOTE]
> See the [release post](https://www.emiliensocchi.io/tiering-entra-roles-and-application-permissions-based-on-attack-paths/) for full information

#### Design choice 1: tiering based on known attack paths

This project tiers administrative assets in Azure, Entra and Microsoft Graph based on testing their effective capabilities. This means all information coming from role actions, permission names and Microsoft documentation is ignored as much as possible, as those do not always provide a reliable way to understand the effective capabilities of an asset.

#### Design choice 2: supporting assets based on maintenance capabilities

This project attempts to tier **all** Entra roles and MS Graph application permissions, while supporting **common** Azure roles only. The reason for the latter is due to the fast paced development and volatility of Azure services, which make the addition and removal of Azure roles too frequent for an approach that is not entirely automated.

**Entra roles** and **MS Graph application permissions** are scanned **every 24 hours** for detecting the addition of new roles and permissions by Microsoft. The latter are automatically added to the "untiered section" of their respective models, reviewed manually for possible attack paths, and added to the tier models once the analysis is completed.

Tiered **Azure roles** are static and are only updated if a common role is missing. The addition of new roles can be requested by creating an [issue](https://github.com/emiliensocchi/azure-tiering/issues) in this project. If the role is considered common enough, it will be reviewed for possible attack paths, and added to the Azure roles tier model accordingly.

#### Design choice 3: linking asset definitions to the official Microsoft documentation

For convenience when browsing the tier models without authenticated access to an Entra tenant, administrative assets are hyperlinked to their repective definitions in the Microsoft documentation, as long as the definition exists. Assets with an API definition, but *without* an entry in the Microsoft documentation are hyperlinked directly to their respective definitions in the MS Graph or ARM API instead.


## 🛠️ Integration

> [!TIP]
> See the [Internal Azure administrative tiering](https://github.com/emiliensocchi/azure-internal-tiering) project for inspiration

Each tier model is available in table format for human readability, as well as JSON format for machine consumption:

| Human-readable | Machine-consumable |
|---|---|
| [Azure roles tiering](Azure%20roles/README.md) | [`tiered-azure-roles.json`](Azure%20roles/tiered-azure-roles.json) |
| [Entra roles tiering](Entra%20roles/README.md) | [`tiered-entra-roles.json`](Entra%20roles/tiered-entra-roles.json) |
| [MS Graph application permissions tiering](Microsoft%20Graph%20application%20permissions/README.md) | [`tiered-msgraph-app-permissions.json`](Microsoft%20Graph%20application%20permissions/tiered-msgraph-app-permissions.json) |

By integrating this project with multiple tools, organizations can easily ensure that the same tiers are used across their entire technology stack, while centralizing tier definitions into a single place.


## 📢 Disclaimer

**This is a research project and is neither a flawless, nor a complete solution**. It uses some level of automation to detect the addition of new roles and permissions by Microsoft. The latter are reviewed and added to the relevant models as soon as possible, but the reader should keep in mind that **the maintenance of this project is based on best effort**. 

Furthermore, a categorization based on known attack paths is only as good as the research that has been conducted around those assets. **Administrative assets with undocumented attack paths may therefore be categorized inappropriately**. 

To limit the risk of having dangerous roles or permissions categorized inappropriately in lower tiers, the reader is recommended to adopt the following approach:
> When considering the adoption of a new role/permission in your own implementation of these models, verify if the role is already categorized as Tier-0 in this project. If that is <u>not</u> the case, test the **effective capabilities** of the role/permission to ensure it has not changed without warning from Microsoft. If its capabilities have changed, re-categorize the asset accordingly.
