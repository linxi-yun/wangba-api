#安装 Streamlit在终端输入pip install streamlit

#创建本文件后，在本文件所在文件夹输入运行命令streamlit run wangba_web.py启动模拟器

import streamlit as st
import sqlite3
import os

DB_PATH = "wangba.db"  # 与 API 版共用同一个库

# 从环境变量读取机器总数，默认3台
TOTAL_MACHINES = int(os.getenv("WANGBA_MACHINES", "3"))

#====================================================================
def init_db():
    """创建数据库表并初始化（如果表为空）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS wangba_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            剩余机器 INTEGER DEFAULT {TOTAL_MACHINES},
            今日营收 INTEGER DEFAULT 0,
            轰走未成年 INTEGER DEFAULT 0
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM wangba_state")
    if cursor.fetchone()[0] == 0:
        cursor.execute(f"INSERT INTO wangba_state (id, 剩余机器, 今日营收, 轰走未成年) VALUES (1, {TOTAL_MACHINES}, 0, 0)")
    conn.commit()
    conn.close()

def get_state():
    """读取当前状态"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 剩余机器, 今日营收, 轰走未成年 FROM wangba_state WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return {"剩余机器": row[0], "今日营收": row[1], "轰走未成年": row[2]}

def update_state(jiqi, jiner, hongzou):
    """更新状态到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE wangba_state SET 剩余机器 = ?, 今日营收 = ?, 轰走未成年 = ? WHERE id = 1",
                   (jiqi, jiner, hongzou))
    conn.commit()
    conn.close()


# ========== 你的核心逻辑函数（一字未改） ==========
def chuli_guke(nianling, daizheng, shengyujiqi, dangqianjiner, hongzourenshu):
    # ========== 后端校验：防止非法年龄 ==========
    if nianling < 1 or nianling > 120:
        return shengyujiqi, dangqianjiner, hongzourenshu, "年龄输入不合法！请输入 1-120 之间的年龄。"
    # ===========================================

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

# 从数据库加载状态
if "db_loaded" not in st.session_state:
    state = get_state()
    st.session_state.jiqi = state["剩余机器"]
    st.session_state.jiner = state["今日营收"]
    st.session_state.hongzou = state["轰走未成年"]
    st.session_state.lishi = []   # 历史记录仍然用内存（可以以后再持久化）
    st.session_state.db_loaded = True

# 侧边栏显示实时状态
with st.sidebar:
    st.header("📊 营业状态")
    st.metric("剩余机器", st.session_state.jiqi)
    st.metric("今日营收", f"{st.session_state.jiner} 元")
    st.metric("轰走未成年", st.session_state.hongzou)

    if st.session_state.jiqi == 0:
        st.success("🎉 机器已满，收工！")
        st.balloons()
init_db()   # 确保每次启动数据库都就绪


# 主界面：输入顾客信息
col1, col2 = st.columns(2)
with col1:
    age_input = st.text_input("请输入顾客年龄", value="20")
    # 尝试转成整数，如果输入的不是数字就报错
    try:
        age = int(age_input)
    except ValueError:
        age = -1  # 触发后端校验
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
        update_state(new_ji, new_money, new_hong)
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
    st.session_state.jiqi = TOTAL_MACHINES
    st.session_state.jiner = 0
    st.session_state.hongzou = 0
    st.session_state.lishi = []
    update_state(TOTAL_MACHINES, 0, 0)   # 同步到数据库
    st.rerun()