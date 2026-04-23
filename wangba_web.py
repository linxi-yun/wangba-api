#安装 Streamlit在终端输入pip install streamlit

#创建本文件后，在本文件所在文件夹输入运行命令streamlit run wangba_web.py启动模拟器

import streamlit as st


# ========== 你的核心逻辑函数（一字未改） ==========
def chuli_guke(nianling, daizheng, shengyujiqi, dangqianjiner, hongzourenshu):
    xin_jiqi = shengyujiqi
    xin_jiner = dangqianjiner
    xin_hongzou = hongzourenshu
    xiaoxi = ""

    if nianling >= 18 and daizheng == "y":
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


# ========== Streamlit 网页界面 ==========
st.set_page_config(page_title="网吧老板模拟器", page_icon="🖥️")
st.title("🖥️ 网吧老板模拟器")
st.markdown("---")

# 初始化状态（Streamlit 会自动记住）
if "jiqi" not in st.session_state:
    st.session_state.jiqi = 3
    st.session_state.jiner = 0
    st.session_state.hongzou = 0
    st.session_state.lishi = []  # 存放历史消息

# 侧边栏显示实时状态
with st.sidebar:
    st.header("📊 营业状态")
    st.metric("剩余机器", st.session_state.jiqi)
    st.metric("今日营收", f"{st.session_state.jiner} 元")
    st.metric("轰走未成年", st.session_state.hongzou)

    if st.session_state.jiqi == 0:
        st.success("🎉 机器已满，收工！")
        st.balloons()

# 主界面：输入顾客信息
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("顾客年龄", min_value=1, max_value=100, value=20)
with col2:
    zheng = st.radio("带身份证了吗？", ["y", "n"], horizontal=True)

# 处理按钮
if st.button("🚪 接待这位顾客", disabled=(st.session_state.jiqi == 0)):
    if st.session_state.jiqi > 0:
        # 调用你的函数
        new_ji, new_money, new_hong, msg = chuli_guke(
            age, zheng,
            st.session_state.jiqi,
            st.session_state.jiner,
            st.session_state.hongzou
        )
        # 更新状态
        st.session_state.jiqi = new_ji
        st.session_state.jiner = new_money
        st.session_state.hongzou = new_hong
        st.session_state.lishi.append(f"👤 {age}岁 | 带证:{zheng} → {msg}")
        st.rerun()  # 刷新界面

# 显示营业记录
st.markdown("---")
st.subheader("📋 今日接待记录")
if st.session_state.lishi:
    for record in reversed(st.session_state.lishi):
        st.text(record)
else:
    st.text("暂无顾客，点击按钮开始营业")

# 重置按钮
if st.button("🔄 新的一天（重置）"):
    st.session_state.jiqi = 3
    st.session_state.jiner = 0
    st.session_state.hongzou = 0
    st.session_state.lishi = []
    st.rerun()