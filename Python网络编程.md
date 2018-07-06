

### Http、TCP/UDP、socket
http使用TCP\UDP连接，TCP\UDP是一种协议，其具体实现是socket(操作系统负责底层通信
 
http请求：维护一个线程池，每个线程完成一次请求，当没有空闲线程时就会出现503 service unavailable  
IO多路复用：多个网络连接，复用同一个线程  

TCP/IP协议的操作系统实现：socket  类似于文件操作 listen accept send write
使用端口进行多路复用和分解  使用UDP协议的程序需要自己处理丢包、重组和包的乱序问题--不如使用消息队列
TCP则保证了数据流的顺序和可靠传输
![TCP分层.jpg](https://github.com/yuanlongzeng/my-summary/blob/master/img/TCP%E5%88%86%E5%B1%82.jpg)

其中socke API层之下的几层：  
传输控制协议（TCP）,该层通过发送（可能重发）、接收以及重排称为数据包（packet）的小
型网络信息，支持由字节流组成的双向网络会话。  
网际协议（IP），该层处理不同计算机间数据包的发送。  
最底层的"链路层",该层负责在直接相连的计算机之间发送物理信息，由网络硬件设备组成，
如以太网端口和无线网卡。  DSL调制解调器使用了频域多路复用  

IP地址：一般 .0子网名 .1连接网关 .255广播地址

#### TCP为什么建立连接是三次握手，而关闭连接却是四次挥手呢？

这是因为服务端在LISTEN状态下，收到建立连接请求的SYN报文后，把**ACK和SYN放在一个报文里发送给客户端**。而关闭连接时，
当收到对方的FIN报文时，仅仅表示**对方不再发送数据了但是还能接收数据**，己方也未必全部数据都发送给对方了，所以己方可以立即close，
也可以发送一些数据给对方后，再发送FIN报文给对方来表示同意现在关闭连接，因此，己方ACK和FIN一般都会分开发送。

![三次握手](https://github.com/yuanlongzeng/my-summary/blob/master/img/%E4%B8%89%E6%AC%A1%E6%8F%A1%E6%89%8B.jpg)
