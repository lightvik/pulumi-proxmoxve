import pulumi
import pulumi_proxmoxve as proxmox

from models import (
    StorageNfsSpec,
    StorageCifsSpec,
    StorageLvmSpec,
    StorageLvmThinSpec,
    StorageZfspoolSpec,
    StoragePbsSpec,
    StorageDirectorySpec,
    StorageConfig,
)


def _common(args: dict, spec) -> None:
    if spec.contents is not None:
        args["contents"] = spec.contents
    if spec.nodes is not None:
        args["nodes"] = spec.nodes
    if spec.disable is not None:
        args["disable"] = spec.disable


def build_storage_nfs(
    spec: StorageNfsSpec,
    provider: proxmox.Provider,
) -> proxmox.storage.Nfs:
    args: dict = {
        "resource_id": spec.resource_id,
        "server": spec.server,
        "export": spec.export,
    }
    _common(args, spec)
    if spec.backups is not None:
        args["backups"] = spec.backups
    if spec.options is not None:
        args["options"] = spec.options
    if spec.preallocation is not None:
        args["preallocation"] = spec.preallocation
    if spec.snapshot_as_volume_chain is not None:
        args["snapshot_as_volume_chain"] = spec.snapshot_as_volume_chain

    return proxmox.storage.Nfs(
        f"storage-nfs-{spec.resource_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_storage_cifs(
    spec: StorageCifsSpec,
    provider: proxmox.Provider,
) -> proxmox.storage.Cifs:
    args: dict = {
        "resource_id": spec.resource_id,
        "server": spec.server,
        "share": spec.share,
        "username": spec.username,
        "password": spec.password,
    }
    _common(args, spec)
    if spec.backups is not None:
        args["backups"] = spec.backups
    if spec.domain is not None:
        args["domain"] = spec.domain
    if spec.subdirectory is not None:
        args["subdirectory"] = spec.subdirectory
    if spec.preallocation is not None:
        args["preallocation"] = spec.preallocation
    if spec.snapshot_as_volume_chain is not None:
        args["snapshot_as_volume_chain"] = spec.snapshot_as_volume_chain

    return proxmox.storage.Cifs(
        f"storage-cifs-{spec.resource_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_storage_lvm(
    spec: StorageLvmSpec,
    provider: proxmox.Provider,
) -> proxmox.storage.Lvm:
    args: dict = {
        "resource_id": spec.resource_id,
        "volume_group": spec.volume_group,
    }
    _common(args, spec)
    if spec.shared is not None:
        args["shared"] = spec.shared
    if spec.wipe_removed_volumes is not None:
        args["wipe_removed_volumes"] = spec.wipe_removed_volumes

    return proxmox.storage.Lvm(
        f"storage-lvm-{spec.resource_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_storage_lvmthin(
    spec: StorageLvmThinSpec,
    provider: proxmox.Provider,
) -> proxmox.storage.Lvmthin:
    args: dict = {
        "resource_id": spec.resource_id,
        "volume_group": spec.volume_group,
        "thin_pool": spec.thin_pool,
    }
    _common(args, spec)

    return proxmox.storage.Lvmthin(
        f"storage-lvmthin-{spec.resource_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_storage_zfspool(
    spec: StorageZfspoolSpec,
    provider: proxmox.Provider,
) -> proxmox.storage.Zfspool:
    args: dict = {
        "resource_id": spec.resource_id,
        "zfs_pool": spec.zfs_pool,
    }
    _common(args, spec)
    if spec.blocksize is not None:
        args["blocksize"] = spec.blocksize
    if spec.thin_provision is not None:
        args["thin_provision"] = spec.thin_provision

    return proxmox.storage.Zfspool(
        f"storage-zfspool-{spec.resource_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_storage_pbs(
    spec: StoragePbsSpec,
    provider: proxmox.Provider,
) -> proxmox.storage.Pbs:
    args: dict = {
        "resource_id": spec.resource_id,
        "server": spec.server,
        "datastore": spec.datastore,
        "username": spec.username,
        "password": spec.password,
    }
    _common(args, spec)
    if spec.backups is not None:
        args["backups"] = spec.backups
    if spec.encryption_key is not None:
        args["encryption_key"] = spec.encryption_key
    if spec.fingerprint is not None:
        args["fingerprint"] = spec.fingerprint
    if spec.generate_encryption_key is not None:
        args["generate_encryption_key"] = spec.generate_encryption_key
    if spec.namespace is not None:
        args["namespace"] = spec.namespace

    return proxmox.storage.Pbs(
        f"storage-pbs-{spec.resource_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_storage_directory(
    spec: StorageDirectorySpec,
    provider: proxmox.Provider,
) -> proxmox.storage.Directory:
    args: dict = {
        "resource_id": spec.resource_id,
        "path": spec.path,
    }
    _common(args, spec)
    if spec.backups is not None:
        args["backups"] = spec.backups
    if spec.preallocation is not None:
        args["preallocation"] = spec.preallocation
    if spec.shared is not None:
        args["shared"] = spec.shared

    return proxmox.storage.Directory(
        f"storage-dir-{spec.resource_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_storages(cfg: StorageConfig, provider: proxmox.Provider) -> None:
    for spec in cfg.nfs:
        build_storage_nfs(spec, provider)
    for spec in cfg.cifs:
        build_storage_cifs(spec, provider)
    for spec in cfg.lvm:
        build_storage_lvm(spec, provider)
    for spec in cfg.lvmthin:
        build_storage_lvmthin(spec, provider)
    for spec in cfg.zfspool:
        build_storage_zfspool(spec, provider)
    for spec in cfg.pbs:
        build_storage_pbs(spec, provider)
    for spec in cfg.dir:
        build_storage_directory(spec, provider)
