import json

hw_info= open("./json.txt", "r").read()  # 使
hw_info = json.loads(hw_info) # 使用json解析arm

sn = hw_info["serial"] # 解析json中的SN



def GET_SPF_NET_CARD_INFO(net_card_info):
    
    rj45_net_card_name = []   # 创建RJ45对
    rj45_net_card_model = []

    for i in net_card_info['children'][0]['children']:
        if len(i['children'][0]['logicalname']) == 2:   # 说明现在是插入网线了
            rj45_net_card_name.append(i['children'][0]['logicalname'][0])
            rj45_net_card_model.append(i['children'][0]['product'])
        else:
            rj45_net_card_name.append(i['children'][0]['logicalname'])
            rj45_net_card_model.append(i['children'][0]['product'])

    result = []
    for i in range(len(rj45_net_card_name)):
        js = {
            "name": rj45_net_card_name[i],
            "model": rj45_net_card_model[i]
        }
        result.append(js)
    

    print(result)



def GET_RJ45_CARD_INFO(net_card_info):
    print()

for i in hw_info['children'][0]['children']:
    # print(json.dumps(i))
    if "Ethernet interface" in json.dumps(i): # 获取电口的数据
       
        # print(json.dumps(i['children']))

        if  len(i['children']) == 1: # 获取光口的数据
            GET_SPF_NET_CARD_INFO(i)
        # GET_RJ45_CARD_INFO(i)