info = "Adress : "
def func_father(country):
    def func_son(area):
        city = "Shanghai "  # 此处的city变量，覆盖了父函数的city变量
        print(info + country + city + area)

    city = " Beijing "
    # 调用内部函数
    func_son("ChaoYang ");
func_father("China ")