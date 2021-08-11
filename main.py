import csv # 导入CSV模块
import os # 导入os模块

CSV_FILE_NAME="../info.csv" # 配置要打开的csv文件的路径
TEST_SN = "2102313CQDP0L6000210" # 用于测试脚本是否可以运行SN

# 设置BOND的模式 BONDING_MODULE_OPTS
BOND_0_MODE = "mode=802.3ad miimon=100"
BOND_1_MODE = "mode=active-backup miimon=100"
BOND_2_MODE = "" # 此子项目无bond2
def SET_BOND_IP_ADDR(BOND_NAME, BOND_MODE,
                    IPv4_ADDR, IPv4_GATEWAY,
                    IPv6_ADDR, IPv6_GATEWAY
    ): # 使用配置文件生成BOND的IP地址

    # IF_CFG_PATH = "/etc/sysconfig/network/"
    IF_CFG_PATH = "../test_file/"    # 生成bond配置文件的目录，不填写在当前生成
    BOND_IF_FILE = IF_CFG_PATH + "ifcfg-" + BOND_NAME   # 配置BOND网卡的配置文件的位置
    print(BOND_IF_FILE)
    BOND_CFG = \
        "BONDING_MASTER='yes'" + '\n' + \
        "BONDING_MODULE_OPTS='" + BOND_MODE + "'" + '\n' + \
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
    
    BOND_FILE = open(BOND_IF_FILE, 'w+') # 打开BOND的配置文件
    BOND_FILE.write(BOND_CFG)


def IF_BOND(
            BOND_0_IPv4_ADDR, BOND_0_IPv4_GATEWAY,
            BOND_0_IPv6_ADDR, BOND_0_IPv6_GATEWAY,
            BOND_1_IPv4_ADDR, BOND_1_IPv4_GATEWAY,
            BOND_1_IPv6_ADDR, BOND_1_IPv6_GATEWAY,
            BOND_2_IPv4_ADDR, BOND_2_IPv4_GATEWAY,
            BOND_2_IPv6_ADDR, BOND_2_IPv6_GATEWAY
            ): # 判断BOND是否存在并配置IP地址

    if BOND_0_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        SET_BOND_IP_ADDR("bond0", BOND_0_MODE,
                        BOND_0_IPv4_ADDR, BOND_0_IPv4_GATEWAY, 
                        BOND_0_IPv6_ADDR, BOND_0_IPv6_GATEWAY
                        )

    if BOND_1_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        SET_BOND_IP_ADDR("bond1", BOND_1_MODE,
                        BOND_1_IPv4_ADDR, BOND_1_IPv4_GATEWAY, 
                        BOND_1_IPv6_ADDR, BOND_1_IPv6_GATEWAY
                        )

    if BOND_2_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        SET_BOND_IP_ADDR("bond2", BOND_2_MODE,
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
        SN = i[1] # 解析CSV中的SN
        if SN == GET_SN: # 判断服务器的SN与CSV的中的SN
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

def ADD_NET_CARD_CONF():
    print


def DEL_DEFAULT_NET_CARD_CONF():    # 删除默认的网卡、路由配置文件
    os.system('rm -rf /etc/sysconfig/network/ifcfg-e*')
    os.system('rm -rf /etc/sysconfig/network/ifroute-e*')
    os.system('rm -rf /etc/sysconfig/network/route*')
    
# DEL_DEFAULT_NET_CARD_CONF() 
GET_SERVER_INFO()