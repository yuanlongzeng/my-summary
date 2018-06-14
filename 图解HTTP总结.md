

RFC（Request for Comments，征求修正意见书）

## http报文格式：
### 请求：
GET/POST URL HTTP/1.1  
各种headers（Cache-Control、Refer防盗链）  
\r\n\r\n 
请求体  
[注]有时我们会在控制台看见浏览器会发生两个请求  
第二个是浏览器自动发送的 GET /favicon.ico HTTP/1.1 请求  如果有就作为地址栏的图标  
`<link rel="icon" type="image/x-icon"  href="xxx/favicon.ico">`

### 响应： 
HTTP/1.1 状态码 原因短语  
response headers  
\r\n\r\n 
请求体


### status code分类
#### 3XX 重定向 
响应结果表明浏览器需要***执行某些特殊的处理以正确处理请求***。
当 301、302、303 响应状态码返回时，几乎所有的浏览器都会把POST 改成 GET，并删除请求报文内的主体，***之后请求会自动再次发送***。
301、302 标准是禁止将 POST 方法改变成 GET 方法的，但实际使用时大家都会这么做。

#### 4XX 的响应结果表明客户端是发生错误的原因所在
如404是客户端访问地址出错

#### 5XX 的响应结果表明服务器本身发生错误

### 常见status code
200成功  
204 no content:处理成功但是没有内容返回，页面不刷新  
206部分请求成功   Content-Range 指定范围的实体内容  
301永久转移  请求的资源已被分配了新的 URI  
302暂时转移  
400 bad request  
401未认证--需要一个身份才能访问  
403 禁止服务，未授权--没有权限  
404 not found  
500 内部服务器错误  
501 未实现  
503服务不可用 

### 解决http的无状态性

Session是服务端的解决方案，实现了web的会话跟踪，而Cookie是客户端的解决方案，实现了跟踪过程的用户识别。
Session是真正解决HTTP无状态的方案，而Cookie只是实现了Session过程中的SessionID方式  
使用 Cookie 来管理Session（会话），浏览器会自动发送Cookie

Cookie:  
Set-Cookie:响应返回给浏览器的  
Cookie:浏览器发送给服务器进行身份验证的

## 一些header
## nginx缓存设置
压缩可以节省宽带但是会消耗CPU资源：浏览器发起请求是会说明自己接受的编码方式
大文件还可以使用分块传输chunked transfer coding

Server最后不暴露这个信息  能更轻易的被利用漏洞攻击
隐藏版本号：server_tokens off; //nginx.conf http中配置  
自定义名称需要自己编译源码

### 传输数据格式：Content-type
MIME:多用途因特网邮件拓展multipuepose internet mail extensions
多部分对象集合：multipart
multipart/form-data  在 Web 表单文件上传时使用。
multipart/byteranges
状态码 206（Partial Content，部分内容）响应报文包含了多个范
围的内容时使用。
multipart/form-data


### 请求部分资源：用到首部的Range字段
    #python代码实例
    r = requests.get(url_file, stream=True)  #流模式  
    f = open("file_path", "ab")  
    for chunk in r.iter_content(chunk_size=512):  
        if chunk:  
            f.write(chunk)


## 内容协商字段：
Accept 用户代理可处理的媒体类型  
Accept-Charset优先的字符集  
Accept-Encoding优先的内容编码  
Accept-Language优先的语言（自然语言）  
Content-Language HTTP 客户端程序的信息  


## 安全
反爬：隐藏表单域

服务器端安全：  
https:ssl/tsl一个加密/身份验证层（在 HTTP 与 TCP 之间）  
TLS（Transport Layer Security，安全层传输协议）
客户端需要对 HTTP 报文主体进行加密处理后再发送请求

至少要确保一次正确的连接才能保证安全;  
中间人攻击：请求或响应在传输途中，遭攻击者拦截并篡改内容  
校验文件完整性与未修改：md5或hash值（但你也不能确定你访问的网站就是你想要访问的《DNS缓存服务器被攻击》   

共享密钥加密：发送密文的一方使用对方的公开密钥进行加密处理，对方收到被加密的信息后，再使用自己的私有密钥进行解密

HTTPS 采用混合加密机制：在交换密钥环节使用公开密钥加密方式（确保共享密钥的安全），之后的建立通信交换报文阶段则使用共享密钥加密方式   
公开密钥使用CA确保安全：浏览器会在内部植入常用认证机关的公开密钥

银行客户端证书，以确认用户是否从特定的终端访问网银

[TCP/IP四层网络模型]:  
应用层（ftp\http)  
传输层TCP、UDP(user data protocol)  
网络层IP、ARP  
链路层  

ARP 协议（Address Resolution Protocol）。ARP 是一种用以解析地址的协议，根据通信方的 IP 地址就可以反查出对应的 MAC 地址

字节流服务（Byte Stream Service）是指，为了方便传输，将大块数据分割成以报文段（segment）为单位的数据包进行管理（发送在传输层，为每个数据包编号及打上对方的ip\mac及对应的端口号）

TCP三次握手：
发送端首先发送一个带 SYN 标志的数据包给对方。接收端收到后，回传一个带有 SYN/ACK 标志的数据包以示传达确认信息。最后，发送端再回传一个带 ACK 标志的数据包，代表“握手”结束

## 其他
#### URL、URI
URI:资源的唯一标识符---身份证
URL:URI的子集，也可以唯一标识一个资源，但是提供了找到该资源的路径--住址
URL也可以称为URI

通过虚拟主机可以在一台服务器上部署多个域名的网站
因为请求到达服务器事是IP地址，所以需要在Host中标明URL/主机


通信数据转发程序：
代理：一种有转发功能的应用程序，它扮演了位于服务器和客户端“中间人”的角色，接收由客户端发送的请求并转发给服务器，同时
也接收服务器返回的响应并转发给客户端   Via 首部信息

网关：转发其他服务器通信数据的服务器，接收从客户端发送来的请求时，它就像自己拥有资源的源服务器一样对请求进行处理
以由 HTTP 请求转化为其他协议通信,也就是网关再使用别的协议（非 HTTP 协议）与服务器进行通信，并将最后的结果返回给客户端
应用：连接数据库、和信用卡结算系统联动

隧道:在相隔甚远的客户端和服务器两者之间进行中转，并保持双方
通信连接的应用程序
建立起一条与其他服务器的通信线路，可进行加密，本身不会去解析 HTTP 请求。会把请求保持原样中转给之后的服务器



浏览器发出自己可处理的首部信息，然后服务器也会有相应的实体首部可以让浏览器进行信息的提取  如Content-Encoding:gzip 
Content-Type:text/html; charset=utf-8



持久连接(默认），只要任意一端没有明确提出断开连接，则保持 TCP 连接状态，这样就不用等待响应就可发送多个请求---并行化
Keep-Alive头部解决的核心问题：一定时间内，同一域名多次请求数据，只建立一次HTTP请求，其他请求可复用每一次建立的连接通道，以达到提高请求效率的问题

WebSocket，即 Web 浏览器与 Web 服务器之间全双工通信标准。
由于是建立在 HTTP 基础上的协议，因此连接的发起方仍是客户端，而一旦确立 WebSocket 通信连接，不论服务器还是客户端，任意一方
都可直接向对方发送报文。
使B/S模式具备了C/S模式的实时通信能力
本质上是TCP连接，不需要每次传输都带上重复的头部数据

首部：Upgrade: websocket

响应请求，返回状态码 101 Switching Protocols 的响应

成功握手确立 WebSocket 连接之后，通信时不再使用 HTTP 的数据帧，而采用 WebSocket 独立的数据帧。

CGI（Common Gateway Interface，通用网关接口）是指 Web 服务器在接收到客户端发送过来的请求后***转发给程序***的一组机制

安全性：
HTTP 就是一个通用的单纯协议机制。因此它具备较多优势，但是在安全性方面则呈劣势。  
就拿远程登录时会用到的 SSH 协议来说，SSH 具备协议级别的认证及会话管理等功能，HTTP 协议则没有




