import pulumi
import pulumi_proxmoxve as proxmox

from models import UploadFileSpec


def build_upload_file(
    spec: UploadFileSpec,
    provider: proxmox.Provider,
) -> proxmox.FileLegacy:
    sf = spec.source_file
    source_file_args = proxmox.FileLegacySourceFileArgs(
        path=sf.path,
        checksum=sf.checksum,
        file_name=sf.file_name,
        insecure=sf.insecure,
    )

    args: dict = {
        "node_name": spec.node,
        "datastore_id": spec.datastore,
        "source_file": source_file_args,
    }
    if spec.content_type is not None:
        args["content_type"] = spec.content_type
    if spec.file_mode is not None:
        args["file_mode"] = spec.file_mode
    if spec.overwrite is not None:
        args["overwrite"] = spec.overwrite
    if spec.timeout_upload is not None:
        args["timeout_upload"] = spec.timeout_upload

    return proxmox.FileLegacy(
        f"upload-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )
