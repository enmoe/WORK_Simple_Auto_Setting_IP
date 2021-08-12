import csv # 导入CSV模块
import os # 导入os模块

CSV_FILE_NAME="../info.csv" # 配置要打开的csv文件的位置
TEST_SN = open("../testsn.txt", "r").read() # 用于测试脚本是否可以运行,配置测试的SN，测试是否呢个能生成bond、网卡的配置文件

# IF_CFG_PATH = "/etc/sysconfig/network/"  生成bond配置文件的目录,用于正式环境用
IF_CFG_PATH = "../test_file/"    # 生成bond配置文件的目录,用于测试输出文件的结果

# 设置BOND的模式 BONDING_MODULE_OPTS
BOND_0_MODE = "mode=802.3ad miimon=100"
BOND_1_MODE = "mode=active-backup miimon=100"
BOND_2_MODE = "" # 此项目无bond2

BOND_0_ETH = ["eth5", "eth7"]
BOND_1_ETH = ["eth0", "eth1"]
BOND_2_ETH = "" # 此项目无bond2

def GEN_BOND_CONF(BOND_NAME, BOND_MODE, BOND_ETH, 
                    IPv4_ADDR, IPv4_GATEWAY,
                    IPv6_ADDR, IPv6_GATEWAY
    ): # 使用配置文件生成BOND的IP地址

    BOND_IF_FILE = IF_CFG_PATH + "ifcfg-" + BOND_NAME   # 配置生成BOND网卡的配置文件
    print(BOND_IF_FILE)
    BOND_CFG = \
        "BONDING_MASTER='yes'" + '\n' + \
        "BONDING_MODULE_OPTS='" + BOND_MODE + "'" + '\n' + \
        "BONDING_SLAVE0='" + BOND_ETH[0] + "'" + '\n' + \
        "BONDING_SLAVE1='" + BOND_ETH[1] + "'" + '\n' + \
        "BOOTPROTO='static'" + '\n' + \
        "BROADCAST=''" + '\n' + \
        "ETHTOOL_OPTIONS=''" + '\n' + \
        "MTU=''" + '\n' + \
        "NAME=''" + '\n' + \
        "NETWORK=''" + '\n' + \
        "REMOTE_IPADDR=''" + '\n' + \
        "STARTMODE='auto'" + '\n' + \
        "IPADDR_0='" + IPv4_ADDR + "'" + '\n' + \
        "LABEL_0='0'" + '\n' + \
        "IPADDR_1='" + IPv6_ADDR + "'" + '\n' + \
        "LABEL_1='0'" + '\n'
    
    
    FILE = open(BOND_IF_FILE, 'w+') # 打开BOND的配置文件
    FILE.write(BOND_CFG) # 写入BOND配置文件

    BOND_IF_ROUTE_FILE = IF_CFG_PATH + "ifroute-" + BOND_NAME   # 配置BOND的路由
    FILE = open(BOND_IF_ROUTE_FILE, 'w+') # 打开bond的路由配置文件

    if BOND_NAME == "bond0":    # 如果bond0的话指添加默认路由
        BOND_ROUTE = \
            "default " + IPv4_GATEWAY + " - bond0 " + '\n' + \
            "default " + IPv6_GATEWAY + " - bond0 "
    else:
        BOND_ROUTE = \
            IPv4_ADDR + " " + IPv4_GATEWAY + " - " + BOND_NAME + '\n' + \
            IPv6_ADDR + " " + IPv6_GATEWAY + " - " + BOND_NAME + '\n' 
   
    FILE.write(BOND_ROUTE)

def IF_BOND(
            BOND_0_IPv4_ADDR, BOND_0_IPv4_GATEWAY,
            BOND_0_IPv6_ADDR, BOND_0_IPv6_GATEWAY,
            BOND_1_IPv4_ADDR, BOND_1_IPv4_GATEWAY,
            BOND_1_IPv6_ADDR, BOND_1_IPv6_GATEWAY,
            BOND_2_IPv4_ADDR, BOND_2_IPv4_GATEWAY,
            BOND_2_IPv6_ADDR, BOND_2_IPv6_GATEWAY
            ): # 判断BOND是否存在并配置IP地址

    if BOND_0_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        GEN_BOND_CONF("bond0", BOND_0_MODE, BOND_0_ETH,
                        BOND_0_IPv4_ADDR, BOND_0_IPv4_GATEWAY, 
                        BOND_0_IPv6_ADDR, BOND_0_IPv6_GATEWAY
                        )

    if BOND_1_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        GEN_BOND_CONF("bond1", BOND_1_MODE, BOND_1_ETH,
                        BOND_1_IPv4_ADDR, BOND_1_IPv4_GATEWAY, 
                        BOND_1_IPv6_ADDR, BOND_1_IPv6_GATEWAY
                        )

    if BOND_2_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        GEN_BOND_CONF("bond2", BOND_2_MODE, BOND_2_ETH,
                        BOND_2_IPv4_ADDR, BOND_2_IPv4_GATEWAY, 
                        BOND_2_IPv6_ADDR, BOND_2_IPv6_GATEWAY
                        )
  
def SET_HOST_NAME(HOST_NAME): # 配置主机名
    comm = "hostnamectl" + " " + "set-hostname" + " " + \
        HOST_NAME  # 使用hostnamectl 配置主机名
    print(comm)
    # os.system(comm)

def GET_SERVER_INFO(): # 获取服务器硬件SN、并解析bond信息 IP信息
    GET_SN =  TEST_SN   # 配置获取SN的方式是测试SN
    FILE = csv.reader(open(CSV_FILE_NAME,'r')) # 使用只读打开csv文件
    for i in FILE:
        SN = i[1] # 解析CSV中的SN
        if SN == GET_SN: # 判断服务器的SN与现场的是否一致
            HOST_NAME=i[2]
            BOND_0_IPv4_ADDR=i[3]
            BOND_0_IPv4_GATEWAY=i[4]
            BOND_0_IPv6_ADDR=i[5]
            BOND_0_IPv6_GATEWAY=i[6]
            BOND_1_IPv4_ADDR=i[7]
            BOND_1_IPv4_GATEWAY=i[8]
            BOND_1_IPv6_ADDR=i[9]
            BOND_1_IPv6_GATEWAY=i[10]
            BOND_2_IPv4_ADDR=i[11]
            BOND_2_IPv4_GATEWAY=i[12]
            BOND_2_IPv6_ADDR=i[13]
            BOND_2_IPv6_GATEWAY=i[14]

            SET_HOST_NAME(HOST_NAME) # 如果一致开始配置主机名

            IF_BOND(
                    BOND_0_IPv4_ADDR, BOND_0_IPv4_GATEWAY,
                    BOND_0_IPv6_ADDR, BOND_0_IPv6_GATEWAY,
                    BOND_1_IPv4_ADDR, BOND_1_IPv4_GATEWAY,
                    BOND_1_IPv6_ADDR, BOND_1_IPv6_GATEWAY,
                    BOND_2_IPv4_ADDR, BOND_2_IPv4_GATEWAY,
                    BOND_2_IPv6_ADDR, BOND_2_IPv6_GATEWAY
                    )   # 传入所有ip的信息，判断是否存在bond
            break   #如果查询到了就跳出循环

def GEN_NET_CARD_CONF(NET_CARD_NAME, NET_CARD_MODEL):   # 
    NET_CARD_FILE = IF_CFG_PATH + "ifcfg-" + NET_CARD_NAME
    FILE=open(NET_CARD_FILE, "w+")
    NET_CARD = \
        "BOOTPROTO='none'" + '\n' + \
        "BROADCAST=''" + '\n' + \
        "ETHTOOL_OPTIONS=''" + '\n' + \
        "IPADDR=''" + '\n' + \
        "MTU=''" + '\n' + \
        "NAME='" + NET_CARD_MODEL + "'" + '\n' + \
        "NETMASK=''" + '\n' + \
        "NETWORK=''" + '\n' + \
        "REMOTE_IPADDR=''" + '\n' + \
        "STARTMODE='hotplug'" + '\n' 

    FILE.write(NET_CARD)    # 写入网卡配置文件

    # print(NET_CARD)


def ADD_NET_CADR_CONF():    # 添加网卡配置文件
    GEN_NET_CARD_CONF(BOND_1_ETH[0], "HNS GE/10GE/25GE RDMA Network Controller")
    GEN_NET_CARD_CONF(BOND_1_ETH[1], "HNS GE/10GE/25GE Network Controller")
    GEN_NET_CARD_CONF(BOND_0_ETH[0], "Hi1822 Family (2*25GE)")
    GEN_NET_CARD_CONF(BOND_0_ETH[1], "Hi1822 Family (2*25GE)")


def DEL_DEFAULT_NET_CARD_CONF():    # 删除默认的网卡、路由配置文件
    os.system('rm -rf /etc/sysconfig/network/ifcfg-e*')
    os.system('rm -rf /etc/sysconfig/network/ifroute-e*')
    os.system('rm -rf /etc/sysconfig/network/route*')
    
# DEL_DEFAULT_NET_CARD_CONF() 
GET_SERVER_INFO()
ADD_NET_CADR_CONF()
