# -*- coding: utf-8 -*-
"""
===================================
如意金股 (RuyiDailyStockAnalysis) - 公共 Schema
===================================

职责：
1. 定义 API 通用请求/响应模型
2. 提供类型提示和文档生成支持
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """健康检查响应"""

    status: str = Field(..., description="服务运行状态", json_schema_extra={"example": "ok"})
    timestamp: str = Field(..., description="当前时间戳", json_schema_extra={"example": "2026-01-15T10:30:00"})

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "status": "ok",
            "timestamp": "2026-01-15T10:30:00"
        }
    })


class RootResponse(BaseModel):
    """API 根路由响应"""

    message: str = Field(..., description="API 运行状态消息", json_schema_extra={"example": "RuyiDailyStockAnalysis API is running"})
    version: Optional[str] = Field(None, description="API 版本", json_schema_extra={"example": "1.0.0"})

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "message": "RuyiDailyStockAnalysis API is running",
            "version": "1.0.0"
        }
    })
