ARG PULUMI_VERSION=3.246.0
ARG PROXMOXVE_VERSION=8.2.1
ARG TLS_VERSION=5.5.0
ARG PROJECT_VERSION=0.1.0

FROM oraclelinux:10-slim

ARG PULUMI_VERSION
ARG PROXMOXVE_VERSION
ARG TLS_VERSION
ARG PROJECT_VERSION

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
        "pulumi-tls==${TLS_VERSION}" \
        pydantic \
        pyyaml \
        jinja2 \
        rich \
        questionary

RUN pulumi plugin install resource proxmoxve ${PROXMOXVE_VERSION} \
        --server https://github.com/muhlba91/pulumi-proxmoxve/releases/download/v${PROXMOXVE_VERSION} \
 && pulumi plugin install resource tls ${TLS_VERSION}

ENV PULUMI_BACKEND_URL=file:///workspace/pulumi-state
ENV PULUMI_CONFIG_PASSPHRASE=""
ENV PULUMI_PYTHON_CMD=python3
ENV PYTHONPATH=/app/sources
ENV PULUMI_VERSION=${PULUMI_VERSION}
ENV PROXMOXVE_VERSION=${PROXMOXVE_VERSION}
ENV PROJECT_VERSION=${PROJECT_VERSION}

WORKDIR /workspace

COPY sources/ /app/sources/
COPY entrypoint.py /entrypoint.py
COPY render_helpers.py /render_helpers.py
RUN chmod +x /entrypoint.py

CMD ["python3", "/entrypoint.py"]
