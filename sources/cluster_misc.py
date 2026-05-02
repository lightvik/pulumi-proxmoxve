import pulumi
import pulumi_proxmoxve as proxmox

from models import (
    ClusterMiscConfig,
    ClusterOptionsSpec,
    HwMappingPciSpec,
    HwMappingUsbSpec,
    MetricsServerSpec,
    OciImageSpec,
    AptRepositorySpec,
    PoolMembershipSpec,
)


def build_cluster_options(
    spec: ClusterOptionsSpec,
    provider: proxmox.Provider,
) -> proxmox.cluster.Options:
    args: dict = {}
    if spec.bandwidth_limit_clone is not None:
        args["bandwidth_limit_clone"] = spec.bandwidth_limit_clone
    if spec.bandwidth_limit_default is not None:
        args["bandwidth_limit_default"] = spec.bandwidth_limit_default
    if spec.bandwidth_limit_migration is not None:
        args["bandwidth_limit_migration"] = spec.bandwidth_limit_migration
    if spec.bandwidth_limit_move is not None:
        args["bandwidth_limit_move"] = spec.bandwidth_limit_move
    if spec.bandwidth_limit_restore is not None:
        args["bandwidth_limit_restore"] = spec.bandwidth_limit_restore
    if spec.console is not None:
        args["console"] = spec.console
    if spec.crs_ha is not None:
        args["crs_ha"] = spec.crs_ha
    if spec.crs_ha_rebalance_on_start is not None:
        args["crs_ha_rebalance_on_start"] = spec.crs_ha_rebalance_on_start
    if spec.description is not None:
        args["description"] = spec.description
    if spec.email_from is not None:
        args["email_from"] = spec.email_from
    if spec.ha_shutdown_policy is not None:
        args["ha_shutdown_policy"] = spec.ha_shutdown_policy
    if spec.http_proxy is not None:
        args["http_proxy"] = spec.http_proxy
    if spec.keyboard is not None:
        args["keyboard"] = spec.keyboard
    if spec.language is not None:
        args["language"] = spec.language
    if spec.mac_prefix is not None:
        args["mac_prefix"] = spec.mac_prefix
    if spec.max_workers is not None:
        args["max_workers"] = spec.max_workers
    if spec.migration_cidr is not None:
        args["migration_cidr"] = spec.migration_cidr
    if spec.migration_type is not None:
        args["migration_type"] = spec.migration_type
    if spec.next_id is not None:
        ni = spec.next_id
        args["next_id"] = proxmox.cluster.OptionsNextIdArgs(
            lower=ni.lower,
            upper=ni.upper,
        )
    if spec.notify is not None:
        n = spec.notify
        args["notify"] = proxmox.cluster.OptionsNotifyArgs(
            ha_fencing_mode=n.ha_fencing_mode,
            ha_fencing_target=n.ha_fencing_target,
            package_updates=n.package_updates,
            package_updates_target=n.package_updates_target,
            replication=n.replication,
            replication_target=n.replication_target,
        )

    return proxmox.cluster.Options(
        "cluster-options",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_hw_mapping_pci(
    spec: HwMappingPciSpec,
    provider: proxmox.Provider,
):
    args: dict = {}
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.mediated_devices is not None:
        args["mediated_devices"] = spec.mediated_devices
    if spec.maps:
        if spec.legacy:
            args["maps"] = [
                proxmox.hardware.mapping.PciLegacyMapArgs(
                    id=m.id,
                    node=m.node,
                    path=m.path,
                    comment=m.comment,
                    iommu_group=m.iommu_group,
                    subsystem_id=m.subsystem_id,
                )
                for m in spec.maps
            ]
        else:
            args["maps"] = [
                proxmox.hardware.mapping.PciMapArgs(
                    id=m.id,
                    node=m.node,
                    path=m.path,
                    comment=m.comment,
                    iommu_group=m.iommu_group,
                    subsystem_id=m.subsystem_id,
                )
                for m in spec.maps
            ]

    if spec.legacy:
        return proxmox.hardware.mapping.PciLegacy(
            f"hw-mapping-pci-{spec.name}",
            name=spec.name,
            **args,
            opts=pulumi.ResourceOptions(provider=provider),
        )
    return proxmox.hardware.mapping.Pci(
        f"hw-mapping-pci-{spec.name}",
        name=spec.name,
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_hw_mapping_usb(
    spec: HwMappingUsbSpec,
    provider: proxmox.Provider,
):
    args: dict = {}
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.maps:
        if spec.legacy:
            args["maps"] = [
                proxmox.hardware.mapping.UsbLegacyMapArgs(
                    id=m.id,
                    node=m.node,
                    comment=m.comment,
                    path=m.path,
                )
                for m in spec.maps
            ]
        else:
            args["maps"] = [
                proxmox.hardware.mapping.UsbMapArgs(
                    id=m.id,
                    node=m.node,
                    comment=m.comment,
                    path=m.path,
                )
                for m in spec.maps
            ]

    if spec.legacy:
        return proxmox.hardware.mapping.UsbLegacy(
            f"hw-mapping-usb-{spec.name}",
            name=spec.name,
            **args,
            opts=pulumi.ResourceOptions(provider=provider),
        )
    return proxmox.hardware.mapping.Usb(
        f"hw-mapping-usb-{spec.name}",
        name=spec.name,
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_metrics_server(
    spec: MetricsServerSpec,
    provider: proxmox.Provider,
) -> proxmox.metrics.Server:
    args: dict = {}
    if spec.disable is not None:
        args["disable"] = spec.disable
    if spec.graphite_path is not None:
        args["graphite_path"] = spec.graphite_path
    if spec.graphite_proto is not None:
        args["graphite_proto"] = spec.graphite_proto
    if spec.influx_api_path_prefix is not None:
        args["influx_api_path_prefix"] = spec.influx_api_path_prefix
    if spec.influx_bucket is not None:
        args["influx_bucket"] = spec.influx_bucket
    if spec.influx_db_proto is not None:
        args["influx_db_proto"] = spec.influx_db_proto
    if spec.influx_max_body_size is not None:
        args["influx_max_body_size"] = spec.influx_max_body_size
    if spec.influx_organization is not None:
        args["influx_organization"] = spec.influx_organization
    if spec.influx_token is not None:
        args["influx_token"] = spec.influx_token
    if spec.influx_verify is not None:
        args["influx_verify"] = spec.influx_verify
    if spec.mtu is not None:
        args["mtu"] = spec.mtu
    if spec.opentelemetry_compression is not None:
        args["opentelemetry_compression"] = spec.opentelemetry_compression
    if spec.opentelemetry_headers is not None:
        args["opentelemetry_headers"] = spec.opentelemetry_headers
    if spec.opentelemetry_max_body_size is not None:
        args["opentelemetry_max_body_size"] = spec.opentelemetry_max_body_size
    if spec.opentelemetry_path is not None:
        args["opentelemetry_path"] = spec.opentelemetry_path
    if spec.opentelemetry_proto is not None:
        args["opentelemetry_proto"] = spec.opentelemetry_proto
    if spec.opentelemetry_resource_attributes is not None:
        args["opentelemetry_resource_attributes"] = spec.opentelemetry_resource_attributes
    if spec.opentelemetry_timeout is not None:
        args["opentelemetry_timeout"] = spec.opentelemetry_timeout
    if spec.opentelemetry_verify_ssl is not None:
        args["opentelemetry_verify_ssl"] = spec.opentelemetry_verify_ssl
    if spec.port is not None:
        args["port"] = spec.port
    if spec.server is not None:
        args["server"] = spec.server
    if spec.timeout is not None:
        args["timeout"] = spec.timeout
    if spec.type is not None:
        args["type"] = spec.type

    return proxmox.metrics.Server(
        f"metrics-server-{spec.name}",
        name=spec.name,
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_oci_image(
    spec: OciImageSpec,
    provider: proxmox.Provider,
) -> proxmox.oci.Image:
    args: dict = {
        "node_name": spec.node_name,
        "datastore_id": spec.datastore_id,
        "reference": spec.reference,
    }
    if spec.file_name is not None:
        args["file_name"] = spec.file_name
    if spec.overwrite is not None:
        args["overwrite"] = spec.overwrite
    if spec.overwrite_unmanaged is not None:
        args["overwrite_unmanaged"] = spec.overwrite_unmanaged
    if spec.upload_timeout is not None:
        args["upload_timeout"] = spec.upload_timeout

    return proxmox.oci.Image(
        f"oci-image-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_apt_repository(
    spec: AptRepositorySpec,
    provider: proxmox.Provider,
) -> proxmox.apt.Repository:
    args: dict = {
        "node": spec.node,
        "file_path": spec.file_path,
        "index": spec.index,
    }
    if spec.enabled is not None:
        args["enabled"] = spec.enabled

    return proxmox.apt.Repository(
        f"apt-repository-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_pool_membership(
    spec: PoolMembershipSpec,
    provider: proxmox.Provider,
) -> proxmox.pool.Membership:
    args: dict = {"pool_id": spec.pool_id}
    if spec.vm_id is not None:
        args["vm_id"] = spec.vm_id
    if spec.storage_id is not None:
        args["storage_id"] = spec.storage_id

    return proxmox.pool.Membership(
        f"pool-membership-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_cluster_misc(cfg: ClusterMiscConfig, provider: proxmox.Provider) -> None:
    if cfg.options is not None:
        build_cluster_options(cfg.options, provider)
    for spec in cfg.hw_mapping_pci:
        build_hw_mapping_pci(spec, provider)
    for spec in cfg.hw_mapping_usb:
        build_hw_mapping_usb(spec, provider)
    for spec in cfg.metrics_servers:
        build_metrics_server(spec, provider)
    for spec in cfg.oci_images:
        build_oci_image(spec, provider)
    for spec in cfg.apt_repositories:
        build_apt_repository(spec, provider)
    for spec in cfg.pool_memberships:
        build_pool_membership(spec, provider)
