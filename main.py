import asyncio
import shutil
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from pathlib import Path


class Cpu(BaseModel):
    ms: int = Field(default=10000, gt=0, lt=60000)


class Memory(BaseModel):
    mb: int = Field(default=600, gt=0, lt=4096)
    hold_ms: int = Field(default=5000, gt=0, lt=300000)


class File(BaseModel):
    filename: str = Field(default="main.py"),
    copies: int = Field(default=10, gt=0, lt=10_000),
    prefix: str = Field(default="disk_fill_"),


app = FastAPI()


@app.get("/healthz")
def healthz():
    """
    헬스엔드포인트
    """
    return {"status": "ok"}


@app.post("/simulate/cpu")
async def simulate_cpu(item: Cpu):
    """
    CPU 바쁘게
    """
    end = time.perf_counter() + (item.ms / 1000.0)
    while time.perf_counter() < end:
        _ = sum(i * i for i in range(2000))
        await asyncio.sleep(0)
    return {"cpu_busy_ms": item.ms}


@app.post("/simulate/memory-spike")
async def simulate_memory_spike(item: Memory):
    """
    메모리 스파이크(일시적 고사용)
    """
    buf = bytearray(item.mb * 1024 * 1024)
    for i in range(0, len(buf), 4096):
        buf[i] = 1

    # 지정 시간 동안만 메모리를 쥐고 있음
    if item.hold_ms:
        await asyncio.sleep(item.hold_ms / 1000.0)

    return {"spiked_mb": item.mb, "hold_ms": item.hold_ms}


@app.post("/simulate/disk-fill")
async def simulate_disk_fill(item: File):
    base_dir = Path(__file__).resolve().parent
    src = base_dir / item.filename
    if not src.is_file():
        raise HTTPException(400, detail=f"source file not found: {item.filename}")

    created: List[str] = []
    total_bytes = 0

    for i in range(item.copies):
        ts = int(time.time() * 1000)
        dst = base_dir / f"{item.prefix}{ts}_{i}{src.suffix}"
        shutil.copy2(src, dst)
        created.append(str(dst))
        total_bytes += dst.stat().st_size

    return {
        "source": str(src),
        "created_count": len(created),
        "approx_bytes_used": total_bytes,
    }


@app.post("/simulate/router-nuke")
async def simulate_router_nuke():
    """
    현재 라우터를 날려버리고 빈 라우터로 교체
    """
    app.router.routes.clear()
    return {"status": "router nuked"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8888, workers=1)
