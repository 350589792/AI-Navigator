from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import User, NotificationSetting
from app.services.notification import NotificationService


class SchedulerService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService()

    async def check_scheduled_reports(self):
        """Check and trigger scheduled reports"""
        current_time = datetime.utcnow()

        # Get all active notification settings
        settings = (
            self.db.query(NotificationSetting)
            .join(User)
            .filter(User.is_active.is_(True))
            .all()
        )

        for setting in settings:
            scheduled_time = setting.delivery_time.time()
            current_time_only = current_time.time()

            # Check if it's time to send the report
            if (
                scheduled_time.hour == current_time_only.hour
                and scheduled_time.minute == current_time_only.minute
            ):
                await self.notification_service.send_daily_report(
                    user_id=setting.user_id,
                    email_enabled=setting.email_enabled,
                    pdf_enabled=setting.pdf_enabled,
                    in_app_enabled=setting.in_app_enabled
                )

    async def update_notification_settings(
        self,
        user_id: int,
        delivery_time: datetime,
        email_enabled: bool,
        pdf_enabled: bool,
        in_app_enabled: bool
    ):
        """Update notification settings for a user"""
        setting = (
            self.db.query(NotificationSetting)
            .filter(NotificationSetting.user_id == user_id)
            .first()
        )

        if setting:
            setting.delivery_time = delivery_time
            setting.email_enabled = email_enabled
            setting.pdf_enabled = pdf_enabled
            setting.in_app_enabled = in_app_enabled
        else:
            setting = NotificationSetting(
                user_id=user_id,
                delivery_time=delivery_time,
                email_enabled=email_enabled,
                pdf_enabled=pdf_enabled,
                in_app_enabled=in_app_enabled
            )
            self.db.add(setting)

        self.db.commit()
        return setting
