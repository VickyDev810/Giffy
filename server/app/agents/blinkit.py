"""
Blinkit Agent - Dummy Implementation
Replace with actual Blinkit API integration
"""
import uuid
import random
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class BlinkitAgent:
    """
    Agent for interacting with Blinkit (quick commerce)
    Currently returns dummy data - integrate with actual API later
    """

    BASE_URL = "https://blinkit.com/api"  # Placeholder

    # Dummy product catalog
    PRODUCTS = [
        {"id": "BL001", "name": "Screaming Goat Toy", "price": 299, "available": True},
        {"id": "BL002", "name": "Mystery Snack Box", "price": 499, "available": True},
        {"id": "BL003", "name": "Exotic Chips Variety", "price": 399, "available": True},
        {"id": "BL004", "name": "Instant Noodle Pack", "price": 599, "available": True},
        {"id": "BL005", "name": "Premium Chocolate Box", "price": 799, "available": True},
        {"id": "BL006", "name": "Coffee Sampler Kit", "price": 699, "available": True},
        {"id": "BL007", "name": "Funny Mug Collection", "price": 349, "available": True},
        {"id": "BL008", "name": "Desk Plant Kit", "price": 449, "available": True},
        {"id": "BL009", "name": "Snack Attack Bundle", "price": 899, "available": True},
        {"id": "BL010", "name": "Cozy Socks Pack", "price": 299, "available": True},
    ]

    @classmethod
    async def search_products(
        cls,
        query: str,
        min_price: float = 0,
        max_price: float = 10000,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for products on Blinkit
        DUMMY: Returns matching products from mock catalog
        """
        query_lower = query.lower()
        results = []

        for product in cls.PRODUCTS:
            if (query_lower in product["name"].lower() and
                min_price <= product["price"] <= max_price):
                results.append({
                    **product,
                    "platform": "blinkit",
                    "delivery_time": "10-15 mins",
                    "url": f"https://blinkit.com/product/{product['id']}"
                })

        return results[:limit]

    @classmethod
    async def check_availability(
        cls,
        product_id: str,
        pincode: str
    ) -> Dict[str, Any]:
        """
        Check if product is available for delivery
        DUMMY: Returns random availability
        """
        product = next((p for p in cls.PRODUCTS if p["id"] == product_id), None)

        if not product:
            return {"available": False, "error": "Product not found"}

        # Simulate availability (90% chance available)
        available = random.random() < 0.9

        return {
            "product_id": product_id,
            "pincode": pincode,
            "available": available,
            "delivery_time": "10-15 mins" if available else None,
            "platform": "blinkit"
        }

    @classmethod
    async def place_order(
        cls,
        product_name: str,
        delivery_address: str,
        price: float,
        quantity: int = 1,
        payment_method: str = "prepaid"
    ) -> Dict[str, Any]:
        """
        Place an order on Blinkit
        DUMMY: Returns mock order confirmation
        """
        # Simulate order success (85% success rate)
        success = random.random() < 0.85

        if not success:
            return {
                "success": False,
                "error": "Product currently unavailable in your area"
            }

        order_id = f"BL-{uuid.uuid4().hex[:8].upper()}"
        estimated_delivery = datetime.utcnow() + timedelta(minutes=random.randint(10, 20))

        return {
            "success": True,
            "order_id": order_id,
            "platform": "blinkit",
            "product_name": product_name,
            "quantity": quantity,
            "total_amount": price * quantity,
            "delivery_address": delivery_address,
            "payment_method": payment_method,
            "estimated_delivery": estimated_delivery.isoformat(),
            "tracking_url": f"https://blinkit.com/track/{order_id}",
            "status": "confirmed"
        }

    @classmethod
    async def get_order_status(cls, order_id: str) -> Dict[str, Any]:
        """
        Get order status
        DUMMY: Returns mock status
        """
        statuses = ["confirmed", "preparing", "out_for_delivery", "delivered"]
        current_status = random.choice(statuses)

        return {
            "order_id": order_id,
            "status": current_status,
            "platform": "blinkit",
            "last_updated": datetime.utcnow().isoformat(),
            "tracking_url": f"https://blinkit.com/track/{order_id}"
        }

    @classmethod
    async def cancel_order(cls, order_id: str) -> Dict[str, Any]:
        """
        Cancel an order
        DUMMY: Returns mock cancellation
        """
        # 70% cancellation success (might be already shipped)
        success = random.random() < 0.7

        return {
            "order_id": order_id,
            "cancelled": success,
            "refund_status": "initiated" if success else None,
            "error": "Order already shipped" if not success else None
        }
