# 🌩️ Application permissions tiering

Tiering of Microsoft Graph application permissions **based on known attack paths**.

## 📃 Tier definition

**Important**: suspicious permissions that have not been tested are categorized as Tier-0 for safety and marked with "⚠️" until they are researched properly.

| Tag | Tier | Name | Definition | 
|---|---|---|---|
| 🔴 | 0 | [Family of Global Admins](#tier-0) | Permissions with a risk of having a direct or indirect path to Global Admin and full tenant takeover. |
| 🟠 | 1 | [Family of restricted Graph permissions](#tier-1) | Permissions with write access to MS Graph scopes or read access to sensitive scopes (e.g. email content), but <u>without</u> a known path to Global Admin. |
| 🟢 | 2 | [Family of unprivileged Graph permission](#tier-2) | Permissions with read access to MS Graph scopes and little to no security implications. |


<a id='tier-0'></a>
## 🔴 Tier 0: Family of Global Admins

**Description**: permissions with a risk of having a direct or indirect path to Global Admin and full tenant takeover.

| Application permission | Path type | Known shortest path | Example |
|---|---|---|---|
| 📌 *Name of the MS Graph permission* | *"Direct" means the escalation requires a single step to become Global Admin. "Indirect" means the privilege escalation requires two or more steps.* | *One of the shortest paths possible to Global Admin that is known with the application permission. <br> It does **not** mean this is the most common or only possible path. In most cases, a large number of paths are possible, but the idea is to document one of the shortest to demonstrate the risk.* | *A concrete high-level example with a Threat Actor (TA), illustrating the "Known shortest path".* |
| [`AdministrativeUnit.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#administrativeunitreadwriteall) | Indirect | When combined with other types of access allowing to reset user passwords, can remove a Global Admin from a [Restricted Management Administrative Unit (RMAU)](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/admin-units-restricted-management) and take it over. | TA has acquired the ability to reset user passwords by other means, but [break-glass accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access) are protected in an RMAU. TA removes one of the accounts from the RMAU, resets the password of the [break-glass account](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access), and takes it over to escalate to Global Admin. |
| [`Application.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#applicationreadwriteall) <a id='application-readwrite-all'></a> | Indirect | Can impersonate any SP with more privileged application permissions granted for MS Graph, and impersonate it to escalate to Global Admin. | TA identifies an SP with the [`RoleManagement.ReadWrite.Directory`](#rolemanagement-readwrite-directory) application permission. TA creates a new secret for the SP, impersonates it and follows the same path as that permission to escalate to Global Admin. |
| [`Application.ReadWrite.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#applicationreadwriteownedby) | Indirect | Same as [`Application.ReadWrite.All`](#application-readwrite-all), but the impersonation is limited to the SP(s) for which the compromised SP is an owner. | Same as [`Application.ReadWrite.All`](#application-readwrite-all), but the impersonation is limited to the SP(s) for which the compromised SP is an owner. |
| [`AppRoleAssignment.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#approleassignmentreadwriteall) | Indirect | Can assign the [`RoleManagement.ReadWrite.Directory`](#rolemanagement-readwrite-directory) permission to the compromised SP *without* requiring admin consent, and escalate to Global Admin. | TA assigns the [`RoleManagement.ReadWrite.Directory`](#rolemanagement-readwrite-directory) permission to the compromised SP and follows the same path as that permission to escalate to Global Admin. |
| [`DelegatedAdminRelationship.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#delegatedadminrelationshipreadwriteall) | n/a | ⚠️ *Untested! Needs more research.* <br> Note: the tenant must be provisioned with the "Partner Customer Delegated Administration" SP already. Otherwise, the [`Application.ReadWrite.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#applicationreadwriteownedby) permission or higher will be required to create it ([more info](https://learn.microsoft.com/en-us/graph/api/tenantrelationship-post-delegatedadminrelationships?view=graph-rest-beta&tabs=http#permissions)). This is most-likely a required preliminary to any exploitation. | n/a |
| [`DeviceManagementConfiguration.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementconfigurationreadwriteall) <a id='devicemanagementconfiguration-readwrite-all'></a> | Indirect | Can run arbitrary commands on the InTune-managed endpoint of a Global Administrator and steal their tokens to impersonate them. | TA  identifies an InTune-managed endpoint belonging to a Global Administrator, runs commands remotely to extract PRT, refresh and/or access tokens issued for MS Graph from the endpoint, and uses those to escalate to Global Admin.  |
| [`DeviceManagementRBAC.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementrbacreadwriteall) | Indirect | Can assign InTune roles to a controlled user account, which allows running arbitrary commands on the InTune-managed endpoint of a Global Administrator and steal their tokens to impersonate them. | TA assigns the [School Administrator](https://learn.microsoft.com/en-us/mem/intune/fundamentals/role-based-access-control-reference#school-administrator) or [Help Desk Operator](https://learn.microsoft.com/en-us/mem/intune/fundamentals/role-based-access-control-reference#help-desk-operator) InTune role to a user account in their control, and the same path as [`DeviceManagementConfiguration.ReadWrite.All`](#devicemanagementconfiguration-readwrite-all) can be followed to escalate to Global Admin. |
| [`Directory.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#directoryreadwriteall) <a id='directory-readwrite-all'></a> | Indirect | Can become member of a non-role-assignable user group with assigned privileged Azure permissions, and leverage Azure resources to escalate to Global Admin. <br>**Note**: can also acquire access to external solutions integrated with Entra ID via SSO, and providing access based on non-role-assignable group memberships. | TA adds a controlled user account to a group with Contributor access to a subscription containing a resource with an assigned MI. The MI is granted [`Application.ReadWrite.All`](#application-readwrite-all) or similar, and the same path as that permissions can be followed to escalate to Global Admin. <br>Note: many other paths of this kind are possible. |
| [`Domain.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#domainreadwriteall) | Indirect | Can add a federated domain to Entra ID and authenticate as an existing Global Admin without password or MFA requirements. | TA adds a federated domain to Entra ID, by importing a certificate with the domain's public key. TA generates a SAML token for an existing Global Admin with an MFA claim and signs it with the private key. TA successfully authenticates as Global Admin, without MFA requirements. |
| [`EntitlementManagement.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#entitlementmanagementreadwriteall) | Indirect | Can update the assignment policy of an access package provisioning access to Global Admin, so that requesting the package without approval is possible from a controlled user account. | TA identifies an access package providing access to a security group with an active Global Admin assignment. TA adds an assignment policy to the access package, so that the latter can be requested from a controlled user account, without manual approval. TA requests the access package and escalates to Global Admin via group membership. |
| [`Group.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#groupreadwriteall) | Indirect | Same as [`Directory.ReadWrite.All`](#directory-readwrite-all). | Same as [`Directory.ReadWrite.All`](#directory-readwrite-all). |
| [`GroupMember.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#groupmemberreadwriteall) | Indirect | Same as [`Directory.ReadWrite.All`](#directory-readwrite-all). | Same as [`Directory.ReadWrite.All`](#directory-readwrite-all). |
| [`Organization.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#organizationreadwriteall) | Indirect | If Certificate Based Authentication (CBA) is enabled in the tenant, can upload a trusted root certificate to Entra ID and impersonate a Global Admin. | TA identifies the UPN of a Global admin. TA adds a trusted root certificate to Entra ID, and uses the associated private key to generate a user certificate for the UPN. TA authenticates with the user certificate to escalate to Global Admin. | 
| [`Policy.ReadWrite.AuthenticationMethod`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteauthenticationmethod) <a id='policy-readwrite-authenticationmethod'></a> | Indirect | When combined with [`UserAuthenticationMethod.ReadWrite.All`](#userauthenticationmethod-readwrite-all), can enable the [Temporary Access Pass (TAP)](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass) authentication method to help leveraging and follow the same path as that permission. | TA enables the TAP authentication method for the whole tenant and follows the same path as [`UserAuthenticationMethod.ReadWrite.All`](#userauthenticationmethod-readwrite-all). |
| [`Policy.ReadWrite.ConditionalAccess`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteconditionalaccess) | Direct | Can create a CAP blocking all users (including break-glass accounts) for all applications (making the tenant unavailable), and ask for a ransomware to remove the malicious CAP. <br>Note: this role is "Global-Admin-like", as it affects the availability of the tenant in the same way as a Global Admin. | TA creates a CAP blocking all users (including break-glass accounts) for all applications, and asks for a ransomware to remove the malicious CAP. |
| [`Policy.ReadWrite.PermissionGrant`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwritepermissiongrant) | Indirect | Can create a [permission grant policy](https://learn.microsoft.com/en-us/graph/api/permissiongrantpolicy-post-includes?view=graph-rest-1.0&tabs=http) for the compromised SP with the [`RoleManagement.ReadWrite.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadwritedirectory) permission, and leverage that policy to follow the same path as that permission and escalate to Global Admin. | TA creates a new [permission grant policy](https://learn.microsoft.com/en-us/graph/api/permissiongrantpolicy-post-permissiongrantpolicies?view=graph-rest-1.0&tabs=http) and updates it with a [condition set](https://learn.microsoft.com/en-us/graph/api/permissiongrantpolicy-post-includes?view=graph-rest-1.0&tabs=http) that includes the [`RoleManagement.ReadWrite.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadwritedirectory) permission and the compromised SP as the authorized client application of the policy. <br> Thanks to the policy, TA assigns the [`RoleManagement.ReadWrite.Directory`](#rolemanagement-readwrite-directory) permission to the compromised SP and creates the same path as that permission. |
| [`PrivilegedAccess.ReadWrite.AzureAD`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedaccessreadwriteazuread) | n/a | 🕰️ Legacy, kept here for safety until completely removed. <br> Note: seems to have been used with PIM iteration 1 and [2](https://learn.microsoft.com/en-us/graph/api/governanceroleassignmentrequest-post?view=graph-rest-beta&tabs=http) for Azure AD role assignments via delegated permissions. Does not seem to have ever been usable as application permission (only delegated). | n/a |
| [`PrivilegedAccess.ReadWrite.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedaccessreadwriteazureadgroup) <a id='privilegedaccess-readwrite-azureadgroup'></a> | Direct | Can add a controlled user account as owner or member of a group with an active Global Admin assignment (i.e. can update the membership of role-assignable groups). | TA adds a controlled user account to a group that is actively assigned the Global Admin role, re-authenticates with the account and escalates to Global Admin. <br>Note: if the active group assignment requires MFA, this path may need to be combined with [`RoleManagementPolicy.ReadWrite.AzureADGroup`](#rolemanagementpolicy-readwrite-azureadgroup) to be successful, depending on how the controlled user account was compromised. |
| [`PrivilegedAccess.ReadWrite.AzureResources`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedaccessreadwriteazureresources) | n/a | 🕰️ Legacy, kept here for safety until completely removed. <br> Note: seems to have been used with PIM iteration 1 and [2](https://learn.microsoft.com/en-us/graph/api/governanceroleassignmentrequest-post?view=graph-rest-beta&tabs=http) for Azure role assignments via delegated permissions. Does not seem to have ever been usable as application permission (only delegated). | n/a |
| [`PrivilegedAssignmentSchedule.ReadWrite.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedassignmentschedulereadwriteazureadgroup) <a id='privilegedassignmentschedule-readwrite-azureadgroup'></a> | Direct | Same as [`PrivilegedAccess.ReadWrite.AzureADGroup`](#privilegedaccess-readwrite-azureadgroup). | Same as [`PrivilegedAccess.ReadWrite.AzureADGroup`](#privilegedaccess-readwrite-azureadgroup). | 
| [`PrivilegedEligibilitySchedule.ReadWrite.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedeligibilityschedulereadwriteazureadgroup) <a id='privilegedeligibilityschedule-readwrite-azureadgroup'></a> | Indirect | Can make a controlled user account eligible to a group with an active Global Admin assignment, and activate the group membership to escalate to Global Admin. | TA makes a controlled user account eligible to a group that is actively assigned the Global Admin role, activates the group membership and escalates to Global Admin. <br>Note: if the eligible assignment or membership activation requires to meet specific requirements such as admin approval, this path needs to be combined with [`RoleManagementPolicy.ReadWrite.AzureADGroup`](#rolemanagementpolicy-readwrite-azureadgroup) to be successful. |
| [`RoleAssignmentSchedule.ReadWrite.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#roleassignmentschedulereadwritedirectory) <a id='roleassignmentschedule-readwrite-directory'></a> | Direct | Can assign the Global Admin role to a controlled user account, by creating an active PIM role assignment. | TA assigns the Global Admin role to a user account in their control (assigning to the compromised SP is not possible), re-authenticates with the user account and escalates to Global Admin. <br>Note: if the active role assignment requires MFA, this path may need to be combined with [`RoleManagementPolicy.ReadWrite.Directory`](#rolemanagementpolicy-readwrite-directory) to be successful, depending on how the controlled user account was compromised. |
| [`RoleEligibilitySchedule.ReadWrite.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#roleeligibilityschedulereadwritedirectory) <a id='roleeligibilityschedule-readwrite-directory'></a> | Indirect | Can make a controlled user account eligible to the Global Admin role, and activate it to escalate to Global Admin. | TA makes a controlled user account eligible to the Global Admin role, and activates it to escalate to Global Admin. <br> Note: if the eligible assignment or role activation requires to meet specific requirements such as admin approval, this path needs to be combined with [`RoleManagementPolicy.ReadWrite.Directory`](#rolemanagementpolicy-readwrite-directory) to be successful. |
| [`RoleManagement.ReadWrite.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadwritedirectory) <a id='rolemanagement-readwrite-directory'></a> | Direct | Can assign the Global Admin role to a controlled principal. | TA assigns the Global Admin role to the compromised SP, re-authenticates with the SP and escalates to Global Admin. |
| [`RoleManagementPolicy.ReadWrite.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementpolicyreadwriteazureadgroup) <a id='rolemanagementpolicy-readwrite-azureadgroup'></a> | Indirect | Can remove group role assignment and activation constrains, such as MFA requirements or admin approval, to help leveraging [`PrivilegedAccess.ReadWrite.AzureADGroup`](#privilegedaccess-readwrite-azureadgroup), [`PrivilegedAssignmentSchedule.ReadWrite.AzureADGroup`](#privilegedassignmentschedule-readwrite-azureadgroup) or [`PrivilegedEligibilitySchedule.ReadWrite.AzureADGroup`](#privilegedeligibilityschedule-readwrite-azureadgroup), and follow the same path as those permissions in a tenant with strict PIM settings. | TA identifies a group that is actively assigned the Global Admin role. In the group's role management policy, TA removes all assignment and activation requirements. TA adds a controlled user account to the group, re-authenticates with the account and escalates to Global Admin. |
| [`RoleManagementPolicy.ReadWrite.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementpolicyreadwritedirectory) <a id='rolemanagementpolicy-readwrite-directory'></a> | Indirect | Can remove Entra role assignment and activation constrains, such as MFA requirements or admin approval, to help leveraging [`RoleAssignmentSchedule.ReadWrite.Directory`](#roleassignmentschedule-readwrite-directory) or [`RoleEligibilitySchedule.ReadWrite.Directory`](#roleeligibilityschedule-readwrite-directory), and follow the same path as those permissions in a tenant with strict PIM settings. | TA has compromised user credentials for an account that is eligible to the Global Admin role. TA updates the role's management policy to remove all activation requirements. TA activates the role and escalates to Global Admin. |
| [`Synchronization.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#synchronizationreadwriteall) | n/a | ⚠️ *Untested! Needs more research.* <br> Note: does not seem to be able to create new SP credentials. | n/a |
| [`User.DeleteRestore.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userdeleterestoreall) | Direct | Can delete all user accounts in the tenant (making the latter unavailable), and ask for a ransomware to restore one of the break-glass accounts. <br>Note: this permission is "Global-Admin-like", as it affects the availability of the tenant in the same way as a Global Admin. | TA deletes all users in the tenant, including break-glass accounts, and ask for a ransom to restore one emergency account. <br>Note: TA has the ability to delete user accounts <u>permanently.</u> |
| [`User.EnableDisableAccount.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userenabledisableaccountall) | Direct | When combined with [`User.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userreadall), can disable all user accounts in the tenant (making the latter unavailable), and ask for a ransomware to re-enable one of the break-glass accounts. <br>Note: this permission is "Global-Admin-like", as it affects the availability of the tenant in the same way as a Global Admin. | TA disables all users in the tenant, including break-glass accounts, and ask for a ransom to re-enable one emergency account. |
| [`User.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userreadwriteall) | Indirect | Can edit sensitive properties of a controlled user account, such as "Employee ID" and "Department", to become member of a dynamic group with assigned privileged Azure permissions, and leverage Azure resources to escalate to Global Admin. | TA identifies a dynamic group with a membership rule based on a user property (e.g. department) and with assigned Contributor access to a subscription. TA updates the appropriate property of a controlled user account accordingly, to become part of the dynamic group. With the new Azure permissions, TA identifies a compute resource with an assigned MI granted [`Application.ReadWrite.All`](#application-readwrite-all) or similar, and the same path as that permission can be followed to escalate to Global Admin. <br>Note: many other paths of this kind are possible. |
| [`User-PasswordProfile.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#user-passwordprofilereadwriteall) | Indirect | Same as [`Directory.ReadWrite.All`](#directory-readwrite-all). | Same as [`Directory.ReadWrite.All`](#directory-readwrite-all). |
| [`UserAuthenticationMethod.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userauthenticationmethodreadwriteall) <a id='userauthenticationmethod-readwrite-all'></a> | Direct | Can generate a [Temporary Access Pass (TAP)](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass) and take over any user account in the tenant. <br> Note: if TAP is not an enabled authentication method in the tenant, this path needs to be combined with [`Policy.ReadWrite.AuthenticationMethod`](#policy-readwrite-authenticationmethod) to be successful. | TA creates a TAP for a [break-glass account](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access), authenticates with the TAP instead of the account's password and escalates to Global Admin. | 


<a id='tier-1'></a>
## 🟠 Tier 1: Family of restricted Graph permissions

**Description**: permissions with write access to MS Graph scopes or read access to sensitive scopes (e.g. email content), but <u>without</u> a known path to Global Admin.

| Application permission |
|---|
| [`AiEnterpriseInteraction.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#aienterpriseinteractionreadall) |
| [`APIConnectors.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#apiconnectorsreadwriteall) |
| [`AccessReview.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#accessreviewreadwriteall) |
| [`AccessReview.ReadWrite.Membership`](https://learn.microsoft.com/en-us/graph/permissions-reference#accessreviewreadwritemembership) |
| [`Agreement.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#agreementreadwriteall) |
| [`AppCatalog.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#appcatalogreadwriteall) |
| [`Application-RemoteDesktopConfig.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#application-remotedesktopconfigreadwriteall) |
| [`ApprovalSolution.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#approvalsolutionreadwriteall) |
| [`AttackSimulation.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#attacksimulationreadwriteall) |
| [`AuditLog.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlogreadall) |
| [`AuditLogsQuery-CRM.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlogsquery-crmreadall) |
| [`AuditLogsQuery-Endpoint.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlogsquery-endpointreadall) |
| [`AuditLogsQuery-Entra.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlogsquery-entrareadall) |
| [`AuditLogsQuery-Exchange.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlogsquery-exchangereadall) |
| [`AuditLogsQuery-OneDrive.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlogsquery-onedrivereadall) |
| [`AuditLogsQuery-SharePoint.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlogsquery-sharepointreadall) |
| [`AuditLogsQuery.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlogsqueryreadall) |
| [`AuthenticationContext.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#authenticationcontextreadwriteall) |
| [`BackupRestore-Configuration.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#backuprestore-configurationreadwriteall) |
| [`BackupRestore-Control.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#backuprestore-controlreadwriteall) |
| [`BackupRestore-Restore.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#backuprestore-restorereadwriteall) |
| [`BillingConfiguration.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#billingconfigurationreadwriteall) |
| [`BitlockerKey.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#bitlockerkeyreadall) |
| [`Bookings.Manage.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#bookingsmanageall) |
| [`Bookings.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#bookingsreadwriteall) |
| [`BookingsAppointment.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#bookingsappointmentreadwriteall) |
| [`BrowserSiteLists.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#browsersitelistsreadwriteall) |
| [`BusinessScenarioConfig.ReadWrite.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#businessscenarioconfigreadwriteownedby) |
| [`BusinessScenarioData.ReadWrite.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#businessscenariodatareadwriteownedby) |
| [`Calendars.ReadWrite`](https://learn.microsoft.com/en-us/graph/permissions-reference#calendarsreadwrite) |
| [`Calls.JoinGroupCall.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#callsjoingroupcallall) |
| [`Calls.JoinGroupCallAsGuest.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#callsjoingroupcallasguestall) |
| [`CallRecord-PstnCalls.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#callrecord-pstncallsreadall) |
| [`CallRecords.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#callrecordsreadall) |
| [`Channel.Delete.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#channeldeleteall) |
| [`ChannelMember.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#channelmemberreadwriteall) |
| [`ChannelMessage.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#channelmessagereadall) |
| [`ChannelSettings.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#channelsettingsreadwriteall) |
| [`Chat.ManageDeletion.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatmanagedeletionall) |
| [`Chat.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatreadall) |
| [`Chat.Read.WhereInstalled`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatreadwhereinstalled) |
| [`Chat.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatreadwriteall) |
| [`Chat.ReadWrite.WhereInstalled`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatreadwritewhereinstalled) |
| [`ChatMember.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatmemberreadwriteall) |
| [`ChatMember.ReadWrite.WhereInstalled`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatmemberreadwritewhereinstalled) |
| [`CloudPC.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#cloudpcreadwriteall) |
| [`Community.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#communityreadwriteall) |
| [`ConsentRequest.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#consentrequestreadwriteall) |
| [`Contacts.ReadWrite`](https://learn.microsoft.com/en-us/graph/permissions-reference#contactsreadwrite) |
| [`CrossTenantUserProfileSharing.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#crosstenantuserprofilesharingreadwriteall) |
| [`CustomAuthenticationExtension.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customauthenticationextensionreadwriteall) |
| [`CustomDetection.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customdetectionreadall) |
| [`CustomDetection.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customdetectionreadwriteall) |
| [`CustomSecAttributeAssignment.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customsecattributeassignmentreadwriteall) |
| [`CustomSecAttributeDefinition.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customsecattributedefinitionreadwriteall) |
| [`CustomSecAttributeProvisioning.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customsecattributeprovisioningreadwriteall) |
| [`CustomTags.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customtagsreadwriteall) |
| [`DelegatedPermissionGrant.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#delegatedpermissiongrantreadwriteall) |
| [`Device.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicereadwriteall) |
| [`DeviceLocalCredential.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicelocalcredentialreadall) |
| [`DeviceManagementApps.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementappsreadwriteall) |
| [`DeviceManagementCloudCA.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementcloudcareadwriteall) |
| [`DeviceManagementManagedDevices.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementmanageddevicesreadwriteall) |
| [`DeviceManagementServiceConfig.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementserviceconfigreadwriteall) |
| [`DeviceTemplate.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicetemplatereadwriteall) |
| [`DirectoryRecommendations.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#directoryrecommendationsreadwriteall) |
| [`EduAdministration.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#eduadministrationreadwriteall) |
| [`EduAssignments.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#eduassignmentsreadwriteall) |
| [`EduAssignments.ReadWriteBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#eduassignmentsreadwritebasicall) |
| [`EduCurricula.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#educurriculareadwriteall) |
| [`EduRoster.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#edurosterreadwriteall) |
| [`EventListener.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#eventlistenerreadwriteall) |
| [`ExternalConnection.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#externalconnectionreadwriteall) |
| [`ExternalConnection.ReadWrite.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#externalconnectionreadwriteownedby) |
| [`ExternalItem.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#externalitemreadwriteall) |
| [`ExternalItem.ReadWrite.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#externalitemreadwriteownedby) |
| [`ExternalUserProfile.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#externaluserprofilereadwriteall) |
| [`FileIngestion.Ingest`](https://learn.microsoft.com/en-us/graph/permissions-reference#fileingestioningest) |
| [`FileIngestionHybridOnboarding.Manage`](https://learn.microsoft.com/en-us/graph/permissions-reference#fileingestionhybridonboardingmanage) |
| [`Files.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#filesreadall) |
| [`Files.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#filesreadwriteall) |
| [`Files.ReadWrite.AppFolder`](https://learn.microsoft.com/en-us/graph/permissions-reference#filesreadwriteappfolder) |
| [`Group-Conversation.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#group-conversationreadall) |
| [`Group-Conversation.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#group-conversationreadwriteall) |
| [`Group.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#groupreadall) |
| [`HealthMonitoringAlert.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#healthmonitoringalertreadwriteall) |
| [`HealthMonitoringAlertConfig.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#healthmonitoringalertconfigreadwriteall) |
| [`IdentityProvider.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityproviderreadwriteall) |
| [`IdentityRiskEvent.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityriskeventreadwriteall) |
| [`IdentityRiskyServicePrincipal.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityriskyserviceprincipalreadwriteall) |
| [`IdentityRiskyUser.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityriskyuserreadwriteall) |
| [`IdentityUserFlow.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityuserflowreadwriteall) |
| [`IndustryData-DataConnector.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-dataconnectorreadwriteall) |
| [`IndustryData-DataConnector.Upload`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-dataconnectorupload) |
| [`IndustryData-InboundFlow.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-inboundflowreadwriteall) |
| [`IndustryData-OutboundFlow.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-outboundflowreadwriteall) |
| [`IndustryData-ReferenceDefinition.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-referencedefinitionreadwriteall) |
| [`IndustryData-SourceSystem.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-sourcesystemreadwriteall) |
| [`IndustryData-TimePeriod.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-timeperiodreadwriteall) |
| [`InformationProtectionContent.Sign.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#informationprotectioncontentsignall) |
| [`InformationProtectionContent.Write.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#informationprotectioncontentwriteall) |
| [`LearningAssignedCourse.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#learningassignedcoursereadwriteall) |
| [`LearningContent.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#learningcontentreadwriteall) |
| [`LearningSelfInitiatedCourse.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#learningselfinitiatedcoursereadwriteall) |
| [`LicenseAssignment.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#licenseassignmentreadwriteall) |
| [`LifecycleWorkflows.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#lifecycleworkflowsreadwriteall) |
| [`Mail.Read`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailread) |
| [`Mail.ReadBasic`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailreadbasic) |
| [`Mail.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailreadbasicall) |
| [`Mail.ReadWrite`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailreadwrite) |
| [`Mail.Send`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailsend) |
| [`MailboxFolder.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailboxfolderreadall) |
| [`MailboxFolder.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailboxfolderreadwriteall) |
| [`MailboxItem.ImportExport.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailboxitemimportexportall) |
| [`MailboxItem.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailboxitemreadall) |
| [`MailboxSettings.ReadWrite`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailboxsettingsreadwrite) |
| [`MultiTenantOrganization.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#multitenantorganizationreadwriteall) |
| [`MutualTlsOauthConfiguration.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#mutualtlsoauthconfigurationreadwriteall) |
| [`NetworkAccess.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#networkaccessreadwriteall) |
| [`NetworkAccessBranch.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#networkaccessbranchreadwriteall) |
| [`NetworkAccessPolicy.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#networkaccesspolicyreadwriteall) |
| [`Notes.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#notesreadall) |
| [`Notes.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#notesreadwriteall) |
| [`OnPremDirectorySynchronization.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onpremdirectorysynchronizationreadwriteall) | 
| [`OnPremisesPublishingProfiles.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onpremisespublishingprofilesreadwriteall) |
| [`OnlineMeetingAiInsight.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onlinemeetingaiinsightreadall) |
| [`OnlineMeetingAiInsight.Read.Chat`](https://learn.microsoft.com/en-us/graph/permissions-reference#onlinemeetingaiinsightreadchat) |
| [`OnlineMeetingRecording.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onlinemeetingrecordingreadall) |
| [`OnlineMeetings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onlinemeetingsreadall) |
| [`OnlineMeetings.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onlinemeetingsreadwriteall) |
| [`OnlineMeetingTranscript.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onlinemeetingtranscriptreadall) |
| [`OrgSettings-AppsAndServices.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-appsandservicesreadwriteall) |
| [`OrgSettings-DynamicsVoice.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-dynamicsvoicereadwriteall) |
| [`OrgSettings-Forms.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-formsreadwriteall) |
| [`OrgSettings-Microsoft365Install.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-microsoft365installreadwriteall) |
| [`OrgSettings-Todo.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-todoreadwriteall) |
| [`OrganizationalBranding.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#organizationalbrandingreadwriteall) |
| [`PartnerSecurity.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#partnersecurityreadwriteall) |
| [`PendingExternalUserProfile.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#pendingexternaluserprofilereadwriteall) |
| [`PeopleSettings.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#peoplesettingsreadwriteall) |
| [`PlaceDevice.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#placedevicereadwriteall) |
| [`PlaceDeviceTelemetry.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#placedevicetelemetryreadwriteall) |
| [`Policy.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadall) |
| [`Policy.Read.ConditionalAccess`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadconditionalaccess) |
| [`Policy.Read.DeviceConfiguration`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreaddeviceconfiguration) |
| [`Policy.ReadWrite.AccessReview`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteaccessreview) |
| [`Policy.ReadWrite.ApplicationConfiguration`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteapplicationconfiguration) |
| [`Policy.ReadWrite.AuthenticationFlows`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteauthenticationflows) |
| [`Policy.ReadWrite.Authorization`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteauthorization) |
| [`Policy.ReadWrite.ConsentRequest`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteconsentrequest) |
| [`Policy.ReadWrite.CrossTenantAccess`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwritecrosstenantaccess) |
| [`Policy.ReadWrite.DeviceConfiguration`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwritedeviceconfiguration) |
| [`Policy.ReadWrite.ExternalIdentities`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteexternalidentities) |
| [`Policy.ReadWrite.FeatureRollout`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwritefeaturerollout) |
| [`Policy.ReadWrite.FedTokenValidation`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwritefedtokenvalidation) |
| [`Policy.ReadWrite.IdentityProtection`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwriteidentityprotection) |
| [`Policy.ReadWrite.SecurityDefaults`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwritesecuritydefaults) |
| [`Policy.ReadWrite.TrustFramework`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadwritetrustframework) |
| [`Presence.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#presencereadwriteall) |
| [`PrintJob.Manage.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printjobmanageall) |
| [`PrintJob.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printjobreadall) |
| [`PrintJob.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printjobreadwriteall) |
| [`PrintJob.ReadWriteBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printjobreadwritebasicall) |
| [`PrintTaskDefinition.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printtaskdefinitionreadwriteall) |
| [`Printer.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printerreadwriteall) |
| [`PrivilegedAccess.Read.AzureAD`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedaccessreadazuread) |
| [`PrivilegedAccess.Read.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedaccessreadazureadgroup) |
| [`PrivilegedAccess.Read.AzureResources`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedaccessreadazureresources) |
| [`PrivilegedAssignmentSchedule.Read.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedassignmentschedulereadazureadgroup) |
| [`PrivilegedAssignmentSchedule.Remove.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedassignmentscheduleremoveazureadgroup) |
| [`PrivilegedEligibilitySchedule.Read.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedeligibilityschedulereadazureadgroup) |
| [`PrivilegedEligibilitySchedule.Remove.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#privilegedeligibilityscheduleremoveazureadgroup) |
| [`ProfilePhoto.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#profilephotoreadwriteall) |
| [`ProgramControl.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#programcontrolreadwriteall) |
| [`PublicKeyInfrastructure.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#publickeyinfrastructurereadwriteall) |
| [`RecordsManagement.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#recordsmanagementreadwriteall) |
| [`ReportSettings.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#reportsettingsreadwriteall) |
| [`RiskPreventionProviders.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#riskpreventionprovidersreadwriteall) |
| [`RoleAssignmentSchedule.Read.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#roleassignmentschedulereaddirectory) |
| [`RoleAssignmentSchedule.Remove.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#roleassignmentscheduleremovedirectory) |
| [`RoleEligibilitySchedule.Read.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#roleeligibilityschedulereaddirectory) |
| [`RoleEligibilitySchedule.Remove.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#roleeligibilityscheduleremovedirectory) |
| [`RoleManagement.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadall) |
| [`RoleManagement.Read.CloudPC`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadcloudpc) |
| [`RoleManagement.Read.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreaddirectory) |
| [`RoleManagement.Read.Exchange`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadexchange) |
| [`RoleManagement.ReadWrite.CloudPC`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadwritecloudpc) |
| [`RoleManagement.ReadWrite.Defender`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadwritedefender) | 
| [`RoleManagement.ReadWrite.Exchange`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreadwriteexchange) |
| [`RoleManagementAlert.Read.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementalertreaddirectory) |
| [`RoleManagementAlert.ReadWrite.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementalertreadwritedirectory) |
| [`RoleManagementPolicy.Read.AzureADGroup`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementpolicyreadazureadgroup) |
| [`RoleManagementPolicy.Read.Directory`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementpolicyreaddirectory) |
| [`Schedule-WorkingTime.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#schedule-workingtimereadwriteall) |
| [`Schedule.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#schedulereadwriteall) |
| [`SchedulePermissions.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#schedulepermissionsreadwriteall) |
| [`SearchConfiguration.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#searchconfigurationreadwriteall) |
| [`SecurityActions.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityactionsreadwriteall) |
| [`SecurityAlert.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityalertreadall) |
| [`SecurityAlert.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityalertreadwriteall) |
| [`SecurityAnalyzedMessage.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityanalyzedmessagereadwriteall) |
| [`SecurityEvents.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityeventsreadall) |
| [`SecurityEvents.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityeventsreadwriteall) |
| [`SecurityIdentitiesHealth.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityidentitieshealthreadwriteall) |
| [`SecurityIdentitiesSensors.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityidentitiessensorsreadwriteall) |
| [`SecurityIdentitiesUserActions.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityidentitiesuseractionsreadwriteall) |
| [`SecurityIncident.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityincidentreadall) |
| [`SecurityIncident.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityincidentreadwriteall) |
| [`ServicePrincipalEndpoint.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#serviceprincipalendpointreadwriteall) |
| [`SharePointTenantSettings.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#sharepointtenantsettingsreadwriteall) |
| [`ShortNotes.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#shortnotesreadall) |
| [`ShortNotes.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#shortnotesreadwriteall) |
| [`Sites.FullControl.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesfullcontrolall) |
| [`Sites.Manage.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesmanageall) |
| [`Sites.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesreadall) |
| [`Sites.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesreadwriteall) |
| [`Sites.Selected`](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesselected) |
| [`SpiffeTrustDomain.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#spiffetrustdomainreadwriteall) |
| [`SubjectRightsRequest.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#subjectrightsrequestreadwriteall) |
| [`SynchronizationData-User.Upload`](https://learn.microsoft.com/en-us/graph/permissions-reference#synchronizationdata-userupload) |
| [`Tasks.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#tasksreadwriteall) |
| [`Team.Create`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamcreate) |
| [`TeamMember.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teammemberreadwriteall) |
| [`TeamMember.ReadWriteNonOwnerRole.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teammemberreadwritenonownerroleall) |
| [`TeamsActivity.Send`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsactivitysend) |
| [`TeamsAppInstallation.ManageSelectedForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationmanageselectedforchatall) |
| [`TeamsAppInstallation.ManageSelectedForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationmanageselectedforteamall) |
| [`TeamsAppInstallation.ManageSelectedForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationmanageselectedforuserall) |
| [`TeamsAppInstallation.ReadWriteAndConsentForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteandconsentforchatall) |
| [`TeamsAppInstallation.ReadWriteAndConsentForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteandconsentforteamall) |
| [`TeamsAppInstallation.ReadWriteAndConsentForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteandconsentforuserall) |
| [`TeamsAppInstallation.ReadWriteAndConsentSelfForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteandconsentselfforchatall) |
| [`TeamsAppInstallation.ReadWriteAndConsentSelfForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteandconsentselfforteamall) |
| [`TeamsAppInstallation.ReadWriteAndConsentSelfForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteandconsentselfforuserall) |
| [`TeamsAppInstallation.ReadWriteForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteforchatall) |
| [`TeamsAppInstallation.ReadWriteForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteforteamall) |
| [`TeamsAppInstallation.ReadWriteForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteforuserall) |
| [`TeamsAppInstallation.ReadWriteSelectedForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteselectedforchatall) |
| [`TeamsAppInstallation.ReadWriteSelectedForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteselectedforteamall) |
| [`TeamsAppInstallation.ReadWriteSelectedForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteselectedforuserall) |
| [`TeamsAppInstallation.ReadWriteSelfForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteselfforchatall) |
| [`TeamsAppInstallation.ReadWriteSelfForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteselfforteamall) |
| [`TeamsAppInstallation.ReadWriteSelfForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadwriteselfforuserall) |
| [`TeamSettings.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsettingsreadwriteall) |
| [`TeamsPolicyUserAssign.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamspolicyuserassignreadwriteall) |
| [`TeamsTab.Create`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabcreate) |
| [`TeamsTab.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabreadall) |
| [`TeamsTab.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabreadwriteall) |
| [`TeamsTab.ReadWriteForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabreadwriteforchatall) |
| [`TeamsTab.ReadWriteForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabreadwriteforteamall) |
| [`TeamsTab.ReadWriteForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabreadwriteforuserall) |
| [`TeamsTab.ReadWriteSelfForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabreadwriteselfforchatall) |
| [`TeamsTab.ReadWriteSelfForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabreadwriteselfforteamall) |
| [`TeamsTab.ReadWriteSelfForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamstabreadwriteselfforuserall) |
| [`Teamwork.Migrate.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamworkmigrateall) |
| [`TeamworkAppSettings.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamworkappsettingsreadwriteall) |
| [`TeamworkDevice.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamworkdevicereadwriteall) |
| [`TeamworkTag.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamworktagreadwriteall) |
| [`TermStore.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#termstorereadwriteall) |
| [`ThreatAssessment.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#threatassessmentreadall) |
| [`ThreatHunting.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#threathuntingreadall) |
| [`ThreatIndicators.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#threatindicatorsreadall) |
| [`ThreatIndicators.ReadWrite.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#threatindicatorsreadwriteownedby) |
| [`ThreatIntelligence.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#threatintelligencereadall) |
| [`ThreatSubmission.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#threatsubmissionreadall) |
| [`ThreatSubmission.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#threatsubmissionreadwriteall) |
| [`ThreatSubmissionPolicy.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#threatsubmissionpolicyreadwriteall) |
| [`TrustFrameworkKeySet.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#trustframeworkkeysetreadwriteall) |
| [`User-ConvertToInternal.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#user-converttointernalreadwriteall) |
| [`User-LifeCycleInfo.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#user-lifecycleinforeadwriteall) |
| [`User-Mail.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#user-mailreadwriteall) |
| [`User-Phone.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#user-phonereadwriteall) |
| [`User.Export.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userexportall) |
| [`User.ManageIdentities.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#usermanageidentitiesall) |
| [`User.RevokeSessions.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userrevokesessionsall) |
| [`UserAuthMethod-Passkey.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userauthmethod-passkeyreadwriteall) |
| [`UserNotification.ReadWrite.CreatedByApp`](https://learn.microsoft.com/en-us/graph/permissions-reference#usernotificationreadwritecreatedbyapp) |
| [`UserShiftPreferences.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#usershiftpreferencesreadwriteall) |
| [`VirtualAppointment.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#virtualappointmentreadall) |
| [`VirtualAppointment.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#virtualappointmentreadwriteall) |
| [`VirtualEvent.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#virtualeventreadall) |
| [`VirtualEventRegistration-Anon.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#virtualeventregistration-anonreadwriteall) |
| [`WindowsUpdates.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#windowsupdatesreadwriteall) |
| [`WorkforceIntegration.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#workforceintegrationreadwriteall) |
| [`eDiscovery.ReadWrite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#ediscoveryreadwriteall) |


<a id='tier-2'></a>
## 🟢 Tier 2: Family of unprivileged Graph permissions

**Description**: Permissions with read access to MS Graph scopes and little to no security implications.

| Application permission |
|---|
| [`ApprovalSolution.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#approvalsolutionreadall) |
| [`APIConnectors.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#apiconnectorsreadall) |
| [`AccessReview.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#accessreviewreadall) |
| [`Acronym.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#acronymreadall) |
| [`AdministrativeUnit.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#administrativeunitreadall) |
| [`Agreement.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#agreementreadall) |
| [`AgreementAcceptance.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#agreementacceptancereadall) |
| [`AppCatalog.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#appcatalogreadall) |
| [`Application.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#applicationreadall) |
| [`AttackSimulation.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#attacksimulationreadall) |
| [`AuthenticationContext.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#authenticationcontextreadall) |
| [`BackupRestore-Configuration.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#backuprestore-configurationreadall) |
| [`BackupRestore-Control.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#backuprestore-controlreadall) |
| [`BackupRestore-Monitor.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#backuprestore-monitorreadall) |
| [`BackupRestore-Restore.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#backuprestore-restorereadall) |
| [`BackupRestore-Search.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#backuprestore-searchreadall) |
| [`BitlockerKey.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#bitlockerkeyreadbasicall) |
| [`Bookings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#bookingsreadall) |
| [`Bookmark.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#bookmarkreadall) |
| [`BrowserSiteLists.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#browsersitelistsreadall) |
| [`BusinessScenarioConfig.Read.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#businessscenarioconfigreadownedby) |
| [`BusinessScenarioData.Read.OwnedBy`](https://learn.microsoft.com/en-us/graph/permissions-reference#businessscenariodatareadownedby) |
| [`Calendars.Read`](https://learn.microsoft.com/en-us/graph/permissions-reference#calendarsread) |
| [`Calendars.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#calendarsreadbasicall) |
| [`CallEvents-Emergency.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#callevents-emergencyreadall) |
| [`CallEvents.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#calleventsreadall) |
| [`Calls.AccessMedia.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#callsaccessmediaall) |
| [`Calls.Initiate.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#callsinitiateall) |
| [`Calls.InitiateGroupCall.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#callsinitiategroupcallall) |
| [`ChangeManagement.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#changemanagementreadall) |
| [`Channel.Create`](https://learn.microsoft.com/en-us/graph/permissions-reference#channelcreate) |
| [`Channel.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#channelreadbasicall) |
| [`ChannelMember.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#channelmemberreadall) |
| [`ChannelMessage.UpdatePolicyViolation.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#channelmessageupdatepolicyviolationall) |
| [`ChannelSettings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#channelsettingsreadall) |
| [`Chat.Create`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatcreate) |
| [`Chat.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatreadbasicall) |
| [`Chat.ReadBasic.WhereInstalled`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatreadbasicwhereinstalled) |
| [`Chat.UpdatePolicyViolation.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatupdatepolicyviolationall) |
| [`ChatMember.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatmemberreadall) |
| [`ChatMember.Read.WhereInstalled`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatmemberreadwhereinstalled) |
| [`ChatMessage.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#chatmessagereadall) |
| [`CloudApp-Discovery.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#cloudapp-discoveryreadall) |
| [`CloudPC.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#cloudpcreadall) |
| [`Community.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#communityreadall) |
| [`ConsentRequest.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#consentrequestreadall) |
| [`Contacts.Read`](https://learn.microsoft.com/en-us/graph/permissions-reference#contactsread) |
| [`CrossTenantInformation.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#crosstenantinformationreadbasicall) |
| [`CrossTenantUserProfileSharing.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#crosstenantuserprofilesharingreadall) |
| [`CustomAuthenticationExtension.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customauthenticationextensionreadall) |
| [`CustomAuthenticationExtension.Receive.Payload`](https://learn.microsoft.com/en-us/graph/permissions-reference#customauthenticationextensionreceivepayload) |
| [`CustomSecAttributeAssignment.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customsecattributeassignmentreadall) |
| [`CustomSecAttributeAuditLogs.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customsecattributeauditlogsreadall) |
| [`CustomSecAttributeDefinition.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customsecattributedefinitionreadall) |
| [`CustomSecAttributeProvisioning.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customsecattributeprovisioningreadall) |
| [`CustomTags.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#customtagsreadall) |
| [`DelegatedAdminRelationship.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#delegatedadminrelationshipreadall) |
| [`DelegatedPermissionGrant.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#delegatedpermissiongrantreadall) |
| [`Device.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicereadall) |
| [`DeviceLocalCredential.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicelocalcredentialreadbasicall) |
| [`DeviceManagementApps.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementappsreadall) |
| [`DeviceManagementCloudCA.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementcloudcareadall) |
| [`DeviceManagementConfiguration.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementconfigurationreadall) |
| [`DeviceManagementManagedDevices.PrivilegedOperations.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementmanageddevicesprivilegedoperationsall) |
| [`DeviceManagementManagedDevices.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementmanageddevicesreadall) |
| [`DeviceManagementRBAC.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementrbacreadall) |
| [`DeviceManagementServiceConfig.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicemanagementserviceconfigreadall) |
| [`DeviceTemplate.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#devicetemplatereadall) |
| [`Directory.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#directoryreadall) |
| [`DirectoryRecommendations.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#directoryrecommendationsreadall) |
| [`Domain.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#domainreadall) |
| [`EduAdministration.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#eduadministrationreadall) |
| [`EduAssignments.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#eduassignmentsreadall) |
| [`EduAssignments.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#eduassignmentsreadbasicall) |
| [`EduCurricula.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#educurriculareadall) |
| [`EduReports-Reading.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#edureports-readingreadall) |
| [`EduReports-Reading.ReadAnonymous.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#edureports-readingreadanonymousall) |
| [`EduReports-Reflect.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#edureports-reflectreadall) |
| [`EduReports-Reflect.ReadAnonymous.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#edureports-reflectreadanonymousall) |
| [`EduRoster.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#edurosterreadall) |
| [`EduRoster.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#edurosterreadbasicall) |
| [`EntitlementManagement.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#entitlementmanagementreadall) |
| [`EventListener.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#eventlistenerreadall) |
| [`ExternalConnection.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#externalconnectionreadall) |
| [`ExternalItem.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#externalitemreadall) |
| [`ExternalUserProfile.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#externaluserprofilereadall) |
| [`FileStorageContainer.Selected`](https://learn.microsoft.com/en-us/graph/permissions-reference#filestoragecontainerselected) |
| [`Files.SelectedOperations.Selected`](https://learn.microsoft.com/en-us/graph/permissions-reference#filesselectedoperationsselected) |
| [`Group.Create`](https://learn.microsoft.com/en-us/graph/permissions-reference#groupcreate) |
| [`GroupMember.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#groupmemberreadall) |
| [`HealthMonitoringAlert.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#healthmonitoringalertreadall) |
| [`HealthMonitoringAlertConfig.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#healthmonitoringalertconfigreadall) |
| [`IdentityProvider.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityproviderreadall) |
| [`IdentityRiskEvent.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityriskeventreadall) |
| [`IdentityRiskyServicePrincipal.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityriskyserviceprincipalreadall) |
| [`IdentityRiskyUser.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityriskyuserreadall) |
| [`IdentityUserFlow.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#identityuserflowreadall) |
| [`IndustryData-DataConnector.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-dataconnectorreadall) |
| [`IndustryData-InboundFlow.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-inboundflowreadall) |
| [`IndustryData-OutboundFlow.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-outboundflowreadall) |
| [`IndustryData-ReferenceDefinition.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-referencedefinitionreadall) |
| [`IndustryData-Run.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-runreadall) |
| [`IndustryData-SourceSystem.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-sourcesystemreadall) |
| [`IndustryData-TimePeriod.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydata-timeperiodreadall) |
| [`IndustryData.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#industrydatareadbasicall) |
| [`InformationProtectionConfig.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#informationprotectionconfigreadall) |
| [`InformationProtectionPolicy.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#informationprotectionpolicyreadall) |
| [`Insights-UserMetric.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#insights-usermetricreadall) |
| [`LearningAssignedCourse.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#learningassignedcoursereadall) |
| [`LearningContent.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#learningcontentreadall) |
| [`LearningSelfInitiatedCourse.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#learningselfinitiatedcoursereadall) |
| [`LifecycleWorkflows.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#lifecycleworkflowsreadall) |
| [`ListItems.SelectedOperations.Selected`](https://learn.microsoft.com/en-us/graph/permissions-reference#listitemsselectedoperationsselected) |
| [`Lists.SelectedOperations.Selected`](https://learn.microsoft.com/en-us/graph/permissions-reference#listsselectedoperationsselected) |
| [`MailboxSettings.Read`](https://learn.microsoft.com/en-us/graph/permissions-reference#mailboxsettingsread) |
| [`Member.Read.Hidden`](https://learn.microsoft.com/en-us/graph/permissions-reference#memberreadhidden) |
| [`MultiTenantOrganization.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#multitenantorganizationreadall) |
| [`MultiTenantOrganization.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#multitenantorganizationreadbasicall) |
| [`MutualTlsOauthConfiguration.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#mutualtlsoauthconfigurationreadall) |
| [`NetworkAccess-Reports.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#networkaccess-reportsreadall) |
| [`NetworkAccess.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#networkaccessreadall) |
| [`NetworkAccessBranch.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#networkaccessbranchreadall) |
| [`NetworkAccessPolicy.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#networkaccesspolicyreadall) |
| [`OnPremDirectorySynchronization.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onpremdirectorysynchronizationreadall) |
| [`OnlineMeetingArtifact.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#onlinemeetingartifactreadall) |
| [`OrgContact.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgcontactreadall) |
| [`OrgSettings-AppsAndServices.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-appsandservicesreadall) |
| [`OrgSettings-DynamicsVoice.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-dynamicsvoicereadall) |
| [`OrgSettings-Forms.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-formsreadall) |
| [`OrgSettings-Microsoft365Install.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-microsoft365installreadall) |
| [`OrgSettings-Todo.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#orgsettings-todoreadall) |
| [`Organization.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#organizationreadall) |
| [`OrganizationalBranding.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#organizationalbrandingreadall) |
| [`PartnerBilling.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#partnerbillingreadall) |
| [`PartnerSecurity.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#partnersecurityreadall) |
| [`PendingExternalUserProfile.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#pendingexternaluserprofilereadall) |
| [`People.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#peoplereadall) |
| [`PeopleSettings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#peoplesettingsreadall) |
| [`Place.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#placereadall) |
| [`PlaceDevice.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#placedevicereadall) |
| [`Policy.Read.IdentityProtection`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadidentityprotection) |
| [`Policy.Read.PermissionGrant`](https://learn.microsoft.com/en-us/graph/permissions-reference#policyreadpermissiongrant) |
| [`Presence.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#presencereadall) |
| [`PrintJob.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printjobreadbasicall) |
| [`PrintSettings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printsettingsreadall) |
| [`Printer.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#printerreadall) |
| [`ProfilePhoto.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#profilephotoreadall) |
| [`ProgramControl.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#programcontrolreadall) |
| [`PublicKeyInfrastructure.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#publickeyinfrastructurereadall) |
| [`QnA.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#qnareadall) |
| [`RecordsManagement.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#recordsmanagementreadall) |
| [`ReportSettings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#reportsettingsreadall) |
| [`Reports.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#reportsreadall) |
| [`ResourceSpecificPermissionGrant.ReadForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#resourcespecificpermissiongrantreadforchatall) |
| [`ResourceSpecificPermissionGrant.ReadForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#resourcespecificpermissiongrantreadforteamall) |
| [`ResourceSpecificPermissionGrant.ReadForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#resourcespecificpermissiongrantreadforuserall) |
| [`RoleManagement.Read.Defender`](https://learn.microsoft.com/en-us/graph/permissions-reference#rolemanagementreaddefender) |
| [`RiskPreventionProviders.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#riskpreventionprovidersreadall) |
| [`Schedule.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#schedulereadall) |
| [`SearchConfiguration.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#searchconfigurationreadall) |
| [`SecurityActions.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityactionsreadall) |
| [`SecurityAnalyzedMessage.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityanalyzedmessagereadall) |
| [`SecurityIdentitiesHealth.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityidentitieshealthreadall) |
| [`SecurityIdentitiesSensors.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityidentitiessensorsreadall) |
| [`SecurityIdentitiesUserActions.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#securityidentitiesuseractionsreadall) |
| [`ServiceActivity-Exchange.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#serviceactivity-exchangereadall) |
| [`ServiceActivity-Microsoft365Web.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#serviceactivity-microsoft365webreadall) |
| [`ServiceActivity-OneDrive.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#serviceactivity-onedrivereadall) |
| [`ServiceActivity-Teams.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#serviceactivity-teamsreadall) |
| [`ServiceHealth.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#servicehealthreadall) |
| [`ServiceMessage.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#servicemessagereadall) |
| [`ServicePrincipalEndpoint.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#serviceprincipalendpointreadall) |
| [`SharePointTenantSettings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#sharepointtenantsettingsreadall) |
| [`SpiffeTrustDomain.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#spiffetrustdomainreadall) |
| [`SubjectRightsRequest.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#subjectrightsrequestreadall) |
| [`Synchronization.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#synchronizationreadall) |
| [`Tasks.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#tasksreadall) |
| [`Team.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamreadbasicall) |
| [`TeamMember.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teammemberreadall) |
| [`TeamSettings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsettingsreadall) |
| [`TeamTemplates.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamtemplatesreadall) |
| [`TeamsActivity.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsactivityreadall) |
| [`TeamsAppInstallation.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadall) |
| [`TeamsAppInstallation.ReadForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadforchatall) |
| [`TeamsAppInstallation.ReadForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadforteamall) |
| [`TeamsAppInstallation.ReadForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadforuserall) |
| [`TeamsAppInstallation.ReadSelectedForChat.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadselectedforchatall) |
| [`TeamsAppInstallation.ReadSelectedForTeam.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadselectedforteamall) |
| [`TeamsAppInstallation.ReadSelectedForUser.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsappinstallationreadselectedforuserall) |
| [`TeamsUserConfiguration.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsuserconfigurationreadall) |
| [`TeamsResourceAccount.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamsresourceaccountreadall) |
| [`Teamwork.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamworkreadall) |
| [`TeamworkAppSettings.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamworkappsettingsreadall) |
| [`TeamworkDevice.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamworkdevicereadall) |
| [`TeamworkTag.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#teamworktagreadall) |
| [`TermStore.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#termstorereadall) |
| [`TrustFrameworkKeySet.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#trustframeworkkeysetreadall) |
| [`User-LifeCycleInfo.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#user-lifecycleinforeadall) |
| [`User.Invite.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userinviteall) |
| [`User.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userreadall) |
| [`User.ReadBasic.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userreadbasicall) |
| [`UserAuthenticationMethod.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userauthenticationmethodreadall) |
| [`UserAuthMethod-Passkey.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userauthmethod-passkeyreadall) |
| [`UserShiftPreferences.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#usershiftpreferencesreadall) |
| [`UserTeamwork.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#userteamworkreadall) |
| [`VirtualAppointmentNotification.Send`](https://learn.microsoft.com/en-us/graph/permissions-reference#virtualappointmentnotificationsend) |
| [`eDiscovery.Read.All`](https://learn.microsoft.com/en-us/graph/permissions-reference#ediscoveryreadall) |