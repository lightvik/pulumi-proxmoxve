import pulumi
import pulumi_proxmoxve as proxmox

from models import ClonedVmSpec


def build_cloned_vm(
    spec: ClonedVmSpec,
    provider: proxmox.Provider,
    depends_on: list | None = None,
) -> proxmox.cloned.VmLegacy | proxmox.cloned.Vm:
    ignore_changes: list[str] = []
    if spec.started == "keep":
        ignore_changes.append("started")
    opts = pulumi.ResourceOptions(
        provider=provider,
        depends_on=depends_on or [],
        ignore_changes=ignore_changes or None,
    )

    c = spec.clone

    if spec.legacy:
        clone_args = proxmox.cloned.VmLegacyCloneArgs(
            source_vm_id=c.source_vm_id,
            bandwidth_limit=c.bandwidth_limit,
            full=c.full,
            pool_id=c.pool_id,
            retries=c.retries,
            snapshot_name=c.snapshot_name,
            source_node_name=c.source_node_name,
            target_datastore=c.target_datastore,
            target_format=c.target_format,
        )
        vm_args: dict = {
            "clone": clone_args,
            "node_name": spec.node,
        }
        if spec.description is not None:
            vm_args["description"] = spec.description
        if spec.tags:
            vm_args["tags"] = spec.tags
        if spec.started is not None and spec.started != "keep":
            vm_args["started"] = spec.started
        if spec.stop_on_destroy is not None:
            vm_args["stop_on_destroy"] = spec.stop_on_destroy
        if spec.purge_on_destroy is not None:
            vm_args["purge_on_destroy"] = spec.purge_on_destroy
        if spec.delete_unreferenced_disks_on_destroy is not None:
            vm_args["delete_unreferenced_disks_on_destroy"] = (
                spec.delete_unreferenced_disks_on_destroy
            )
        return proxmox.cloned.VmLegacy(spec.name, **vm_args, opts=opts)

    clone_args_new = proxmox.cloned.VmCloneArgs(
        source_vm_id=c.source_vm_id,
        bandwidth_limit=c.bandwidth_limit,
        full=c.full,
        pool_id=c.pool_id,
        retries=c.retries,
        snapshot_name=c.snapshot_name,
        source_node_name=c.source_node_name,
        target_datastore=c.target_datastore,
        target_format=c.target_format,
    )
    vm_args_new: dict = {
        "clone": clone_args_new,
        "node_name": spec.node,
    }
    if spec.description is not None:
        vm_args_new["description"] = spec.description
    if spec.tags:
        vm_args_new["tags"] = spec.tags
    if spec.started is not None and spec.started != "keep":
        vm_args_new["started"] = spec.started
    if spec.stop_on_destroy is not None:
        vm_args_new["stop_on_destroy"] = spec.stop_on_destroy
    if spec.purge_on_destroy is not None:
        vm_args_new["purge_on_destroy"] = spec.purge_on_destroy
    if spec.delete_unreferenced_disks_on_destroy is not None:
        vm_args_new["delete_unreferenced_disks_on_destroy"] = (
            spec.delete_unreferenced_disks_on_destroy
        )
    return proxmox.cloned.Vm(spec.name, **vm_args_new, opts=opts)
