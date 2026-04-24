import pulumi
import pulumi_proxmoxve as proxmox

from models import PoolSpec


def build_pool(
    spec: PoolSpec,
    provider: proxmox.Provider,
) -> proxmox.PoolLegacy:
    return proxmox.PoolLegacy(
        f"pool-{spec.id}",
        pool_id=spec.id,
        comment=spec.comment,
        opts=pulumi.ResourceOptions(provider=provider),
    )
