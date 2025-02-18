# 🌩️ Azure administrative tiering

Collection of personal tier models for Microsoft Graph and Azure administrative assets, **based on known attack paths**.

## 📌 Overview

| Available tier models |
|---|
| [Entra roles tiering](https://github.com/emiliensocchi/azure-tiering/tree/main/Entra%20roles) |
| [MS Graph application permissions tiering](https://github.com/emiliensocchi/azure-tiering/tree/main/Microsoft%20Graph%20application%20permissions) |

## 🎯 Objectives

> 📌 See the [release post](https://www.emiliensocchi.io/tiering-entra-roles-and-application-permissions-based-on-attack-paths/) for full information

#### Objective 1: provide a better understanding of security implications

This project attempts to categorize roles and permissions within Microsoft Graph and Azure, **based on known attack paths**. The objective is to provide a better understanding of what a threat actor with those administrative permissions can do in terms of privilege escalation, while providing a better understanding of the security implications of those assets.

#### Objective 2: provide a base for further development

The definition of a "tier" and its content is highly dependent on the business requirements, risk appetite and governance strategy of a company. The second objective of this project is to provide a base that can be adapted to develop company-specific tier models based on the same philosophy, but answering different requirements.

## 📃 Tier definitions

**Tier 0** contains assets with at least one known technique to create a path to Global Admin. This does **not** mean a path necessarily exist in every tenant, as privilege escalations are often tenant specific, but the goal is to identify roles and permissions with a **risk** of having a path to Global Admin. 

**Tier 1** contains administrative assets with limited write access, and *without* any known path to Global Admin. In case a new path is discovered for a Tier-1 asset, the latter is automatically bumped to Tier-0. 

**Tier 2** contains remaining roles and permissions with little to no security implications.

## 🧱 Opiniated design

> 📌 See the [release post](https://www.emiliensocchi.io/tiering-entra-roles-and-application-permissions-based-on-attack-paths/) for full information

This project tiers administrative assets in Microsoft Graph and Azure based on testing their effective capabilities. This means all information coming from role actions, permission names and Microsoft documentation is ignored as much as possible, as those do not provide a reliable way to be certain of what an asset is effectively capable of doing.

For convenience when browsing the tier models without authenticated access to an Entra tenant, administrative assets are hyperlinked to their repective definitions in the Microsoft documentation, as long as the definition exists. Assets with an API definition, but *without* an entry in the Microsoft documentation are hyperlinked directly to their respective definitions in the MS Graph or ARM API instead.

## 🤖 Integration

Each tier model is available in table format for human readability, as well as JSON format for machine consumption:

| Human-readable | Machine-consumable |
|---|---|
| [Entra roles tiering](https://github.com/emiliensocchi/azure-tiering/tree/main/Entra%20roles) | [`tiered-entra-roles.json`](https://github.com/emiliensocchi/azure-tiering/blob/main/Entra%20roles/tiered-entra-roles.json) |
| [MS Graph application permissions tiering](https://github.com/emiliensocchi/azure-tiering/tree/main/Microsoft%20Graph%20application%20permissions) | [`tiered-msgraph-app-permissions.json`](https://github.com/emiliensocchi/azure-tiering/blob/main/Microsoft%20Graph%20application%20permissions/tiered-msgraph-app-permissions.json) |

By integrating this project with multiple tools, organizations can easily ensure that the same Tiers are used across their entire technology stack, while centralizing tier definitions into a single place.

## 📢 Disclaimer

**This is a research project and is neither a flawless, nor a complete solution**. It uses some level of automation to detect the addition of new roles and permissions by Microsoft. The latter are reviewed and added to the relevant models as soon as possible, but the reader should keep in mind that **the maintenance of this project is based on best effort**.

Furthermore, a categorization based on known attack paths is only as good as the research that has been conducted around those assets. **Administrative assets with undocumented attack paths may therefore be categorized inappropriately**. 

To limit the risk of having dangerous roles or permissions categorized inappropriately in lower tiers, the reader is recommended to adopt the following approach:
> When considering the adoption of a new role/permission in your own implementation of these models, verify if the role is already categorized in Tier-0 in the original tiers from this project. If that is not the case, test the **effective capabilities** of the role/permission to ensure it has not changed without warning from Microsoft. If that is the case, re-categorize accordingly.
