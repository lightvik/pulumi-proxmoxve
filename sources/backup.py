import pulumi
import pulumi_proxmoxve as proxmox

from models import BackupJobSpec


def build_backup_job(
    spec: BackupJobSpec,
    provider: proxmox.Provider,
) -> proxmox.backup.Job:
    args: dict = {}
    if spec.resource_id is not None:
        args["resource_id"] = spec.resource_id
    if spec.storage is not None:
        args["storage"] = spec.storage
    if spec.schedule is not None:
        args["schedule"] = spec.schedule
    if spec.all is not None:
        args["all"] = spec.all
    if spec.vmids is not None:
        args["vmids"] = spec.vmids
    if spec.pool is not None:
        args["pool"] = spec.pool
    if spec.node is not None:
        args["node"] = spec.node
    if spec.enabled is not None:
        args["enabled"] = spec.enabled
    if spec.mode is not None:
        args["mode"] = spec.mode
    if spec.compress is not None:
        args["compress"] = spec.compress
    if spec.mailnotification is not None:
        args["mailnotification"] = spec.mailnotification
    if spec.mailtos is not None:
        args["mailtos"] = spec.mailtos
    if spec.notes_template is not None:
        args["notes_template"] = spec.notes_template
    if spec.exclude_paths is not None:
        args["exclude_paths"] = spec.exclude_paths
    if spec.fleecing is not None:
        args["fleecing"] = proxmox.backup.JobFleecingArgs(
            enabled=spec.fleecing.enabled,
            storage=spec.fleecing.storage,
        )
    if spec.performance is not None:
        args["performance"] = proxmox.backup.JobPerformanceArgs(
            max_workers=spec.performance.max_workers,
            pbs_entries_max=spec.performance.pbs_entries_max,
        )
    if spec.prune_backups is not None:
        args["prune_backups"] = spec.prune_backups
    if spec.bwlimit is not None:
        args["bwlimit"] = spec.bwlimit
    if spec.ionice is not None:
        args["ionice"] = spec.ionice
    if spec.lockwait is not None:
        args["lockwait"] = spec.lockwait
    if spec.maxfiles is not None:
        args["maxfiles"] = spec.maxfiles
    if spec.pigz is not None:
        args["pigz"] = spec.pigz
    if spec.stopwait is not None:
        args["stopwait"] = spec.stopwait
    if spec.zstd is not None:
        args["zstd"] = spec.zstd
    if spec.pbs_change_detection_mode is not None:
        args["pbs_change_detection_mode"] = spec.pbs_change_detection_mode
    if spec.protected is not None:
        args["protected"] = spec.protected
    if spec.remove is not None:
        args["remove"] = spec.remove
    if spec.repeat_missed is not None:
        args["repeat_missed"] = spec.repeat_missed
    if spec.script is not None:
        args["script"] = spec.script
    if spec.starttime is not None:
        args["starttime"] = spec.starttime
    if spec.stdexcludes is not None:
        args["stdexcludes"] = spec.stdexcludes
    if spec.tmpdir is not None:
        args["tmpdir"] = spec.tmpdir

    return proxmox.backup.Job(
        f"backup-job-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )
