import pulumi
import pulumi_proxmoxve as proxmox

from models import (
    RbacConfig,
    RoleSpec,
    GroupSpec,
    UserSpec,
    UserTokenSpec,
    AclSpec,
    RealmLdapSpec,
    RealmOpenIdSpec,
    RealmSyncSpec,
)


def build_role(
    spec: RoleSpec,
    provider: proxmox.Provider,
) -> proxmox.RoleLegacy:
    args: dict = {}
    if spec.role_id is not None:
        args["role_id"] = spec.role_id
    if spec.privileges is not None:
        args["privileges"] = spec.privileges

    return proxmox.RoleLegacy(
        f"role-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_group(
    spec: GroupSpec,
    provider: proxmox.Provider,
) -> proxmox.GroupLegacy:
    args: dict = {}
    if spec.group_id is not None:
        args["group_id"] = spec.group_id
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.acls:
        args["acls"] = [
            proxmox.GroupLegacyAclArgs(
                path=a.path,
                role_id=a.role_id,
                propagate=a.propagate,
            )
            for a in spec.acls
        ]

    return proxmox.GroupLegacy(
        f"group-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_user(
    spec: UserSpec,
    provider: proxmox.Provider,
) -> proxmox.UserLegacy:
    args: dict = {}
    if spec.user_id is not None:
        args["user_id"] = spec.user_id
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.email is not None:
        args["email"] = spec.email
    if spec.enabled is not None:
        args["enabled"] = spec.enabled
    if spec.expiration_date is not None:
        args["expiration_date"] = spec.expiration_date
    if spec.first_name is not None:
        args["first_name"] = spec.first_name
    if spec.groups is not None:
        args["groups"] = spec.groups
    if spec.keys is not None:
        args["keys"] = spec.keys
    if spec.last_name is not None:
        args["last_name"] = spec.last_name
    if spec.password is not None:
        args["password"] = spec.password
    if spec.acls:
        args["acls"] = [
            proxmox.UserLegacyAclArgs(
                path=a.path,
                role_id=a.role_id,
                propagate=a.propagate,
            )
            for a in spec.acls
        ]

    return proxmox.UserLegacy(
        f"user-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_user_token(
    spec: UserTokenSpec,
    provider: proxmox.Provider,
) -> proxmox.user.Token:
    args: dict = {}
    if spec.user_id is not None:
        args["user_id"] = spec.user_id
    if spec.token_name is not None:
        args["token_name"] = spec.token_name
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.expiration_date is not None:
        args["expiration_date"] = spec.expiration_date
    if spec.privileges_separation is not None:
        args["privileges_separation"] = spec.privileges_separation

    return proxmox.user.Token(
        f"user-token-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_acl(
    spec: AclSpec,
    provider: proxmox.Provider,
) -> proxmox.AclLegacy:
    args: dict = {}
    if spec.path is not None:
        args["path"] = spec.path
    if spec.role_id is not None:
        args["role_id"] = spec.role_id
    if spec.user_id is not None:
        args["user_id"] = spec.user_id
    if spec.group_id is not None:
        args["group_id"] = spec.group_id
    if spec.token_id is not None:
        args["token_id"] = spec.token_id
    if spec.propagate is not None:
        args["propagate"] = spec.propagate

    return proxmox.AclLegacy(
        f"acl-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_realm_ldap(
    spec: RealmLdapSpec,
    provider: proxmox.Provider,
) -> proxmox.realm.Ldap:
    args: dict = {}
    if spec.realm is not None:
        args["realm"] = spec.realm
    if spec.server1 is not None:
        args["server1"] = spec.server1
    if spec.server2 is not None:
        args["server2"] = spec.server2
    if spec.port is not None:
        args["port"] = spec.port
    if spec.base_dn is not None:
        args["base_dn"] = spec.base_dn
    if spec.bind_dn is not None:
        args["bind_dn"] = spec.bind_dn
    if spec.bind_password is not None:
        args["bind_password"] = spec.bind_password
    if spec.user_attr is not None:
        args["user_attr"] = spec.user_attr
    if spec.user_classes is not None:
        args["user_classes"] = spec.user_classes
    if spec.group_dn is not None:
        args["group_dn"] = spec.group_dn
    if spec.group_classes is not None:
        args["group_classes"] = spec.group_classes
    if spec.group_filter is not None:
        args["group_filter"] = spec.group_filter
    if spec.group_name_attr is not None:
        args["group_name_attr"] = spec.group_name_attr
    if spec.filter is not None:
        args["filter"] = spec.filter
    if spec.sync_attributes is not None:
        args["sync_attributes"] = spec.sync_attributes
    if spec.sync_defaults_options is not None:
        args["sync_defaults_options"] = spec.sync_defaults_options
    if spec.mode is not None:
        args["mode"] = spec.mode
    if spec.ssl_version is not None:
        args["ssl_version"] = spec.ssl_version
    if spec.ca_path is not None:
        args["ca_path"] = spec.ca_path
    if spec.cert_path is not None:
        args["cert_path"] = spec.cert_path
    if spec.cert_key_path is not None:
        args["cert_key_path"] = spec.cert_key_path
    if spec.case_sensitive is not None:
        args["case_sensitive"] = spec.case_sensitive
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.default is not None:
        args["default"] = spec.default
    if spec.secure is not None:
        args["secure"] = spec.secure
    if spec.verify is not None:
        args["verify"] = spec.verify

    return proxmox.realm.Ldap(
        f"realm-ldap-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_realm_openid(
    spec: RealmOpenIdSpec,
    provider: proxmox.Provider,
) -> proxmox.realm.Openid:
    args: dict = {}
    if spec.realm is not None:
        args["realm"] = spec.realm
    if spec.issuer_url is not None:
        args["issuer_url"] = spec.issuer_url
    if spec.client_id is not None:
        args["client_id"] = spec.client_id
    if spec.client_key is not None:
        args["client_key"] = spec.client_key
    if spec.username_claim is not None:
        args["username_claim"] = spec.username_claim
    if spec.scopes is not None:
        args["scopes"] = spec.scopes
    if spec.acr_values is not None:
        args["acr_values"] = spec.acr_values
    if spec.prompt is not None:
        args["prompt"] = spec.prompt
    if spec.groups_claim is not None:
        args["groups_claim"] = spec.groups_claim
    if spec.autocreate is not None:
        args["autocreate"] = spec.autocreate
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.default is not None:
        args["default"] = spec.default
    if spec.groups_autocreate is not None:
        args["groups_autocreate"] = spec.groups_autocreate
    if spec.groups_overwrite is not None:
        args["groups_overwrite"] = spec.groups_overwrite
    if spec.query_userinfo is not None:
        args["query_userinfo"] = spec.query_userinfo

    return proxmox.realm.Openid(
        f"realm-openid-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_realm_sync(
    spec: RealmSyncSpec,
    provider: proxmox.Provider,
) -> proxmox.realm.Sync:
    args: dict = {}
    if spec.realm is not None:
        args["realm"] = spec.realm
    if spec.scope is not None:
        args["scope"] = spec.scope
    if spec.dry_run is not None:
        args["dry_run"] = spec.dry_run
    if spec.enable_new is not None:
        args["enable_new"] = spec.enable_new
    if spec.full is not None:
        args["full"] = spec.full
    if spec.purge is not None:
        args["purge"] = spec.purge
    if spec.remove_vanished is not None:
        args["remove_vanished"] = spec.remove_vanished

    return proxmox.realm.Sync(
        f"realm-sync-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_rbac(cfg: RbacConfig, provider: proxmox.Provider) -> None:
    for spec in cfg.roles:
        build_role(spec, provider)
    for spec in cfg.groups:
        build_group(spec, provider)
    for spec in cfg.users:
        build_user(spec, provider)
    for spec in cfg.user_tokens:
        build_user_token(spec, provider)
    for spec in cfg.acls:
        build_acl(spec, provider)
    for spec in cfg.realm_ldap:
        build_realm_ldap(spec, provider)
    for spec in cfg.realm_openid:
        build_realm_openid(spec, provider)
    for spec in cfg.realm_sync:
        build_realm_sync(spec, provider)
