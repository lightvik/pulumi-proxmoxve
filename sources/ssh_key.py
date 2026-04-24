import pulumi_tls as tls


def build_ssh_key(resource_name: str = "ssh-key") -> tls.PrivateKey:
    return tls.PrivateKey(
        resource_name,
        algorithm="ED25519",
    )
