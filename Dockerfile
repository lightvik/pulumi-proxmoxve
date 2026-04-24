ARG PULUMI_VERSION=3.232.0
ARG PROXMOXVE_VERSION=8.0.0

FROM oraclelinux:10-slim

ARG PULUMI_VERSION
ARG PROXMOXVE_VERSION

RUN microdnf install -y \
        python3 \
        python3-pip \
        curl \
        tar \
        gzip \
    && microdnf clean all

RUN curl -fsSL "https://get.pulumi.com/releases/sdk/pulumi-v${PULUMI_VERSION}-linux-x64.tar.gz" \
    | tar -xz -C /usr/local/bin --strip-components=1

RUN pip3 install --no-cache-dir \
        pulumi \
        "pulumi-proxmoxve==${PROXMOXVE_VERSION}" \
        pydantic \
        pyyaml \
        jinja2

ENV PULUMI_BACKEND_URL=file:///workspace/pulumi-state
ENV PULUMI_CONFIG_PASSPHRASE=""
ENV PULUMI_PYTHON_CMD=python3
ENV PYTHONPATH=/workspace/sources

WORKDIR /workspace

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
