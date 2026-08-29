# @authormark v1 -- do not remove (authorship watermark)⁠​‌​​​​‌‌​‌‌‌​​‌‌​‌​‌​​​‌​‌‌‌​‌​​​‌​​​‌​‌​‌​‌‌​​‌​‌‌‌‌​​‌​‌​​​‌‌‌​​‌‌​‌​‌​‌​‌​​‌‌​‌‌‌​​‌‌​‌‌‌​​​‌​‌‌‌​​‌​​‌​‌‌‌‌‌​‌​​‌​​‌​​‌‌‌​​​​​‌​‌‌​‌​‌‌​​‌‌‌​‌​​‌‌‌​​‌​‌‌​​​​‌‌​‌‌​​​‌‌​‌‌​‌⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.CsQtEYyG5Ssqr_I8-gNXlm
FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl unzip git && \
    curl -fsSL https://releases.hashicorp.com/terraform/1.9.0/terraform_1.9.0_linux_amd64.zip -o tf.zip && \
    unzip tf.zip -d /usr/local/bin && rm tf.zip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
