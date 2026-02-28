# ==========================================
# 1. 变量 (Variables)
# ==========================================
# 变量就像是贴了标签的盒子，用来存储数据。
# 在 Python 中，不需要声明变量类型，直接赋值即可。

print("--- 1. 变量演示 ---")

# 整数 (int)
age = 18
print(f"年龄 (int): {age}")

# 浮点数 (float) - 带小数点的数字
height = 1.75
print(f"身高 (float): {height}")

# 字符串 (str) - 用单引号或双引号括起来的文本
name = "Trae User"
print(f"名字 (str): {name}")

# 布尔值 (bool) - True (真) 或 False (假)
is_student = True
print(f"是学生吗 (bool): {is_student}")

# 列表 (list) - 可以存放多个数据的容器
skills = ["Python", "Java", "C++"]
print(f"技能列表 (list): {skills}")
print(f"第一个技能: {skills[0]}")  # 索引从 0 开始


# ==========================================
# 2. 函数 (Functions)
# ==========================================
# 函数是一段可以重复使用的代码块。
# 使用 def 关键字定义函数。

print("\n--- 2. 函数演示 ---")

def greet(person_name, greeting="你好"):
    """
    这是一个简单的问候函数。
    参数:
        person_name: 名字
        greeting: 问候语，默认为 "你好"
    返回:
        格式化后的问候字符串
    """
    message = f"{greeting}, {person_name}!"
    return message

# 调用函数
msg1 = greet(name)
print(msg1)

# 调用函数并指定不同的问候语
msg2 = greet("世界", greeting="Hello")
print(msg2)


# ==========================================
# 3. 类 (Classes)
# ==========================================
# 类是创建对象的蓝图（模板）。对象是类的实例。
# 类封装了数据（属性）和行为（方法）。

print("\n--- 3. 类演示 ---")

class Dog:
    # __init__ 是构造函数，在创建对象时自动调用
    def __init__(self, name, breed):
        self.name = name    # 属性：名字
        self.breed = breed  # 属性：品种

    # 方法：定义类的行为
    def bark(self):
        return f"{self.name} 正在汪汪叫！"

    def introduce(self):
        return f"我是一只{self.breed}，我的名字叫 {self.name}。"

# 创建对象（实例化）
my_dog = Dog("旺财", "金毛")
neighbor_dog = Dog("小白", "比熊")

# 使用对象的方法和属性
print(my_dog.introduce())
print(my_dog.bark())
print(f"邻居的狗是: {neighbor_dog.name}")


# ==========================================
# 4. PIP 与 第三方库演示
# ==========================================
# PIP 是 Python 的包管理工具，用于安装和管理第三方库。
# 通常在命令行使用: pip install <库名>
# 下面演示如何使用一个通过 pip 安装的库：requests
# (在此之前，我会通过终端运行 `pip install requests` 来安装它)

print("\n--- 4. PIP 库演示 (requests) ---")

try:
    import requests
    
    print("成功导入 requests 库！这意味着 pip 安装成功。")
    print("正在尝试访问 GitHub API...")
    
    # 使用 requests 库发送一个简单的网络请求
    response = requests.get("https://api.github.com/zen")
    
    if response.status_code == 200:
        print(f"GitHub 的禅语: {response.text}")
    else:
        print("请求失败")
        
except ImportError:
    print("错误：requests 库未安装。")
    print("请在终端运行: pip install requests")
