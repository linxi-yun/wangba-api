from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="网吧老板 API", description="模拟网吧上机业务逻辑")


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


# ========== 全局状态（模拟数据库，重启会丢，正好让你后面学数据库时更有动力） ==========
jiqi = 3
jiner = 0
hongzou = 0


# ========== 定义请求体模型（Pydantic 数据校验） ==========
class ShangjiRequest(BaseModel):
    age: int = Field(..., ge=1, le=120, description="顾客年龄")
    has_id: bool = Field(..., description="是否带身份证")

    class Config:
        schema_extra = {
            "example": {
                "age": 20,
                "has_id": True
            }
        }


# ========== API 接口 ==========
@app.get("/")
def read_root():
    return {"message": "网吧老板 API 已上线", "剩余机器": jiqi, "今日营收": jiner, "轰走未成年": hongzou}


@app.post("/shangji")
def shangji(request: ShangjiRequest):
    global jiqi, jiner, hongzou

    if jiqi == 0:
        return {"success": False, "message": "机器已满，明日请早"}

    # 把 bool 转换成你函数认识的 "y"/"n"
    daizheng_str = "y" if request.has_id else "n"

    new_ji, new_money, new_hong, msg = chuli_guke(
        request.age, daizheng_str, jiqi, jiner, hongzou
    )

    # 更新全局状态
    jiqi, jiner, hongzou = new_ji, new_money, new_hong

    return {
        "success": True,
        "message": msg,
        "剩余机器": jiqi,
        "今日营收": jiner,
        "轰走未成年": hongzou
    }


@app.post("/reset")
def reset():
    global jiqi, jiner, hongzou
    jiqi, jiner, hongzou = 3, 0, 0
    return {"success": True, "message": "新的一天开始", "剩余机器": jiqi}