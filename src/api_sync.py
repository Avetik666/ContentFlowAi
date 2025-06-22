from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .social_agent import generate_social_calendar

app = FastAPI(title="ContentFlow AI (sync demo)")


class ContentReq(BaseModel):
    url: str
    platform: str = Field("instagram", pattern="^[a-z]+$")
    posts: int = Field(7, ge=1, le=20)
    interval: str = Field("day", pattern="^(day|week)$")
    extra: str = ""


@app.post("/generate-sync")
async def generate_sync(req: ContentReq):
    try:
        calendar = await generate_social_calendar(
            n_posts=req.posts,
            interval=req.interval,
            url=req.url,
            platform=req.platform,
            extra_info=req.extra,
        )
        return calendar
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e)) from e
