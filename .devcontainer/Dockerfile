FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu24.04

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    ffmpeg \
    povray \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*