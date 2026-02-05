"""
Gift Subscription Scheduler
Handles automated recurring gift sending
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models.gift import Gift, GiftSubscription, GiftStatus
from app.models.persona import Persona
from app.services.gift_agent import GiftAgentService
import logging

logger = logging.getLogger(__name__)


class GiftScheduler:
    """Scheduler for recurring gift subscriptions"""

    _scheduler: AsyncIOScheduler = None

    @classmethod
    def get_scheduler(cls) -> AsyncIOScheduler:
        """Get or create scheduler instance"""
        if cls._scheduler is None:
            cls._scheduler = AsyncIOScheduler()
        return cls._scheduler

    @classmethod
    def start(cls):
        """Start the scheduler"""
        scheduler = cls.get_scheduler()

        # Check subscriptions every hour
        scheduler.add_job(
            cls.process_subscriptions,
            CronTrigger(minute=0),  # Every hour at :00
            id="process_gift_subscriptions",
            replace_existing=True
        )

        # Also run immediately on startup
        scheduler.add_job(
            cls.process_subscriptions,
            "date",
            run_date=datetime.utcnow() + timedelta(seconds=10),
            id="initial_subscription_check"
        )

        scheduler.start()
        logger.info("Gift scheduler started")

    @classmethod
    def stop(cls):
        """Stop the scheduler"""
        if cls._scheduler:
            cls._scheduler.shutdown()
            logger.info("Gift scheduler stopped")

    @classmethod
    async def process_subscriptions(cls):
        """Process all active subscriptions that are due"""
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            logger.info(f"Processing gift subscriptions at {now}")

            # Get active subscriptions
            subscriptions = db.query(GiftSubscription).filter(
                GiftSubscription.is_active == True
            ).all()

            for sub in subscriptions:
                if cls._is_due(sub, now):
                    await cls._send_subscription_gift(sub, db)

        except Exception as e:
            logger.error(f"Error processing subscriptions: {e}")
        finally:
            db.close()

    @classmethod
    def _is_due(cls, subscription: GiftSubscription, now: datetime) -> bool:
        """Check if subscription is due for sending"""
        # Parse time
        try:
            hour, minute = map(int, subscription.time_of_day.split(":"))
        except (ValueError, AttributeError):
            hour, minute = 10, 0

        # Check if current time matches
        if now.hour != hour:
            return False

        # Check frequency
        if subscription.frequency == "daily":
            # Check if already sent today
            if subscription.last_sent_at:
                if subscription.last_sent_at.date() == now.date():
                    return False
            return True

        elif subscription.frequency == "weekly":
            # Check day of week (0 = Monday)
            if now.weekday() != subscription.day_of_week:
                return False
            # Check if already sent this week
            if subscription.last_sent_at:
                days_since = (now - subscription.last_sent_at).days
                if days_since < 7:
                    return False
            return True

        elif subscription.frequency == "monthly":
            # Check day of month
            if now.day != subscription.day_of_month:
                return False
            # Check if already sent this month
            if subscription.last_sent_at:
                if (subscription.last_sent_at.year == now.year and
                    subscription.last_sent_at.month == now.month):
                    return False
            return True

        return False

    @classmethod
    async def _send_subscription_gift(cls, subscription: GiftSubscription, db: Session):
        """Send a gift for a subscription"""
        try:
            logger.info(f"Sending subscription gift {subscription.id} to user {subscription.recipient_id}")

            # Get recipient's persona for delivery address
            persona = db.query(Persona).filter(
                Persona.user_id == subscription.recipient_id
            ).first()

            delivery_address = persona.default_address if persona else None

            if not delivery_address:
                logger.warning(f"No delivery address for subscription {subscription.id}")
                return

            # Create gift
            gift = Gift(
                sender_id=subscription.sender_id,
                recipient_id=subscription.recipient_id,
                vibe_prompt=subscription.vibe_prompt,
                budget_min=subscription.budget_min,
                budget_max=subscription.budget_max,
                is_surprise=True,  # Subscriptions are always surprise
                delivery_address=delivery_address,
                status=GiftStatus.AGENT_PICKING,
                sender_message=f"Automated gift from your subscription!"
            )
            db.add(gift)
            db.commit()
            db.refresh(gift)

            # Update subscription
            subscription.last_sent_at = datetime.utcnow()
            subscription.total_gifts_sent = (subscription.total_gifts_sent or 0) + 1

            # Calculate next send time
            if subscription.frequency == "daily":
                subscription.next_send_at = datetime.utcnow() + timedelta(days=1)
            elif subscription.frequency == "weekly":
                subscription.next_send_at = datetime.utcnow() + timedelta(weeks=1)
            elif subscription.frequency == "monthly":
                subscription.next_send_at = datetime.utcnow() + timedelta(days=30)

            db.commit()

            # Trigger agent to pick and order gift
            await GiftAgentService.pick_and_order_gift(
                gift_id=gift.id,
                db_url=str(db.get_bind().url)
            )

            logger.info(f"Subscription gift {gift.id} created successfully")

        except Exception as e:
            logger.error(f"Error sending subscription gift: {e}")
            db.rollback()


async def start_scheduler():
    """Start the gift scheduler"""
    GiftScheduler.start()


def stop_scheduler():
    """Stop the gift scheduler"""
    GiftScheduler.stop()
