FROM ubuntu:22.04

RUN apt update && \
    apt install -y \
      build-essential \
      curl \
      vim \
      cmake \
      git \
      openjdk-8-jdk \
      maven \
      zip \
      unzip \
      && rm -rf /var/lib/apt/lists/*

# 4. 创建一个工作目录
WORKDIR /workspace

# 5. 容器启动时进入交互式 shell
CMD ["/bin/bash"]
