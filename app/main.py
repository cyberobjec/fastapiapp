from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db, engine
from app.models.users import Base  # ✅ 放在 app 定义之前导入

# 1️⃣ 先创建 app 实例
app = FastAPI(title="minimal-api", version="0.0.2")

# 2️⃣ 注册启动事件（在这里建表）
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 3️⃣ 定义路由
@app.get("/healthz")
async def health():
    return {"status": "ok"}

@app.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1 AS ok"))
        return {"db_ok": result.scalar() == 1}
    except Exception as e:
        return {"db_ok": False, "error": str(e)}
