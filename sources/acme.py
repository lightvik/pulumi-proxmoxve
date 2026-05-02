import pulumi
import pulumi_proxmoxve as proxmox

from models import (
    AcmeConfig,
    AcmeDnsPluginSpec,
    AcmeAccountSpec,
    AcmeCertificateSpec,
    NodeCertificateSpec,
)


def build_acme_dns_plugin(
    spec: AcmeDnsPluginSpec,
    provider: proxmox.Provider,
) -> proxmox.acme.dns.Plugin:
    args: dict = {}
    if spec.plugin is not None:
        args["plugin"] = spec.plugin
    if spec.api is not None:
        args["api"] = spec.api
    if spec.data is not None:
        args["data"] = spec.data
    if spec.disable is not None:
        args["disable"] = spec.disable
    if spec.validation_delay is not None:
        args["validation_delay"] = spec.validation_delay
    if spec.digest is not None:
        args["digest"] = spec.digest

    return proxmox.acme.dns.Plugin(
        f"acme-dns-plugin-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_acme_account(
    spec: AcmeAccountSpec,
    provider: proxmox.Provider,
) -> proxmox.acme.Account:
    args: dict = {}
    if spec.contact is not None:
        args["contact"] = spec.contact
    if spec.directory is not None:
        args["directory"] = spec.directory
    if spec.eab_hmac_key is not None:
        args["eab_hmac_key"] = spec.eab_hmac_key
    if spec.eab_kid is not None:
        args["eab_kid"] = spec.eab_kid
    if spec.tos is not None:
        args["tos"] = spec.tos

    return proxmox.acme.Account(
        f"acme-account-{spec.name}",
        name=spec.name,
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_acme_certificate(
    spec: AcmeCertificateSpec,
    provider: proxmox.Provider,
):
    args: dict = {"node_name": spec.node_name}
    if spec.account is not None:
        args["account"] = spec.account
    if spec.force is not None:
        args["force"] = spec.force
    if spec.domains:
        if spec.legacy:
            args["domains"] = [
                proxmox.acme.CertificateLegacyDomainArgs(
                    domain=d.domain,
                    plugin=d.plugin,
                    alias=d.alias,
                )
                for d in spec.domains
            ]
        else:
            args["domains"] = [
                proxmox.acme.CertificateDomainArgs(
                    domain=d.domain,
                    plugin=d.plugin,
                    alias=d.alias,
                )
                for d in spec.domains
            ]

    if spec.legacy:
        return proxmox.acme.CertificateLegacy(
            f"acme-cert-{spec.name}",
            **args,
            opts=pulumi.ResourceOptions(provider=provider),
        )
    return proxmox.acme.Certificate(
        f"acme-cert-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_node_certificate(
    spec: NodeCertificateSpec,
    provider: proxmox.Provider,
) -> proxmox.CertificateLegacy:
    args: dict = {"node_name": spec.node_name}
    if spec.certificate is not None:
        args["certificate"] = spec.certificate
    if spec.certificate_chain is not None:
        args["certificate_chain"] = spec.certificate_chain
    if spec.private_key is not None:
        args["private_key"] = spec.private_key
    if spec.overwrite is not None:
        args["overwrite"] = spec.overwrite

    return proxmox.CertificateLegacy(
        f"node-cert-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_acme(cfg: AcmeConfig, provider: proxmox.Provider) -> None:
    for spec in cfg.dns_plugins:
        build_acme_dns_plugin(spec, provider)
    for spec in cfg.accounts:
        build_acme_account(spec, provider)
    for spec in cfg.certificates:
        build_acme_certificate(spec, provider)
    for spec in cfg.node_certificates:
        build_node_certificate(spec, provider)
