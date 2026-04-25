#       E:
# cd "E:\我的项目\wangba"
# set WANGBA_MACHINES=30
#       uvicorn wangba_api:app --reload
#关闭py       taskkill /f /im python.exe
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
import sqlite3
import os

# l从环境变量读取机器总数，getenv会读取系统里名叫 WANGBA_MACHINES 的环境变量，如果没设置就默认3台
TOTAL_MACHINES = int(os.getenv("WANGBA_MACHINES", "3"))


app = FastAPI(title="网吧老板 API", description="模拟网吧上机业务逻辑")


# ========== 数据库初始化 =====================================
DB_PATH = "wangba.db"

def init_db():
    """创建数据库表（如果不存在）"""
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
        # 注意这里加上了 id 列和值 1
        cursor.execute(
            f"INSERT INTO wangba_state (id, 剩余机器, 今日营收, 轰走未成年) VALUES (1, {TOTAL_MACHINES}, 0, 0)")
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

# 服务启动时自动初始化数据库
init_db()


# ========== 你的核心逻辑函数（一字未改，只加了类型注解） ==========
def chuli_guke(nianling: int, daizheng: str, shengyujiqi: int, dangqianjiner: int, hongzourenshu: int):
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



# ========== 定义请求体模型（Pydantic 数据校验） ==========
#用自定义类定义数据模型，BaseModel 是 Pydantic 库中的基类。
class ShangjiRequest(BaseModel):
    # 注意：去掉了 Field 里的 ge 和 le 参数
    age: int = Field(..., description="顾客年龄")
    has_id: bool = Field(..., description="是否带身份证")

    @field_validator('age')
    def check_age(cls, v):
        # 你的自定义中文提示逻辑写在这里
        if v < 1:
            raise ValueError('年龄不能为负数，请重新输入！')
        if v > 120:
            raise ValueError('输入年龄过大，请确认后再试！')
        return v

    class Config:
        schema_extra = {
            "example": {
                "age": 20,
                "has_id": True
            }
        }


# ========== API 接口 ==========
@app.get("/")#是 FastAPI() 类的实例（例如：app = FastAPI()）。
def read_root():#这是处理请求的函数。当用户访问根路径（例如 http://127.0.0.1:8000/）时，该函数会被调用。
    state = get_state()  # 从数据库读取状态.
    return {
        "message": "网吧老板 API 已上线",
        "剩余机器": state["剩余机器"],
        "今日营收": state["今日营收"],
        "轰走未成年": state["轰走未成年"]
    }



# ========== 全局状态（模拟数据库，重启会丢，正好让你后面学数据库时更有动力） 必须放class ShangjiRequest函数后面==========

@app.post("/shangji")
def shangji(request: ShangjiRequest):
    state = get_state()  # 从数据库读取状态

    if state["剩余机器"] == 0:
        return {"success": False, "message": "机器已满，明日请早"}

    daizheng_str = "y" if request.has_id else "n"

    new_ji, new_money, new_hong, msg = chuli_guke(
        request.age, daizheng_str,
        state["剩余机器"], state["今日营收"], state["轰走未成年"]
    )

    update_state(new_ji, new_money, new_hong)  # 保存到数据库

    return {
        "success": True,
        "message": msg,
        "剩余机器": new_ji,
        "今日营收": new_money,
        "轰走未成年": new_hong
    }



@app.post("/reset")
def reset():
    update_state(TOTAL_MACHINES, 0, 0)
    return {"success": True, "message": "新的一天开始", "剩余机器": TOTAL_MACHINES}
