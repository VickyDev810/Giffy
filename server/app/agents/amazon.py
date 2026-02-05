"""
Amazon Agent - Dummy Implementation
For non-quick-commerce gifts (longer delivery)
Replace with actual Amazon API integration
"""
import uuid
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta


class AmazonAgent:
    """
    Agent for interacting with Amazon
    For gifts that don't need instant delivery
    Currently returns dummy data - integrate with actual API later
    """

    BASE_URL = "https://amazon.in/api"  # Placeholder

    PRODUCTS = [
        {"id": "AZ001", "name": "Inflatable T-Rex Costume", "price": 1499, "available": True},
        {"id": "AZ002", "name": "Nicolas Cage Pillow", "price": 799, "available": True},
        {"id": "AZ003", "name": "100 Rubber Ducks", "price": 599, "available": True},
        {"id": "AZ004", "name": "Personalized Star Map", "price": 999, "available": True},
        {"id": "AZ005", "name": "RGB Keyboard", "price": 2499, "available": True},
        {"id": "AZ006", "name": "Funny T-Shirt Collection", "price": 699, "available": True},
        {"id": "AZ007", "name": "Board Game Bundle", "price": 1299, "available": True},
        {"id": "AZ008", "name": "LED Strip Lights", "price": 899, "available": True},
        {"id": "AZ009", "name": "Portable Projector", "price": 3999, "available": True},
        {"id": "AZ010", "name": "Wireless Earbuds", "price": 1999, "available": True},
        {"id": "AZ011", "name": "Coffee Maker", "price": 2499, "available": True},
        {"id": "AZ012", "name": "Kindle E-Reader", "price": 8999, "available": True},
        {"id": "AZ013", "name": "Smart Watch", "price": 4999, "available": True},
        {"id": "AZ014", "name": "Bluetooth Speaker", "price": 1499, "available": True},
        {"id": "AZ015", "name": "Photography Light Kit", "price": 1799, "available": True},
    ]

    @classmethod
    async def search_products(
        cls,
        query: str,
        min_price: float = 0,
        max_price: float = 50000,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search for products on Amazon"""
        query_lower = query.lower()
        results = []

        for product in cls.PRODUCTS:
            if min_price <= product["price"] <= max_price:
                # Simple keyword matching
                if query_lower in product["name"].lower() or random.random() < 0.3:
                    results.append({
                        **product,
                        "platform": "amazon",
                        "delivery_time": "1-3 days",
                        "prime": random.choice([True, False]),
                        "rating": round(random.uniform(3.5, 5.0), 1),
                        "reviews": random.randint(50, 5000),
                        "url": f"https://amazon.in/dp/{product['id']}"
                    })

        return results[:limit]

    @classmethod
    async def get_product_details(cls, product_id: str) -> Dict[str, Any]:
        """Get detailed product information"""
        product = next((p for p in cls.PRODUCTS if p["id"] == product_id), None)

        if not product:
            return {"error": "Product not found"}

        return {
            **product,
            "platform": "amazon",
            "description": f"A wonderful {product['name']} that makes a perfect gift!",
            "specifications": {
                "brand": "GiftCo",
                "category": "Gifts",
                "material": "Various"
            },
            "images": [
                f"https://placeholder.com/{product['id']}_1.jpg",
                f"https://placeholder.com/{product['id']}_2.jpg"
            ],
            "rating": round(random.uniform(3.5, 5.0), 1),
            "reviews": random.randint(50, 5000),
            "in_stock": product["available"]
        }

    @classmethod
    async def place_order(
        cls,
        product_name: str,
        delivery_address: str,
        price: float,
        quantity: int = 1,
        payment_method: str = "prepaid",
        gift_wrap: bool = True,
        gift_message: str = None
    ) -> Dict[str, Any]:
        """Place an order on Amazon"""
        success = random.random() < 0.95  # Amazon is usually reliable

        if not success:
            return {
                "success": False,
                "error": "Payment failed or item out of stock"
            }

        order_id = f"AZ-{uuid.uuid4().hex[:10].upper()}"
        delivery_days = random.randint(1, 4)
        estimated_delivery = datetime.utcnow() + timedelta(days=delivery_days)

        return {
            "success": True,
            "order_id": order_id,
            "platform": "amazon",
            "product_name": product_name,
            "quantity": quantity,
            "total_amount": price * quantity + (49 if gift_wrap else 0),
            "delivery_address": delivery_address,
            "payment_method": payment_method,
            "gift_wrap": gift_wrap,
            "gift_message": gift_message,
            "estimated_delivery": estimated_delivery.isoformat(),
            "tracking_url": f"https://amazon.in/track/{order_id}",
            "status": "confirmed"
        }

    @classmethod
    async def get_order_status(cls, order_id: str) -> Dict[str, Any]:
        """Get order status"""
        statuses = [
            "order_placed",
            "processing",
            "shipped",
            "out_for_delivery",
            "delivered"
        ]

        return {
            "order_id": order_id,
            "status": random.choice(statuses),
            "platform": "amazon",
            "last_updated": datetime.utcnow().isoformat(),
            "tracking_url": f"https://amazon.in/track/{order_id}"
        }

    @classmethod
    async def cancel_order(cls, order_id: str) -> Dict[str, Any]:
        """Cancel an order"""
        success = random.random() < 0.8

        return {
            "order_id": order_id,
            "cancelled": success,
            "refund_status": "initiated" if success else None,
            "refund_time": "5-7 business days" if success else None,
            "error": "Order already shipped" if not success else None
        }
