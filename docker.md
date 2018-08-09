<!-- TOC -->

- [Docker：](#docker)
    - [进程隔离原理:Linux命名空间](#进程隔离原理linux命名空间)
    - [网络：通过 iptables 进行数据包转发](#网络通过-iptables-进行数据包转发)
    - [文件系统隔离：目录挂载](#文件系统隔离目录挂载)
        - [chroot](#chroot)
    - [概念](#概念)
        - [镜像—类   容器—类的实例对象](#镜像类---容器类的实例对象)
        - [镜像：](#镜像)
        - [容器：独立运行的一个或一组应用](#容器独立运行的一个或一组应用)
        - [UnionFS](#unionfs)
        - [关系](#关系)
    - [命令](#命令)
    - [Run的运行机理](#run的运行机理)
    - [Dockerfile: 定制镜像—独立容器](#dockerfile-定制镜像独立容器)
        - [指令](#指令)
    - [Dokcer-compose:一组容器完成完整项目](#dokcer-compose一组容器完成完整项目)
    - [Docker Swarm](#docker-swarm)
    - [CI/CD：Drone](#cicddrone)
    - [使用实例](#使用实例)
        - [安装rabbitmq](#安装rabbitmq)

<!-- /TOC -->

# Docker：

## Docker从入门到实践
非常好的学习资料，简洁明了：[Docker从入门到实践](https://github.com/yeasy/docker_practice "docker")
## 进程隔离原理:Linux命名空间
使用虚拟化技术解决开发环境和生产环境 环境一致的问题  
运行在同一台机器上的不同服务能做到完全隔离，就像运行在多台不同的机器上一样—模拟集群环境  
docker通过 Linux 的 Namespaces 对不同的容器实现了进程和网络隔离  
可以通过docker exec -it name /bin/bash 进入容器的bash环境  
ps –ef  这样得到的只有容器的相关进程  
## 网络：通过 iptables 进行数据包转发 
![xxx.jpg](https://github.com/yuanlongzeng/my-summary/blob/master/img/docker网络.jpg )

当 Docker 服务器在主机上启动之后会创建新的虚拟网桥 docker0（brctl show），随后在该主机上启动的全部服务在默认情况下都与该网桥相连。
每一个容器在创建时都会创建一对虚拟网卡，两个虚拟网卡组成了数据的通道，其中一个会放在创建的容器中，会加入到名为 docker0 网桥中。

docker0 会为每一个容器分配一个新的 IP 地址并将 docker0 的 IP 地址设置为默认的网关。

网桥 docker0 通过 iptables 中的配置与宿主机器上的网卡相连，所有符合条件的请求都会通过 iptables 转发到 docker0 并由网桥分发给对应的机器（容器）。

当有 Docker 的容器需要将服务暴露给宿主机器，就会为容器分配一个 IP 地址，同时向 iptables 中追加一条新的规则。
iptables -t nat –L 查看转发规则NAT配置 

## 文件系统隔离：目录挂载
通过libcontainer提供的 pivor_root 或者 chroot 函数改变进程能够访问个文件目录的根节点，  
把容器需要的目录挂载到容器中，同时也禁止当前的容器进程访问宿主机器上的其他目录，  
保证了不同文件系统的隔离
### chroot
系统读取到的目录和文件将不在是旧系统根下的而是新根下(即被指定的新的位置) 特定的目录结构和文件，  
从而实现隔离隔离宿主机器上的物理资源： Control Groups(CGroup)  
每一个 CGroup 都是一组被相同的标准和参数限制的进程, 为一组进程分配资源,限制子容器资源占用
## 概念
### 镜像—类   容器—类的实例对象
### 镜像：
镜像都是由一系列只读的层组成的，Dockerfile 中的每一个命令都会在已有的只读层上创建一个新的层
### 容器：独立运行的一个或一组应用
### UnionFS
在 Docker 中，所有镜像层和容器层的内容都存储在 /var/lib/docker/aufs/diff/ 目录中  
/var/lib/docker/aufs/layers/ 中存储着镜像层的元数据，每一个文件都保存着镜像层的元数据，  
/var/lib/docker/aufs/mnt/ 包含镜像或者容器层的挂载点  
每一个镜像层都是建立在另一个镜像层之上的，同时所有的镜像层都是只读的，
只有每个容器最顶层的容器层才可以被用户直接读写，所有的容器都建立在一些底层服务（Kernel）上，
他们是使用存储驱动（aufs/overlay2）对文件进行组装（将不同文件夹中的层联合到同一个文件夹中）
### 关系
当镜像被 docker run 命令创建时就会在镜像的最上层添加一个可写的层，也就是容器层，所有对于运行时容器的修改其实都是对这个容器读写层的修改。
容器和镜像的区别就在于，所有的镜像都是只读的，而每一个容器其实等于镜像加上一个可读写的层，也就是同一个镜像可以对应多个容器。

![xxx.jpg](https://github.com/yuanlongzeng/my-summary/blob/master/img/Docker镜像与容器关系图.jpg )

## 命令
 
![xxx.jpg](https://github.com/yuanlongzeng/my-summary/blob/master/img/Docker命令.jpg)

Pts:伪终端  
run 重要参数：  
-d: 后台运行容器，并返回容器ID；  
-i: 以交互模式运行容器，通常与 -t 同时使用；  
-p: 端口映射，格式为：主机(宿主)端口:容器端口  
-t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；  
--name="nginx-lb": 为容器指定一个名称；  
## Run的运行机理
当利用 docker run 来创建容器时，Docker 在后台运行的标准操作包括：  
检查本地是否存在指定的镜像，不存在就从公有仓库下载  
利用镜像创建并启动一个容器  
分配一个文件系统，并在只读的镜像层外面挂载一层可读写层  
从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去  
从地址池配置一个 ip 地址给容器、执行用户指定的应用程序、执行完毕后容器被终止  
## Dockerfile: 定制镜像—独立容器
镜像的定制实际上就是定制每一层所添加的配置、文件：  
把每一层修改、安装、构建、操作的命令都写入一个脚本,  
每一条指令构建一层，因此每一条指令的内容，就是描述该层应当如何构建：
### 指令
FROM 基础镜像名称 （from scratch <没有基础镜像，go>）  
RUN 命令行：shell命令/脚本+可选参数  每条命令都会创建一层镜像（commit），所以一般应该使用&&连接各条命令。防止镜像层数过多（有最大层数限制）每次run之后都是一个全新的镜像（启动一个容器、执行命令、然后提交存储层文件变更），和需提供run的执行环境不一样（WORKDIR可以影响后面的所有层） 
支持换行/和注释#  
一组命令的最后添加清理工作的命令，清理了所有下载、展开的文件，并且还清理了 apt 缓存文件apt-get purge -y --auto-remove $buildDeps （否则会一直在镜像中，导致臃肿）

构建：docker build [选项：-t镜像名称]  镜像上下文【目录、URL】（打包发送给服务端 .dockerignore）  从标准输入读取dockerfile时没有上下文  
执行时是客户端通过rest API与docker引擎交互，在服务端构建   
Copy 目标目录不用提前创建，不存在会自动创建  
CMD:容器启动时有默认的cmd  如docker run –it Ubuntu  默认就会进入/bin/bash  

## Dokcer-compose:一组容器完成完整项目
使用python编写，调用docker的rest API接口对容器进行管理  
服务 ( service )：一个应用的容器，实际上可以包括若干运行相同镜像的容器实例。  
项目 ( project )：由一组关联的应用容器组成的一个完整业务单元，在 docker-compose.yml 文件中定义。  
docker-compose run service_name ud_cmd . #运行服务自定义cmd，首次运行会创建容器  
docker-compose stop/rm  
删除镜像要先停止其容器，删除子镜像及其容器  docker stop container_id \docker prune  
Docker rmi id  删除镜像再重新构建才会重新根据dockerfile构建镜像  
docker-compose up #它将尝试自动完成包括构建镜像，（重新）创建服务，启动服务，并关联服务相关容器的一系列操作  

## Docker Swarm
提供 Docker 容器集群服务，是 Docker 官方对容器云生态进行支持的核心方案。 可以将多个 Docker 主机封装为单个大型的虚拟 Docker 主机，快速打造一套容器云平台。

Swarm mode 已经内嵌入 Docker 引擎，成为了 docker 子命令 docker swarm 。请注意与旧的 Docker Swarm 区分开来。  
Swarm mode 内置 kv 存储功能，提供了众多的新特性，比如：具有容错能力的去中心化设计、内置服务发现、负载均衡、路由网格、动态伸缩、滚动更新、安全传输等。使得 Docker原生的 Swarm 集群具备与 Mesos、Kubernetes 竞争的实力。

## CI/CD：Drone

## 使用实例
### 安装rabbitmq
docker安装命令   
	docker run -d -p 5672:5672 rabbitmq  
进入容器，查看服务器的情况  
	docker ps  #查看id  
	docker exec -it rabbitmq_id  
运行命令查看  
    rabbitmqctl status  
发现rabbitmq自带可视化管理界面    
	rabbitmq-plugins enable rabbitmq_management  
但是默认端口为15672，需为其重新分配端口一遍可在容器外查看，运行下列命令    
	docker stop rabbitmq_id  
	docker commit rabbitmq_id new_name  
	docker run -d -p 5672:5672 -p 15672:15672 new_name  
输入localhost:15672,输入默认账户密码guest就可以进入可视化管理界面
