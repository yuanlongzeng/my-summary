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
