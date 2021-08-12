import json

SERVER_HW_INFO = open("./json.txt", "r").read()
SERVER_HW_INFO = json.loads(SERVER_HW_INFO) # 使用json解析arm

SN = SERVER_HW_INFO["serial"] # 解析json中的SN

RJ45_NET_CARD_NAME = []
RJ45_NET_CARD_MODEL = []

def GET_SPF_NET_CARD_INFO(NET_CARD_INFO):

    for i in NET_CARD_INFO['children'][0]['children']:
        if len(i['children'][0]['logicalname']) == 2:   # 说明现在是插入网线了
            RJ45_NET_CARD_NAME.append(i['children'][0]['logicalname'][0])
            RJ45_NET_CARD_MODEL.append(i['children'][0]['product'])
        else:
            RJ45_NET_CARD_NAME.append(i['children'][0]['logicalname'])
            RJ45_NET_CARD_MODEL.append(i['children'][0]['product'])

    result = []
    for i in range(len(RJ45_NET_CARD_NAME)):
        js = {
            "name": RJ45_NET_CARD_NAME[i],
            "model": RJ45_NET_CARD_MODEL[i]
        }
        result.append(js)
    

    print(json.dumps(result))



def GET_RJ45_CARD_INFO(NET_CARD_INFO):
    print()

for i in SERVER_HW_INFO['children'][0]['children']:
    # print(json.dumps(i))
    if "Ethernet interface" in json.dumps(i): # 获取电口的数据
       
        # print(json.dumps(i['children']))

        if  len(i['children']) == 1: # 获取光口的数据
            GET_SPF_NET_CARD_INFO(i)
        # GET_RJ45_CARD_INFO(i)