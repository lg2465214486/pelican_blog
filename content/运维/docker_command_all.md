Title: Docker命令大全
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: 操作命令
keywords: Docker常用命令大全
summary: 这是一份非常全面的 Docker 命令大全，包含了从基础到进阶的常用命令、参数解释和使用场景
lang: zh
status: published
Slug: docker_command_all
url: docker_command_all

---

### 第一部分：镜像管理

镜像是构建容器的基础，类似于虚拟机的模板。

| 命令 | 解释与细节 |
| :--- | :--- |
| `docker images` 或 `docker image ls` | 列出本地所有镜像。 |
| `docker search <image_name>` | 从 Docker Hub 搜索镜像。例如：`docker search nginx` |
| `docker pull <image_name>[:tag]` | 拉取（下载）镜像。不指定 tag 时默认为 `latest`。例如：`docker pull ubuntu:20.04` |
| `docker rmi <image_id>` 或 `docker image rm <image_id>` | 删除指定的本地镜像。 |
| `docker rmi $(docker images -q)` | **（小心！）** 删除所有本地镜像。 |
| `docker build -t <name:tag> <path>` | 根据指定路径的 Dockerfile 构建镜像。`-t` 用于给镜像打标签。例如：`docker build -t my-app:1.0 .` |
| `docker build -t <name:tag> -f <Dockerfile_path> .` | 使用指定路径的 Dockerfile 进行构建。 |
| `docker history <image_id>` | 查看镜像的构建历史层。 |
| `docker tag <source> <target>` | 给镜像打一个新的标签。例如：`docker tag my-app:1.0 my-registry.com/my-app:1.0` |
| `docker save -o <file.tar> <image>` | 将镜像保存为一个 tar 归档文件。例如：`docker save -o my-app.tar my-app:1.0` |
| `docker load -i <file.tar>` | 从 tar 归档文件加载镜像。 |

---

### 第二部分：容器生命周期管理

这是最核心的部分，涉及容器的创建、启动、停止和删除。

| 命令 | 解释与细节 |
| :--- | :--- |
| `docker run [options] <image> [command]` | **创建并启动**一个新容器。 |
| `docker create [options] <image> [command]` | 只创建容器但不启动。 |
| `docker start <container_id>` | 启动一个已停止的容器。 |
| `docker stop <container_id>` | **优雅地停止**一个运行中的容器（发送 SIGTERM，等待一段时间后 SIGKILL）。 |
| `docker restart <container_id>` | 重启容器。 |
| `docker kill <container_id>` | **强制立即停止**一个运行中的容器（发送 SIGKILL）。 |
| `docker pause <container_id>` | 暂停容器内的所有进程。 |
| `docker unpause <container_id>` | 恢复暂停的容器。 |
| `docker rm <container_id>` | 删除一个已停止的容器。 |
| `docker rm -f <container_id>` | **强制删除**一个容器（包括正在运行的）。 |
| `docker rm $(docker ps -aq)` | **（小心！）** 删除所有已停止的容器。 |
| `docker container prune` | 交互式地删除所有已停止的容器。 |
| `docker update --memory="512m" <container>` | 更新一个运行中容器的配置（如内存限制）。 |

#### `docker run` 的常用选项（非常重要）

| 选项 | 解释与细节 |
| :--- | :--- |
| `-d` 或 `--detach` | 在后台运行容器（守护进程模式）。 |
| `-it` | 交互模式运行容器，通常与 `-it` 连用，分配一个伪终端。例如：`docker run -it ubuntu bash` |
| `--name <name>` | 为容器指定一个名称，而不是使用随机 ID。 |
| `-p <host_port>:<container_port>` | 端口映射。例如：`-p 8080:80` 将容器的 80 端口映射到主机的 8080 端口。 |
| `-v <host_path>:<container_path>` | 挂载数据卷。例如：`-v /my/data:/var/lib/mysql` |
| `--network <network>` | 指定容器加入的网络。例如：`--network my-bridge` |
| `-e <KEY>=<VALUE>` | 设置环境变量。例如：`-e MYSQL_ROOT_PASSWORD=my-secret-pw` |
| `--rm` | 容器退出时自动删除它。非常适合一次性任务。 |
| `--restart=<policy>` | 设置重启策略（`no`, `on-failure`, `always`, `unless-stopped`）。 |

---

### 第三部分：查看与监控

用于查看容器状态、日志和资源使用情况。

| 命令 | 解释与细节 |
| :--- | :--- |
| `docker ps` | 列出**正在运行**的容器。 |
| `docker ps -a` | 列出**所有**容器（包括已停止的）。 |
| `docker logs <container_id>` | 查看容器的日志输出。 |
| `docker logs -f <container_id>` | **跟随模式**查看日志（类似 `tail -f`）。 |
| `docker logs --tail N <container_id>` | 查看最后 N 行日志。 |
| `docker top <container_id>` | 查看容器内运行的进程。 |
| `docker stats` | **动态显示**所有容器的资源使用统计（CPU，内存，网络IO等）。 |
| `docker stats <container_id>` | 显示指定容器的资源使用统计。 |
| `docker inspect <container_id>` | 获取容器（或镜像）的底层详细信息（JSON格式）。包括配置、网络、卷等。 |
| `docker port <container_id>` | 查看容器的端口映射情况。 |
| `docker diff <container_id>` | 检查容器文件系统相对于其镜像的更改（A：增加，C：修改，D：删除）。 |

---

### 第四部分：进入容器与执行命令

用于在运行的容器内部进行操作。

| 命令 | 解释与细节 | 区别 |
| :--- | :--- | :--- |
| `docker exec -it <container_id> <command>` | 在**正在运行**的容器中执行命令。最常用的是启动一个 shell：`docker exec -it my-container bash` | **主要方式**，用于与运行中的容器交互。 |
| `docker attach <container_id>` | 附着到一个正在运行的容器的**主进程**上。如果主进程是 shell，则可以交互；如果主进程是服务，则只能看到日志。**注意**：使用 `Ctrl+C` 会停止容器，使用 `Ctrl+P Ctrl+Q` 可以分离而不停止。 | 连接到主进程，不推荐新手使用。 |

---

### 第五部分：网络管理

Docker 提供了强大的网络功能来连接容器。

| 命令 | 解释与细节 |
| :--- | :--- |
| `docker network ls` | 列出所有 Docker 网络。 |
| `docker network create <network_name>` | 创建一个新的用户自定义网络（推荐用于多容器应用）。 |
| `docker network inspect <network_name>` | 查看网络的详细信息。 |
| `docker network connect <network> <container>` | 将容器连接到指定网络。 |
| `docker network disconnect <network> <container>` | 将容器从指定网络断开。 |
| `docker network prune` | 删除所有未使用的网络。 |

---

### 第六部分：数据卷管理

数据卷是持久化容器数据的首选机制。

| 命令 | 解释与细节 |
| :--- | :--- |
| `docker volume ls` | 列出所有数据卷。 |
| `docker volume create <volume_name>` | 创建一个命名的数据卷。 |
| `docker volume inspect <volume_name>` | 查看数据卷的详细信息（如挂载点）。 |
| `docker volume rm <volume_name>` | 删除一个数据卷。 |
| `docker volume prune` | **（小心！）** 删除所有未被容器使用的数据卷。 |

---

### 第七部分：Docker Compose

用于定义和运行多容器 Docker 应用程序的工具，通过 `docker-compose.yml` 文件配置。

| 命令 | 解释与细节 |
| :--- | :--- |
| `docker compose up` | 创建并启动所有服务。 |
| `docker compose up -d` | 在后台启动所有服务。 |
| `docker compose down` | 停止并删除所有容器、网络。**（加 `-v` 可以同时删除 compose 中声明的卷）** |
| `docker compose ps` | 列出 compose 项目中的所有容器。 |
| `docker compose logs` | 查看所有服务的日志。 |
| `docker compose logs -f <service>` | 跟随模式查看指定服务的日志。 |
| `docker compose exec <service> <command>` | 在指定服务的容器中执行命令。例如：`docker compose exec db mysql -u root -p` |
| `docker compose build` | 构建或重新构建 compose 文件中定义的服务镜像。 |
| `docker compose pull` | 拉取 compose 文件中定义的服务镜像。 |
| `docker compose config` | 验证并查看编译后的 compose 文件内容。 |

---

### 第八部分：系统与清理

用于管理 Docker 守护进程和清理磁盘空间。

| 命令 | 解释与细节 |
| :--- | :--- |
| `docker system df` | 查看 Docker 的磁盘使用情况（镜像、容器、卷、缓存）。 |
| `docker system prune` | **（小心！）** 一键清理所有未被使用的资源（停止的容器、无用的网络、构建缓存等）。 |
| `docker system prune -a` | **（非常小心！）** 更彻底的清理，包括所有未被使用的镜像。 |
| `docker system info` | 显示整个 Docker 系统的信息。 |
| `docker version` | 显示 Docker 客户端和服务器端的版本信息。 |