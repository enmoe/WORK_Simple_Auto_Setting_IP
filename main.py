import csv # 导入CSV模块
import os # 导入os模块

csv_file_name="../info.csv" # 配置要打开的csv文件的位置

net_card_cfg_path = "/etc/sysconfig/network/"  # 生成bond配置文件的目录,用于正式环境用
# net_card_cfg_path = "../test_file/"    # 生成bond配置文件的目录,用于测试输出文件的结果

# 设置BOND的模式 BONDING_MODULE_OPTS
bond_0_mode = "mode=802.3ad miimon=100"
bond_1_mode = "mode=active-backup miimon=100"
bond_2_mode = "" # 此项目无bond2

bond_0_eth_list = ["eth5", "eth7"]
bond_1_eth_list = ["eth0", "eth1"]
bond_2_eth_list = "" # 此项目无bond2

def GEN_BOND_CONF(bond_name, bond_mode, bond_eth_list, 
                    ipv4_addr, ipv4_gateway,
                    ipv6_addr, ipv6_gateway
    ): # 使用配置文件生成BOND的IP地址

    bond_if_file = net_card_cfg_path + "ifcfg-" + bond_name   # 配置生成BOND网卡的配置文件
    print(bond_if_file)
    bond_cfg = \
        "BONDING_MASTER='yes'" + '\n' + \
        "BONDING_MODULE_OPTS='" + bond_mode + "'" + '\n' + \
        "BONDING_SLAVE0='" + bond_eth_list[0] + "'" + '\n' + \
        "BONDING_SLAVE1='" + bond_eth_list[1] + "'" + '\n' + \
        "BOOTPROTO='static'" + '\n' + \
        "BROADCAST=''" + '\n' + \
        "ETHTOOL_OPTIONS=''" + '\n' + \
        "MTU=''" + '\n' + \
        "NAME=''" + '\n' + \
        "NETWORK=''" + '\n' + \
        "REMOTE_IPADDR=''" + '\n' + \
        "STARTMODE='auto'" + '\n' + \
        "IPADDR_0='" + ipv4_addr + "'" + '\n' + \
        "LABEL_0='0'" + '\n' + \
        "IPADDR_1='" + ipv6_addr + "'" + '\n' + \
        "LABEL_1='0'" + '\n'
    
    
    file = open(bond_if_file, 'w+') # 打开BOND的配置文件
    file.write(bond_cfg) # 写入BOND配置文件

    bond_if_route_file = net_card_cfg_path + "ifroute-" + bond_name   # 配置BOND的路由的文件
    file = open(bond_if_route_file, 'w+') # 打开bond的路由配置文件

    if bond_name == "bond0":    # 如果bond0的话指添加默认路由
        bond_route = \
            "default " + ipv4_gateway + " - bond0 " + '\n' + \
            "default " + ipv6_gateway + " - bond0 "
    else:   # 如果是其他的网口就指定一条普通的路由
        bond_route = \
            ipv4_addr + " " + ipv4_gateway + " - " + bond_name + '\n' + \
            ipv6_addr + " " + ipv6_gateway + " - " + bond_name + '\n' 
   
    file.write(bond_route)

def IF_BOND(
            bond_0_ipv4_addr, bond_0_ipv4_gateway,
            bond_0_ipv6_addr, bond_0_ipv6_gateway,
            bond_1_ipv4_addr, bond_1_ipv4_gateway,
            bond_1_ipv6_addr, bond_1_ipv6_gateway,
            bond_2_ipv4_addr, bond_2_ipv4_gateway,
            bond_2_ipv6_addr, bond_2_ipv6_gateway
            ): # 判断BOND是否存在并配置IP地址

    if bond_0_ipv4_addr!="NULL": # 判断是存在bond,如果存在开始配置bond
        GEN_BOND_CONF("bond0", bond_0_mode, bond_0_eth_list,
                        bond_0_ipv4_addr, bond_0_ipv4_gateway, 
                        bond_0_ipv6_addr, bond_0_ipv6_gateway
                        )

    if bond_1_ipv4_addr!="NULL": # 判断是存在bond,如果存在开始配置bond
        GEN_BOND_CONF("bond1", bond_1_mode, bond_1_eth_list,
                        bond_1_ipv4_addr, bond_1_ipv4_gateway, 
                        bond_1_ipv6_addr, bond_1_ipv6_gateway
                        )

    if bond_2_ipv4_addr!="NULL": # 判断是存在bond,如果存在开始配置bond
        GEN_BOND_CONF("bond2", bond_2_mode, bond_2_eth_list,
                        bond_2_ipv4_addr, bond_2_ipv4_gateway, 
                        bond_2_ipv6_addr, bond_2_ipv6_gateway
                        )
  
def SET_host_name(host_name): # 配置主机名
    comm = "hostnamectl" + " " + "set-hostname" + " " + \
        host_name  # 使用hostnamectl 配置主机名
    print(comm)
    # os.system(comm)
    

def GET_SERVER_INFO(): # 获取服务器硬件SN、并解析bond信息 IP信息

    RET = os.popen("lshw -json").read() # 获取服务器硬件信息
    SN = RET["serial"] # 解析json中的SN
    # SN = open("../testsn.txt", "r").read() # 用于测试脚本是否可以运行,配置测试的SN，测试是否呢个能生成bond、网卡的配置文件

    file = csv.reader(open(csv_file_name,'r')) # 使用只读打开csv文件
    for i in file:
        csv_file = i[1] # 解析CSV中的SN
        if csv_file == SN: # 判断服务器的SN与现场的是否一致，如果一致的话就开始解析CSV中的信息
            host_name=i[2]
            bond_0_ipv4_addr=i[3]
            bond_0_ipv4_gateway=i[4]
            bond_0_ipv6_addr=i[5]
            bond_0_ipv6_gateway=i[6]
            bond_1_ipv4_addr=i[7]
            bond_1_ipv4_gateway=i[8]
            bond_1_ipv6_addr=i[9]
            bond_1_ipv6_gateway=i[10]
            bond_2_ipv4_addr=i[11]
            bond_2_ipv4_gateway=i[12]
            bond_2_ipv6_addr=i[13]
            bond_2_ipv6_gateway=i[14]

            SET_host_name(host_name) # 如果一致开始配置主机名

            IF_BOND(
                    bond_0_ipv4_addr, bond_0_ipv4_gateway,
                    bond_0_ipv6_addr, bond_0_ipv6_gateway,
                    bond_1_ipv4_addr, bond_1_ipv4_gateway,
                    bond_1_ipv6_addr, bond_1_ipv6_gateway,
                    bond_2_ipv4_addr, bond_2_ipv4_gateway,
                    bond_2_ipv6_addr, bond_2_ipv6_gateway
                    )   # 传入所有ip的信息，判断是否存在bond
            break   #如果查询到了就跳出循环

def GEN_net_card_CONF(net_card_name, net_card_model):   # 
    net_card_file = net_card_cfg_path + "ifcfg-" + net_card_name
    file=open(net_card_file, "w+")
    net_card = \
        "BOOTPROTO='none'" + '\n' + \
        "BROADCAST=''" + '\n' + \
        "ETHTOOL_OPTIONS=''" + '\n' + \
        "IPADDR=''" + '\n' + \
        "MTU=''" + '\n' + \
        "NAME='" + net_card_model + "'" + '\n' + \
        "NETMASK=''" + '\n' + \
        "NETWORK=''" + '\n' + \
        "REMOTE_IPADDR=''" + '\n' + \
        "STARTMODE='hotplug'" + '\n' 

    file.write(net_card)    # 写入网卡配置文件

def ADD_NET_CADR_CONF():    # 添加网卡配置文件
    GEN_net_card_CONF(bond_1_eth_list[0], "HNS GE/10GE/25GE RDMA Network Controller")
    GEN_net_card_CONF(bond_1_eth_list[1], "HNS GE/10GE/25GE Network Controller")
    GEN_net_card_CONF(bond_0_eth_list[0], "Hi1822 Family (2*25GE)")
    GEN_net_card_CONF(bond_0_eth_list[1], "Hi1822 Family (2*25GE)")

def DEL_DEFAULT_NET_CARD_CONF():    # 删除默认的网卡、路由配置文件
    os.system('rm -rf /etc/sysconfig/network/ifcfg-e*')
    os.system('rm -rf /etc/sysconfig/network/ifroute-e*')
    os.system('rm -rf /etc/sysconfig/network/route*')

def RET_NET_CARD():
    os.system('systemctl restart network')
    
DEL_DEFAULT_NET_CARD_CONF() 
GET_SERVER_INFO()
ADD_NET_CADR_CONF()
RET_NET_CARD()