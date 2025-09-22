from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db_session
from .config import Settings, get_settings


def get_product_service(
    session = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
) -> "ProductService":
    """Dependency to get ProductService instance"""
    from services.product_service import ProductService
    return ProductService(session=session, settings=settings)


def get_webinar_service(
    session = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
) -> "WebinarService":
    """Dependency to get WebinarService instance"""
    from services.webinar_service import WebinarService
    return WebinarService(session=session, settings=settings)


def get_chat_service(
    settings: Settings = Depends(get_settings)
) -> "ChatService":
    """Dependency to get ChatService instance"""
    from services.chat_service import ChatService
    return ChatService(settings=settings)
