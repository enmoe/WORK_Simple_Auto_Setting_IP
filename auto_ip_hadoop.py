import csv # 导入CSV模块

CSV_FILE_NAME="test.csv" # 配置要打开的csv文件的路径

def SET_BOND_IP_ADDR(BOND_NAME,
                    IPv4_ADDR, IPv4_GATEWAY,
                    IPv6_ADDR, IPv6_GATEWAY
    ): # 使用网卡模版配置BOND的IP地址
    IP_INFO = BOND_NAME + " " + IPv4_ADDR + " " + IPv4_GATEWAY + " " + \
        IPv6_ADDR + " " + IPv6_GATEWAY  
    print(IP_INFO)  # 现在还没生成网卡的配置文件，所以先输出看看,是否能解析到IP地址和网关

def IF_BOND(
            BOND_0_IPv4_ADDR, BOND_0_IPv4_GATEWAY,
            BOND_0_IPv6_ADDR, BOND_0_IPv6_GATEWAY,
            BOND_1_IPv4_ADDR, BOND_1_IPv4_GATEWAY,
            BOND_1_IPv6_ADDR, BOND_1_IPv6_GATEWAY,
            BOND_2_IPv4_ADDR, BOND_2_IPv4_GATEWAY,
            BOND_2_IPv6_ADDR, BOND_2_IPv6_GATEWAY
): # 判断BOND是否存在并配置IP地址

    if BOND_0_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        SET_BOND_IP_ADDR("bond0",
                        BOND_0_IPv4_ADDR, BOND_0_IPv4_GATEWAY, 
                        BOND_0_IPv6_ADDR, BOND_0_IPv6_GATEWAY
        )

    if BOND_1_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        SET_BOND_IP_ADDR("bond1",
                        BOND_1_IPv4_ADDR, BOND_1_IPv4_GATEWAY, 
                        BOND_1_IPv6_ADDR, BOND_1_IPv6_GATEWAY
        )

    if BOND_2_IPv4_ADDR!="NULL": # 判断是存在bond,如果存在开始配置bond
        SET_BOND_IP_ADDR("bond2",
                        BOND_2_IPv4_ADDR, BOND_2_IPv4_GATEWAY, 
                        BOND_2_IPv6_ADDR, BOND_2_IPv6_GATEWAY
        )
    

def SET_HOST_NAME(HOST_NAME): # 配置主机名
    comm = "hostnamectl" + " " + "set-hostname" + " " + HOST_NAME  # 使用hostnamectl 配置主机名
    print(comm)


def GET_SERVER_INFO(): # 获取服务器硬件SN、并解析bond信息 IP信息
    TEST_SN = "" # 用于测试脚本是否可以运行SN
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

GET_SERVER_INFO()