import os
from datetime import datetime
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from app.models.models import User, Category
from app.services.report_generator import ReportGenerator
from app.services.email_service import EmailService

class NotificationService:
    def __init__(self):
        self.report_generator = ReportGenerator()
        self.email_service = EmailService()

    async def send_daily_report(
        self,
        user_id: int,
        email_enabled: bool = True,
        pdf_enabled: bool = True,
        in_app_enabled: bool = True,
        background_tasks: BackgroundTasks = None
    ):
        """Send daily report through specified channels"""
        # Generate report content
        report_content = await self.report_generator.generate_daily_report(user_id)

        if email_enabled:
            # Send email in background if background_tasks is provided
            if background_tasks:
                background_tasks.add_task(
                    self.email_service.send_email,
                    user_id=user_id,
                    subject="Your Daily AI Navigator Report",
                    content=report_content
                )
            else:
                await self.email_service.send_email(
                    user_id=user_id,
                    subject="Your Daily AI Navigator Report",
                    content=report_content
                )

        if pdf_enabled:
            pdf_path = await self.report_generator.generate_pdf_report(
                user_id=user_id,
                content=report_content
            )
            # Store PDF path or send it via email

        if in_app_enabled:
            # Store report in database for in-app access
            await self.store_in_app_notification(
                user_id=user_id,
                content=report_content
            )

    async def store_in_app_notification(self, user_id: int, content: str):
        """Store notification for in-app access"""
        # Implementation for storing in-app notifications
        # This could involve creating a new table for notifications
        # and storing the content there
        pass
