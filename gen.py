import json
from json import JSONEncoder


class SimpleAddress:
    def __init__(self, id, parent_id, name, grade):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.grade = grade
        pass

    pass


class Address:

    def __init__(self):
        self.name = ""
        self.code = ""
        self.children = []
        pass

    pass


pass


class AddressJsonEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__


DefaultProvince = ["北京市", "天津市", "上海市", "重庆市"]

if __name__ == '__main__':
    reader = open('address.txt', mode="r")
    lines = reader.readlines()
    addressList = []

    provinceIndex = -1
    cityIndex = -1

    for line in lines:
        if line.count("#") == 1:
            split_arr = line.split("#")
            code = split_arr[0]
            name = split_arr[1].replace("\n", "")

            # 判断是否为直辖市
            if DefaultProvince.count(name):
                province = Address()
                province.code = code
                province.name = name.replace("市", "")
                addressList.append(province)
                provinceIndex += 1
                cityIndex = -1

                city = Address()
                city.code = int(code) + 100
                city.name = name
                addressList[provinceIndex].children.append(city)
                cityIndex += 1
                pass
            else:
                province = Address()
                province.code = code
                province.name = name
                addressList.append(province)
                provinceIndex += 1
                cityIndex = -1
            pass
        elif line.count("=>") == 1:
            split_arr = line.split("=>")
            city = Address()
            city.code = split_arr[0]
            city.name = split_arr[1].replace("\n", "")
            addressList[provinceIndex].children.append(city)
            cityIndex += 1
        else:
            split_arr = line.split(",")
            level3 = Address()
            level3.code = split_arr[0]
            level3.name = split_arr[1].replace("\n", "")
            p = addressList[provinceIndex]
            addressList[provinceIndex].children[cityIndex].children.append(level3)

    pass

    new_address_list = []

    new_address_list.append(SimpleAddress(id=1, parent_id=0, name="中国", grade=1))

    for p in addressList:
        p_code = p.code
        new_address_list.append(SimpleAddress(id=int(p_code), parent_id=1, name=p.name, grade=2))
        if len(p.children) > 0:
            for c in p.children:
                c_code = c.code
                new_address_list.append(SimpleAddress(id=int(c_code), parent_id=int(p_code), name=c.name, grade=3))
                for d in c.children:
                    d_code = d.code
                    new_address_list.append(SimpleAddress(id=int(d_code), parent_id=int(c_code), name=d.name, grade=4))
                pass
            pass
        pass
    pass

    jsonString = json.dumps(new_address_list, indent=4, cls=AddressJsonEncoder, ensure_ascii=False)
    with open("address.json", "w") as text_file:
        text_file.write(jsonString)
        pass
    text_file.close()
    reader.close()
