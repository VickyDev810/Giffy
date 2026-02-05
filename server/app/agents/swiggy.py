"""
Swiggy Instamart Agent - Dummy Implementation
Replace with actual Swiggy API integration
"""
import uuid
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta


class SwiggyInstamartAgent:
    """
    Agent for interacting with Swiggy Instamart
    Currently returns dummy data - integrate with actual API later
    """

    BASE_URL = "https://swiggy.com/api/instamart"  # Placeholder

    PRODUCTS = [
        {"id": "SW001", "name": "Gourmet Snacks Box", "price": 599, "available": True},
        {"id": "SW002", "name": "Fresh Fruit Basket", "price": 799, "available": True},
        {"id": "SW003", "name": "Bakery Treats Box", "price": 449, "available": True},
        {"id": "SW004", "name": "Artisan Cheese Selection", "price": 999, "available": True},
        {"id": "SW005", "name": "Premium Tea Collection", "price": 649, "available": True},
        {"id": "SW006", "name": "Organic Essentials Kit", "price": 899, "available": True},
        {"id": "SW007", "name": "Breakfast Bundle", "price": 549, "available": True},
        {"id": "SW008", "name": "International Snacks", "price": 749, "available": True},
    ]

    @classmethod
    async def search_products(
        cls,
        query: str,
        min_price: float = 0,
        max_price: float = 10000,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for products"""
        query_lower = query.lower()
        results = []

        for product in cls.PRODUCTS:
            if (query_lower in product["name"].lower() and
                min_price <= product["price"] <= max_price):
                results.append({
                    **product,
                    "platform": "swiggy_instamart",
                    "delivery_time": "15-25 mins",
                    "url": f"https://swiggy.com/instamart/product/{product['id']}"
                })

        return results[:limit]

    @classmethod
    async def place_order(
        cls,
        product_name: str,
        delivery_address: str,
        price: float,
        quantity: int = 1,
        payment_method: str = "prepaid"
    ) -> Dict[str, Any]:
        """Place an order"""
        success = random.random() < 0.80

        if not success:
            return {
                "success": False,
                "error": "Store closed or product unavailable"
            }

        order_id = f"SW-{uuid.uuid4().hex[:8].upper()}"
        estimated_delivery = datetime.utcnow() + timedelta(minutes=random.randint(15, 30))

        return {
            "success": True,
            "order_id": order_id,
            "platform": "swiggy_instamart",
            "product_name": product_name,
            "quantity": quantity,
            "total_amount": price * quantity,
            "delivery_address": delivery_address,
            "estimated_delivery": estimated_delivery.isoformat(),
            "tracking_url": f"https://swiggy.com/track/{order_id}",
            "status": "confirmed"
        }

    @classmethod
    async def get_order_status(cls, order_id: str) -> Dict[str, Any]:
        """Get order status"""
        statuses = ["placed", "preparing", "picked_up", "on_the_way", "delivered"]
        return {
            "order_id": order_id,
            "status": random.choice(statuses),
            "platform": "swiggy_instamart"
        }
