"""
Gift Agent Service
Handles AI-powered gift selection based on persona and vibe prompts
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional, Dict, Any
import random


class GiftAgentService:
    """
    AI Agent for selecting and ordering gifts
    Currently uses dummy data - integrate with actual AI/LLM later
    """

    # Dummy gift database based on vibes
    GIFT_CATALOG = {
        "chaotic": [
            {"name": "Screaming Goat Toy", "price": 299, "description": "A goat that screams when you squeeze it", "image_url": "https://placeholder.com/goat.jpg"},
            {"name": "Inflatable T-Rex Costume", "price": 1499, "description": "Become a dinosaur instantly", "image_url": "https://placeholder.com/trex.jpg"},
            {"name": "100 Rubber Ducks", "price": 599, "description": "For absolutely no reason", "image_url": "https://placeholder.com/ducks.jpg"},
            {"name": "Nicolas Cage Pillow", "price": 799, "description": "Sleep with Nicolas Cage's face", "image_url": "https://placeholder.com/cage.jpg"},
        ],
        "roast": [
            {"name": "World's Okayest Friend Mug", "price": 349, "description": "They're okay, I guess", "image_url": "https://placeholder.com/mug.jpg"},
            {"name": "Participation Trophy", "price": 199, "description": "For trying their best", "image_url": "https://placeholder.com/trophy.jpg"},
            {"name": "'I Survived Another Meeting' Notepad", "price": 149, "description": "For the corporate warrior", "image_url": "https://placeholder.com/notepad.jpg"},
        ],
        "thoughtful": [
            {"name": "Personalized Star Map", "price": 999, "description": "The night sky from a special date", "image_url": "https://placeholder.com/starmap.jpg"},
            {"name": "Custom Photo Book", "price": 1299, "description": "Memories in print", "image_url": "https://placeholder.com/photobook.jpg"},
            {"name": "Handwritten Letter Kit", "price": 499, "description": "Old school vibes", "image_url": "https://placeholder.com/letter.jpg"},
        ],
        "foodie": [
            {"name": "Exotic Snack Box", "price": 799, "description": "Snacks from around the world", "image_url": "https://placeholder.com/snacks.jpg"},
            {"name": "Instant Noodle Variety Pack", "price": 599, "description": "20 different flavors", "image_url": "https://placeholder.com/noodles.jpg"},
            {"name": "Hot Sauce Challenge Set", "price": 899, "description": "From mild to DEATH", "image_url": "https://placeholder.com/hotsauce.jpg"},
        ],
        "techie": [
            {"name": "USB Pet Rock", "price": 299, "description": "Does absolutely nothing, digitally", "image_url": "https://placeholder.com/usbrock.jpg"},
            {"name": "Keyboard Waffle Maker", "price": 1999, "description": "Ctrl+Alt+Breakfast", "image_url": "https://placeholder.com/waffle.jpg"},
            {"name": "RGB Everything Kit", "price": 1499, "description": "Make anything glow", "image_url": "https://placeholder.com/rgb.jpg"},
        ],
        "default": [
            {"name": "Mystery Box", "price": 499, "description": "Who knows what's inside?", "image_url": "https://placeholder.com/mystery.jpg"},
            {"name": "Plant That's Hard to Kill", "price": 399, "description": "Even they can't mess this up", "image_url": "https://placeholder.com/plant.jpg"},
            {"name": "Cozy Socks", "price": 299, "description": "Everyone needs socks", "image_url": "https://placeholder.com/socks.jpg"},
        ]
    }

    VIBE_KEYWORDS = {
        "chaotic": ["chaotic", "crazy", "wild", "random", "weird", "absurd", "unhinged"],
        "roast": ["roast", "burn", "tease", "joke", "funny", "savage", "brutal"],
        "thoughtful": ["thoughtful", "sweet", "meaningful", "sentimental", "heartfelt"],
        "foodie": ["food", "eat", "snack", "hungry", "delicious", "taste", "cook"],
        "techie": ["tech", "nerd", "geek", "computer", "gaming", "code", "gadget"],
    }

    @classmethod
    def _detect_vibe(cls, prompt: str) -> str:
        """Detect vibe category from prompt"""
        prompt_lower = prompt.lower()
        for vibe, keywords in cls.VIBE_KEYWORDS.items():
            if any(kw in prompt_lower for kw in keywords):
                return vibe
        return "default"

    @classmethod
    def _select_gift(cls, vibe: str, budget_min: float, budget_max: float) -> Optional[Dict[str, Any]]:
        """Select a gift based on vibe and budget"""
        catalog = cls.GIFT_CATALOG.get(vibe, cls.GIFT_CATALOG["default"])
        suitable_gifts = [g for g in catalog if budget_min <= g["price"] <= budget_max]

        if not suitable_gifts:
            # Fall back to any gift in budget
            all_gifts = [g for gifts in cls.GIFT_CATALOG.values() for g in gifts]
            suitable_gifts = [g for g in all_gifts if budget_min <= g["price"] <= budget_max]

        if suitable_gifts:
            return random.choice(suitable_gifts)
        return None

    @classmethod
    def _generate_reasoning(cls, vibe: str, gift: Dict[str, Any], persona_data: Dict = None) -> str:
        """Generate AI reasoning for gift selection"""
        reasons = {
            "chaotic": f"Based on the chaotic vibe requested, I picked '{gift['name']}' because it's absolutely unhinged and will definitely get a reaction!",
            "roast": f"For maximum roasting potential, '{gift['name']}' is perfect. It's funny but not too mean - the sweet spot of friendship roasts.",
            "thoughtful": f"'{gift['name']}' shows you really care and put thought into this gift. It's meaningful without being over the top.",
            "foodie": f"For the food lover in your life, '{gift['name']}' is a delicious choice that'll definitely be appreciated (and devoured).",
            "techie": f"'{gift['name']}' is peak tech humor - your friend will either love it or question your sanity. Either way, mission accomplished.",
            "default": f"'{gift['name']}' is a solid choice that works for pretty much anyone. Safe but still fun!"
        }
        return reasons.get(vibe, reasons["default"])

    @classmethod
    async def pick_gift(cls, gift_id: int, db_url: str):
        """Background task to pick a gift"""
        from app.models.gift import Gift, GiftStatus
        from app.models.persona import Persona

        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        db = Session()

        try:
            gift = db.query(Gift).filter(Gift.id == gift_id).first()
            if not gift:
                return

            # Get recipient persona
            persona = db.query(Persona).filter(Persona.user_id == gift.recipient_id).first()
            persona_data = None
            if persona:
                persona_data = {
                    "vibe_tags": persona.vibe_tags or [],
                    "interests": persona.interests or [],
                    "gift_style": persona.gift_style
                }

            # Detect vibe from prompt
            vibe = cls._detect_vibe(gift.vibe_prompt or "")

            # If persona has preferences, factor them in
            if persona_data and persona_data.get("gift_style"):
                vibe = persona_data["gift_style"]

            # Select gift
            selected = cls._select_gift(vibe, gift.budget_min, gift.budget_max)

            if selected:
                gift.gift_name = selected["name"]
                gift.gift_description = selected["description"]
                gift.gift_image_url = selected["image_url"]
                gift.gift_price = selected["price"]
                gift.agent_reasoning = cls._generate_reasoning(vibe, selected, persona_data)

                if gift.is_surprise:
                    gift.status = GiftStatus.ORDERED
                    gift.ordered_at = datetime.utcnow()
                else:
                    gift.status = GiftStatus.AWAITING_APPROVAL
            else:
                gift.status = GiftStatus.CANCELLED
                gift.agent_reasoning = "Could not find a suitable gift within the budget range."

            db.commit()
        finally:
            db.close()

    @classmethod
    async def place_order(cls, gift_id: int, db_url: str):
        """Background task to place order with delivery platform"""
        from app.models.gift import Gift, GiftStatus, DeliveryPlatform
        from app.agents.blinkit import BlinkitAgent
        from app.agents.zepto import ZeptoAgent

        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        db = Session()

        try:
            gift = db.query(Gift).filter(Gift.id == gift_id).first()
            if not gift:
                return

            # Try Blinkit first, then Zepto
            order_result = await BlinkitAgent.place_order(
                product_name=gift.gift_name,
                delivery_address=gift.delivery_address,
                price=gift.gift_price
            )

            if not order_result.get("success"):
                order_result = await ZeptoAgent.place_order(
                    product_name=gift.gift_name,
                    delivery_address=gift.delivery_address,
                    price=gift.gift_price
                )
                if order_result.get("success"):
                    gift.platform = DeliveryPlatform.ZEPTO
            else:
                gift.platform = DeliveryPlatform.BLINKIT

            if order_result.get("success"):
                gift.order_id = order_result.get("order_id")
                gift.tracking_url = order_result.get("tracking_url")
                gift.status = GiftStatus.SHIPPED
            else:
                gift.status = GiftStatus.CANCELLED
                gift.agent_reasoning += f"\n\nOrder failed: {order_result.get('error', 'Unknown error')}"

            db.commit()
        finally:
            db.close()

    @classmethod
    async def pick_and_order_gift(cls, gift_id: int, db_url: str):
        """Combined pick and order for YOLO/surprise mode"""
        await cls.pick_gift(gift_id, db_url)
        await cls.place_order(gift_id, db_url)
