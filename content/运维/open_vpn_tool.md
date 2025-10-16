Title: Centos7搭建OpenVpn全流程
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: 操作命令
keywords: Centos7搭建OpenVpn全流程
summary: Centos7搭建OpenVpn全流程
lang: zh
status: published
Slug: open_vpn_tool
url: open_vpn_tool


# Centos7搭建OpenVpn全流程


### 步骤 1：更新系统首先，确保系统软件包是最新的

`sudo yum update -y`

![](centos7部署openvpn.files/centos7部署openvpn43.png)  

### 步骤 2：安装EPEL仓库和OpenVPN

EPEL （Extra Packages for Enterprise Linux）提供了额外的软件包，包含OpenVPN

`sudo yum install -y epel-release`

`sudo yum install -y openvpn easy-rsa`

![](centos7部署openvpn.files/centos7部署openvpn198.png) 

 

### 步骤 3：配置Easy-RSA并生成CA证书

**1 复制 Easy-RSA模板到OpenVPN目录下：**

`cp -r /usr/share/easy-rsa/ /etc/openvpn/`

**2 配置 Easy-RSA：**

`cd /etc/openvpn/easy-rsa/3`

**3 编辑 vars文件，配置基本信息：**

`vim vars`

在vars文件中设置必要的环境变量，例如：

set_var EASYRSA_REQ_COUNTRY "CN" 

set_var EASYRSA_REQ_PROVINCE "Shanghai" 

set_var EASYRSA_REQ_CITY "" 

set_var EASYRSA_REQ_ORG "Shanghai" 

set_var EASYRSA_REQ_EMAIL "admin@example.com" set_var EASYRSA_REQ_OU "MyUnit"

**4 初始化并构建 CA：**

`./easyrsa init-pki`

`./easyrsa build-ca`

在提示时设置一个CA密码，用于签署证书。

### 步骤 4：生成服务器证书和密钥 

执行以下命令创建服务器证书和密钥：

`./easyrsa gen-req server nopass`

`./easyrsa sign-req server server`

选择yes并输入CA密码完成签署。

### 步骤 5：生成Diffie-Hellman密钥和TLS密钥

`./easyrsa gen-dh`

`openvpn --genkey --secret ta.key`

将生成的密钥和证书移动到OpenVPN目录中：

`cp pki/ca.crt pki/issued/server.crt pki/private/server.key pki/dh.pem ta.key /etc/openvpn/`

### 步骤 6：配置OpenVPN服务器

复制 OpenVPN的示例配置文件并编辑：

`cp /usr/share/doc/openvpn*/sample/sample-config-files/server.conf /etc/openvpn/ `

`vim /etc/openvpn/server.conf`

配置内容可以参考以下示例：
```
# 服务器模式，定义 IP 地址池
port 1194                   # OpenVPN 服务器的端口
proto udp                   # 使用 UDP 协议，可以改为 proto tcp
dev tun                     # TUN 设备模式（可用于路由）
server 10.8.0.0 255.255.255.0 # 分配给客户端的 IP 地址范围

# 证书和密钥
ca ca.crt                   # CA 证书
cert server.crt             # 服务器证书
key server.key              # 服务器私钥
dh dh.pem                   # Diffie-Hellman 参数文件

# 加密设置
tls-auth ta.key 0           # HMAC 防护密钥，用于防止 DOS 攻击（必须与客户端一致）
cipher AES-256-CBC          # 加密算法
auth SHA256                 # 哈希算法

# 客户端配置推送
push "redirect-gateway def1 bypass-dhcp"  # 将客户端所有流量路由到 VPN
push "dhcp-option DNS 8.8.8.8"            # 设置客户端的 DNS（Google DNS）
push "dhcp-option DNS 8.8.4.4"            # 备用 DNS

# 允许客户端之间通信
client-to-client

# 保持客户端连接
keepalive 10 120

# 启用压缩（可选）
# compress lz4-v2           # 使用 LZ4 压缩，OpenVPN 2.4 及以上支持

# 日志和权限
user nobody                 # 降低权限，运行为普通用户
group nobody
persist-key
persist-tun
status /var/log/openvpn-status.log
```

### 步骤 7：启用并启动OpenVPN服务

`sudo systemctl enable openvpn@server`

`sudo systemctl start openvpn@server`

`sudo systemctl status openvpn@server`

### 步骤8：配置服务器安全组

入方向：开放 1194端口，协议是UDP协议

出反向：开放所有端口，协议UDP和TCP

### 步骤9：开通客户端证书

**1、切换到 Easy-RSA目录：**

`cd /etc/openvpn/easy-rsa/3`

**2、生成客户端密钥和证书**

`./easyrsa gen-req client1 nopass`

`./easyrsa sign-req client client1`

**3、将 `client1.crt`和`client1.key`移动到客户端目录，用于后续配置客户端。**

### 步骤 10：配置客户端`.ovpn`文件

```
client
dev tun
proto udp
remote 47.113.197.149 1194
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
tls-auth ta.key 1
cipher AES-256-CBC
auth SHA256
auth-nocache
verb 3


<ca> 
# 将ca.crt内容复制到此处 
</ca>
<cert> 
# 将client1.crt内容复制到此处 
</cert> 
<key> 
# 将client1.key内容复制到此处 
</key> 
<tls-auth> 
# 将ta.key内容复制到此处 
</tls-auth>
```

**下载客户端**

[OpenVpn官方下载地址](https://openvpn-2-0-1-rc1.updatestar.com/download)

导入`.open`文件即可使用


### 注意事项：服务器环境配置

`1`、确保 OpenVPN 服务器启用了 IP 转发。这可以通过运行以下命令来检查：

sudo sysctl net.ipv4.ip_forward

`2`、确保返回的值为 1，如果是 0，启用它：

sudo sysctl -w net.ipv4.ip_forward=1

`3`、并确保在 /etc/sysctl.conf 文件中有以下行：

net.ipv4.ip_forward = 1

`4`、如果在 /etc/sysctl.conf 文件中添加了该行，使用以下命令使其生效：

sudo sysctl -p

`5`、确保在 OpenVPN 服务器上启用 NAT（网络地址转换），以允许客户端通过服务器访问互联网。首先，确保你的 NAT 规则已经正确设置。可以使用以下命令查看 NAT 规则：

sudo iptables -t nat -L -n -v

`6`、确保有一条类似以下的规则：

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)

 pkts bytes target     prot opt in     out     source               destination

 0     0   MASQUERADE  all  \--  *      eth0    10.8.0.0/24        0.0.0.0/0

`7`、如果没有，则添加该规则：

sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

`8`、确保将 eth0 替换为你的实际网络接口名称。



