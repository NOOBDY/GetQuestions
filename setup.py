import json

_id = input("學號: ")
passwd = input("密碼: ")

with open("login.json", "w+") as file:
    login_data = {}

    login_data["name"] = _id
    login_data["passwd"] = passwd
    login_data["rdoCourse"] = "5"

    file.writelines(json.dumps(login_data, indent=4))

with open("config.txt", "w+") as file:
    address = "36" if int(_id[-3:]) % 2 == 1 else "39"

    file.writelines(address)
