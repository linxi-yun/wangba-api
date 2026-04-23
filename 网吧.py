# 把你的逻辑装进这个“黑盒子”
# def add(nianling, daizheng, shengyujiqi, dangqianjiner, hongzourenshu):
#     while shengyujiqi > 0:
#
#         print("\n—— 下一位顾客 ——")
#         nianling = int(input("年龄："))
#         daizheng = input("带证（y/n):")
#         # 在这里写你的 if-elif-else 逻辑
#         if nianling >= 18 and daizheng == "y":
#             shengyujiqi -= 1
#             dangqianjiner += 10
#             if shengyujiqi == 1:
#                 print("叮铃铃 老板！还剩1台机器啦！")
#             print(f"请进！入账10元。")
#
#             print(f">>>剩余机器{shengyujiqi}台 | 今日已赚{dangqianjiner}")
#
#         elif nianling >= 18 and daizheng =="n":
#             print("成年人但没带证，回家拿")
#         else:
#             print("未成年不准进，轰走！")
#             hongzourenshu += 1
#         # 最后返回：新的剩余机器、新的金额、新的轰走计数、提示消息
#     print(f"\n 机器满了！今日总营收额{dangqianjiner}元")
#     print(f"今日一共轰走了{hongzourenshu}人")
#     return shengyujiqi, dangqianjiner, hongzourenshu
#             #新的剩余机器, 新的金额, 新的轰走计数, 消息
#
# import
#
# # 测试函数
# #机, 钱, 轰, 消息
# print("===网吧开业啦，10元一小时===")
#
# result = (add(20, 'y', 3, 0, 0))
# # print(result)       # 打印整个元组
# # print(result[0])    # 打印第一个元素
# # print(result[1])    # 打印第二个元素
# # 应该输出 “请进！入账10元。” 等等






def chuli_guke(nianling, daizheng, shengyujiqi, dangqianjiner, hongzourenshu):
    # 先把传进来的状态存好
    xin_jiqi = shengyujiqi
    xin_jiner = dangqianjiner
    xin_hongzou = hongzourenshu
    xiaoxi = ""

    if nianling >= 18 and daizheng == "y":
        # 最后一台通知（在减之前判断）
        if xin_jiqi == 1:
            xiaoxi += "🔔 叮铃铃 老板！还剩1台机器啦！\n"

        xin_jiqi -= 1
        xin_jiner += 10
        xiaoxi += f"请进！入账10元。\n>>>剩余机器{xin_jiqi}台 | 今日已赚{xin_jiner}元"

    elif nianling >= 18 and daizheng == "n":
        xiaoxi = "成年人但没带证，回家拿"

    else:
        xiaoxi = "未成年不准进，轰走！"
        xin_hongzou += 1

    return xin_jiqi, xin_jiner, xin_hongzou, xiaoxi


# ===== 营业主流程（while在外面） =====
jiqi = 3
jiner = 0
hongzou = 0

print("=== 网吧开业啦，10元一小时 ===")

while jiqi > 0:
    print("\n—— 下一位顾客 ——")
    age = int(input("年龄："))
    zheng = input("带证(y/n)：")

    # 调用函数处理这一位
    jiqi, jiner, hongzou, msg = chuli_guke(age, zheng, jiqi, jiner, hongzou)
    print(msg)

# 机器满了退出循环
print(f"\n🎉 机器满了！今日总营收额{jiner}元")
print(f"📊 今日一共轰走了{hongzou}个未成年人")