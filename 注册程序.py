import json
import os
import re
from dataclasses import dataclass, asdict

# 定义常量
课程 = ["Python", "Linux", "网络安全", "前端", "数据分析"]
文件 = "已注册学生.json"
错误信息 = {
    "年龄": "输入的年龄无效",
    "手机号": "输入手机长度不对或手机号已存在",
    "身份证": "输入身份证号有误或已存在"
}


@dataclass
class 学生:
    姓名: str
    年龄: int
    手机号: str
    身份证号: str
    所选课程: str


def 读取数据():
    if os.path.exists(文件):
        with open(文件, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def 写入数据(数据):
    with open(文件, "w", encoding="utf-8") as f:
        json.dump(数据, f, ensure_ascii=False, indent=4)


def 验证手机号(手机号):
    return bool(re.match(r'^1[3-9]\d{9}$', 手机号))


def 验证年龄(年龄):
    try:
        年龄 = int(年龄)
        return 0 < 年龄 < 150
    except ValueError:
        return False


def 验证身份证(身份证号):
    return bool(re.match(r'^\d{6}(19|20)\d{2}(0[1-9]|1[0-2])([0-2][0-9]|3[0-1])\d{3}[\dX]$', 身份证号))


def 检查唯一性(手机号, 身份证号, 数据):
    return all(学生["手机号"] != 手机号 and 学生["身份证号"] != 身份证号 for 学生 in 数据)


def 获取学员信息(data):
    print("请输入学生信息".center(40, "#"))
    姓名 = input("请输入姓名：")
    年龄 = input("请输入年龄：")
    while not 验证年龄(年龄):
        print(错误信息["年龄"])
        年龄 = input("请输入年龄：")
    手机号 = input("请输入手机号：")

    while not (验证手机号(手机号) and 检查唯一性(手机号, "", data)):
        print(错误信息["手机号"])
        手机号 = input("请输入手机号：")

    身份证号 = input("请输入身份证号：")
    while not (验证身份证(身份证号) and 检查唯一性("", 身份证号, data)):
        print(错误信息["身份证"])
        身份证号 = input("请输入身份证号：")

    return 学生(姓名, int(年龄), 手机号, 身份证号, "")  # placeholder for 所选课程


def 选择课程():
    print("\n可选课程编号")
    for 编号, 课程名 in enumerate(课程, start=1):
        print(f'{编号}: {课程名}')
    while True:
        选择编号 = input("请输入课程编号：")
        if 选择编号.isdigit() and 1 <= int(选择编号) <= len(课程):
            return 课程[int(选择编号)-1]
        else:
            print("选择的编号有误")


def 注册信息():
    data = 读取数据()
    学员 = 获取学员信息(data)
    学员.所选课程 = 选择课程()

    data.append(asdict(学员))  # 直接转换为字典
    写入数据(data)
    print("注册成功！")


def 主程序():
    print("欢迎注册")
    while True:
        注册信息()
        继续 = input("是否继续注册(Y/N): ")
        if 继续.lower() != "y":
            print("感谢使用学籍注册系统，再见！")
            break


if __name__ == "__main__":
    主程序()
