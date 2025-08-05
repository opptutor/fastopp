#!/usr/bin/env python3
"""
Script to add sample webinar registrants for testing photo upload functionality
"""

import asyncio
import uuid
from datetime import datetime, timezone
from db import AsyncSessionLocal
from models import WebinarRegistrants


async def add_sample_registrants():
    """Add sample webinar registrants to the database"""
    
    sample_registrants = [
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "company": "Tech Corp",
            "webinar_title": "Advanced FastAPI Development",
            "webinar_date": datetime(2024, 2, 15, 14, 0, tzinfo=timezone.utc),
            "status": "registered"
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@startup.io",
            "company": "Startup Inc",
            "webinar_title": "Building Scalable APIs",
            "webinar_date": datetime(2024, 2, 20, 10, 0, tzinfo=timezone.utc),
            "status": "attended"
        },
        {
            "name": "Michael Chen",
            "email": "michael.chen@enterprise.com",
            "company": "Enterprise Solutions",
            "webinar_title": "Database Design Best Practices",
            "webinar_date": datetime(2024, 2, 25, 16, 0, tzinfo=timezone.utc),
            "status": "registered"
        },
        {
            "name": "Emily Davis",
            "email": "emily.davis@freelance.dev",
            "company": "Freelance Developer",
            "webinar_title": "Modern Web Development",
            "webinar_date": datetime(2024, 3, 1, 13, 0, tzinfo=timezone.utc),
            "status": "registered"
        },
        {
            "name": "David Wilson",
            "email": "david.wilson@consulting.co",
            "company": "Tech Consulting",
            "webinar_title": "API Security Fundamentals",
            "webinar_date": datetime(2024, 3, 5, 15, 0, tzinfo=timezone.utc),
            "status": "registered"
        }
    ]
    
    async with AsyncSessionLocal() as session:
        for registrant_data in sample_registrants:
            # Check if registrant already exists
            from sqlmodel import select
            existing = await session.execute(
                select(WebinarRegistrants).where(WebinarRegistrants.email == registrant_data['email'])
            )
            if existing.scalar_one_or_none():
                print(f"Registrant {registrant_data['email']} already exists, skipping...")
                continue
            
            # Create new registrant
            registrant = WebinarRegistrants(
                id=uuid.uuid4(),
                name=registrant_data['name'],
                email=registrant_data['email'],
                company=registrant_data['company'],
                webinar_title=registrant_data['webinar_title'],
                webinar_date=registrant_data['webinar_date'],
                status=registrant_data['status']
            )
            
            session.add(registrant)
            print(f"Added registrant: {registrant_data['name']} ({registrant_data['email']})")
        
        await session.commit()
        print(f"\nSuccessfully added {len(sample_registrants)} sample webinar registrants!")


if __name__ == "__main__":
    asyncio.run(add_sample_registrants()) 