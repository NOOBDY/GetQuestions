import json
with open("login.json", "w+") as file:
    login_data = {}

    login_data["name"] = input("學號: ")
    login_data["passwd"] = input("密碼: ")
    login_data["rdoCourse"] = "5"

    file.writelines(json.dumps(login_data, indent=4))

with open("config.txt", "w+") as file:
    address = "36" if input("單號或雙號: (1/2)") == "1" else "39"

    file.writelines(address)
