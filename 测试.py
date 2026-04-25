import streamlit as st
import sqlite3
import os

# ---- 配置 ----
DB_PATH = "wangba.db"
TOTAL_MACHINES = int(os.getenv("WANGBA_MACHINES", "3"))

# ---- 数据库函数 ----
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS wangba_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            剩余机器 INTEGER DEFAULT {TOTAL_MACHINES},
            今日营收 INTEGER DEFAULT 0,
            轰走未成年 INTEGER DEFAULT 0
        )
    """)
    c.execute("SELECT COUNT(*) FROM wangba_state")
    if c.fetchone()[0] == 0:
        c.execute(f"INSERT INTO wangba_state (id, 剩余机器, 今日营收, 轰走未成年) VALUES (1, {TOTAL_MACHINES}, 0, 0)")
    conn.commit()
    conn.close()

def get_state():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 剩余机器, 今日营收, 轰走未成年 FROM wangba_state WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return {"剩余机器": row[0], "今日营收": row[1], "轰走未成年": row[2]}

def update_state(jiqi, jiner, hongzou):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE wangba_state SET 剩余机器 = ?, 今日营收 = ?, 轰走未成年 = ? WHERE id = 1",
              (jiqi, jiner, hongzou))
    conn.commit()
    conn.close()

# ---- 核心业务逻辑 ----
def chuli_guke(nianling, daizheng, shengyujiqi, dangqianjiner, hongzourenshu):
    # 后端校验
    if nianling < 1 or nianling > 120:
        return shengyujiqi, dangqianjiner, hongzourenshu, "年龄输入不合法！请输入1-120之间的年龄。"
    # ... 原有逻辑（你之前的功能，一个字都不要改）
    # 注意变量名要与原来的对应好
    # 最后返回 xin_jiqi, xin_jiner, xin_hongzou, xiaoxi

# ---- Streamlit 界面 ----
st.set_page_config(...)
st.title(...)

init_db()   # 启动时初始化数据库

# 加载状态
if "db_loaded" not in st.session_state:
    state = get_state()
    st.session_state.jiqi = state["剩余机器"]
    st.session_state.jiner = state["今日营收"]
    st.session_state.hongzou = state["轰走未成年"]
    st.session_state.lishi = []
    st.session_state.db_loaded = True

# 界面组件（保持不变）
# ...

# 接待顾客按钮回调
if st.button("接待这位顾客", disabled=(st.session_state.jiqi == 0)):
    new_ji, new_money, new_hong, msg = chuli_guke(
        age, zheng,
        st.session_state.jiqi,
        st.session_state.jiner,
        st.session_state.hongzou
    )
    st.session_state.jiqi = new_ji
    st.session_state.jiner = new_money
    st.session_state.hongzou = new_hong
    update_state(new_ji, new_money, new_hong)   # 持久化
    st.session_state.lishi.append(f"...")
    st.rerun()

# 重置按钮
if st.button("新的一天"):
    st.session_state.jiqi = TOTAL_MACHINES
    st.session_state.jiner = 0
    st.session_state.hongzou = 0
    st.session_state.lishi = []
    update_state(TOTAL_MACHINES, 0, 0)
    st.rerun()