from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db_session
from .config import Settings, get_settings


def get_product_service(
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
):
    """Dependency to get ProductService instance"""
    from services.product_service import ProductService
    return ProductService(session=session, settings=settings)


def get_webinar_service(
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
):
    """Dependency to get WebinarService instance"""
    from services.webinar_service import WebinarService
    return WebinarService(session=session, settings=settings)


def get_chat_service(
    settings: Settings = Depends(get_settings)
):
    """Dependency to get ChatService instance"""
    from services.chat_service import ChatService
    return ChatService(settings=settings)
