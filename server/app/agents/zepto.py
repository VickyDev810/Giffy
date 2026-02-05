"""
Zepto Agent - Dummy Implementation
Replace with actual Zepto API integration
"""
import uuid
import random
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class ZeptoAgent:
    """
    Agent for interacting with Zepto (quick commerce)
    Currently returns dummy data - integrate with actual API later
    """

    BASE_URL = "https://zepto.com/api"  # Placeholder

    # Dummy product catalog
    PRODUCTS = [
        {"id": "ZP001", "name": "Party Snack Combo", "price": 349, "available": True},
        {"id": "ZP002", "name": "Instant Ramen Collection", "price": 449, "available": True},
        {"id": "ZP003", "name": "Chips & Dips Party Pack", "price": 599, "available": True},
        {"id": "ZP004", "name": "Energy Drink Bundle", "price": 399, "available": True},
        {"id": "ZP005", "name": "Ice Cream Tub Set", "price": 699, "available": True},
        {"id": "ZP006", "name": "Midnight Munchies Box", "price": 549, "available": True},
        {"id": "ZP007", "name": "Healthy Snacks Kit", "price": 649, "available": True},
        {"id": "ZP008", "name": "Chocolate Lovers Pack", "price": 799, "available": True},
        {"id": "ZP009", "name": "Quick Breakfast Set", "price": 449, "available": True},
        {"id": "ZP010", "name": "Beverages Combo", "price": 299, "available": True},
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
        Search for products on Zepto
        DUMMY: Returns matching products from mock catalog
        """
        query_lower = query.lower()
        results = []

        for product in cls.PRODUCTS:
            if (query_lower in product["name"].lower() and
                min_price <= product["price"] <= max_price):
                results.append({
                    **product,
                    "platform": "zepto",
                    "delivery_time": "8-12 mins",
                    "url": f"https://zepto.com/product/{product['id']}"
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

        available = random.random() < 0.88

        return {
            "product_id": product_id,
            "pincode": pincode,
            "available": available,
            "delivery_time": "8-12 mins" if available else None,
            "platform": "zepto"
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
        Place an order on Zepto
        DUMMY: Returns mock order confirmation
        """
        success = random.random() < 0.82

        if not success:
            return {
                "success": False,
                "error": "Delivery not available in your location"
            }

        order_id = f"ZP-{uuid.uuid4().hex[:8].upper()}"
        estimated_delivery = datetime.utcnow() + timedelta(minutes=random.randint(8, 15))

        return {
            "success": True,
            "order_id": order_id,
            "platform": "zepto",
            "product_name": product_name,
            "quantity": quantity,
            "total_amount": price * quantity,
            "delivery_address": delivery_address,
            "payment_method": payment_method,
            "estimated_delivery": estimated_delivery.isoformat(),
            "tracking_url": f"https://zepto.com/track/{order_id}",
            "status": "confirmed"
        }

    @classmethod
    async def get_order_status(cls, order_id: str) -> Dict[str, Any]:
        """Get order status"""
        statuses = ["confirmed", "packing", "out_for_delivery", "delivered"]
        current_status = random.choice(statuses)

        return {
            "order_id": order_id,
            "status": current_status,
            "platform": "zepto",
            "last_updated": datetime.utcnow().isoformat(),
            "tracking_url": f"https://zepto.com/track/{order_id}"
        }

    @classmethod
    async def cancel_order(cls, order_id: str) -> Dict[str, Any]:
        """Cancel an order"""
        success = random.random() < 0.65

        return {
            "order_id": order_id,
            "cancelled": success,
            "refund_status": "processing" if success else None,
            "error": "Cannot cancel, order is being packed" if not success else None
        }
