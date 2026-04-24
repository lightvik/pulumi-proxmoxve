import pulumi
import pulumi_proxmoxve as proxmox

from models import DownloadFileSpec


def build_download_file(
    spec: DownloadFileSpec,
    provider: proxmox.Provider,
) -> proxmox.download.File:
    args: dict = {
        "node_name": spec.node,
        "datastore_id": spec.datastore,
        "url": spec.url,
        "file_name": spec.filename,
        "content_type": spec.content_type,
    }
    if spec.checksum:
        args["checksum"] = spec.checksum
    if spec.checksum_algorithm:
        args["checksum_algorithm"] = spec.checksum_algorithm
    if spec.overwrite is not None:
        args["overwrite"] = spec.overwrite
    if spec.verify is not None:
        args["verify"] = spec.verify
    if spec.decompression_algorithm:
        args["decompression_algorithm"] = spec.decompression_algorithm

    return proxmox.download.File(
        f"download-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )
