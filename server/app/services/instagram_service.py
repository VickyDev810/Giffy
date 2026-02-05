"""
Instagram Service
Uses instaloader to fetch public Instagram profile data
"""
import instaloader
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import asyncio


class InstagramService:
    """
    Service for fetching and analyzing Instagram data
    Uses instaloader for public profile access
    """

    _loader: Optional[instaloader.Instaloader] = None

    @classmethod
    def get_loader(cls) -> instaloader.Instaloader:
        """Get or create instaloader instance"""
        if cls._loader is None:
            cls._loader = instaloader.Instaloader(
                download_pictures=False,
                download_videos=False,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                compress_json=False
            )
        return cls._loader

    @classmethod
    async def fetch_profile(cls, username: str) -> Optional[Dict[str, Any]]:
        """Fetch public Instagram profile data"""
        try:
            loader = cls.get_loader()

            # Run in thread pool since instaloader is synchronous
            loop = asyncio.get_event_loop()
            profile = await loop.run_in_executor(
                None,
                lambda: instaloader.Profile.from_username(loader.context, username)
            )

            # Get recent posts (up to 12)
            recent_posts = []
            try:
                posts = profile.get_posts()
                for i, post in enumerate(posts):
                    if i >= 12:
                        break
                    recent_posts.append({
                        "shortcode": post.shortcode,
                        "caption": post.caption[:200] if post.caption else None,
                        "likes": post.likes,
                        "comments": post.comments,
                        "date": post.date_utc.isoformat(),
                        "is_video": post.is_video,
                        "url": f"https://instagram.com/p/{post.shortcode}/"
                    })
            except Exception:
                pass  # Posts might not be accessible

            return {
                "username": profile.username,
                "full_name": profile.full_name,
                "bio": profile.biography,
                "follower_count": profile.followers,
                "following_count": profile.followees,
                "post_count": profile.mediacount,
                "is_private": profile.is_private,
                "profile_pic_url": profile.profile_pic_url,
                "recent_posts": recent_posts
            }

        except instaloader.exceptions.ProfileNotExistsException:
            return None
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            return {
                "username": username,
                "is_private": True,
                "error": "Profile is private"
            }
        except Exception as e:
            print(f"Error fetching Instagram profile: {e}")
            return None

    @classmethod
    async def sync_profile(cls, connection_id: int, db_url: str):
        """Background task to sync Instagram profile data"""
        from app.models.social import SocialConnection
        from app.models.persona import Persona

        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        db = Session()

        try:
            connection = db.query(SocialConnection).filter(
                SocialConnection.id == connection_id
            ).first()

            if not connection or not connection.platform_username:
                return

            profile_data = await cls.fetch_profile(connection.platform_username)

            if profile_data and not profile_data.get("error"):
                connection.follower_count = profile_data.get("follower_count")
                connection.following_count = profile_data.get("following_count")
                connection.post_count = profile_data.get("post_count")
                connection.bio = profile_data.get("bio")
                connection.profile_data = profile_data
                connection.last_synced_at = datetime.utcnow()

                # Update user's persona with Instagram bio if available
                if profile_data.get("bio"):
                    persona = db.query(Persona).filter(
                        Persona.user_id == connection.user_id
                    ).first()
                    if persona and not persona.ai_summary:
                        # Generate simple summary from bio
                        persona.ai_summary = f"Instagram bio: {profile_data['bio']}"

                db.commit()

        except Exception as e:
            print(f"Error syncing Instagram: {e}")
        finally:
            db.close()

    @classmethod
    async def analyze_for_gifts(cls, username: str) -> Dict[str, Any]:
        """
        Analyze Instagram profile to suggest gift ideas using Gemini AI
        """
        from app.services.gemini_service import GeminiService

        profile = await cls.fetch_profile(username)

        if not profile or profile.get("error"):
            return {
                "success": False,
                "error": "Could not fetch profile. Account might be private or invalid."
            }

        # Use Gemini for deep analysis
        ai_analysis = await GeminiService.analyze_profile(profile)

        if ai_analysis:
            return {
                "success": True,
                "username": username,
                "detected_interests": ai_analysis.get("interests", []),
                "gift_suggestions": ai_analysis.get("gift_ideas", []),
                "vibe_tags": ai_analysis.get("vibe_tags", []),
                "ai_summary": ai_analysis.get("summary"),
                "profile_summary": {
                    "followers": profile.get("follower_count"),
                    "posts": profile.get("post_count"),
                    "bio": profile.get("bio"),
                    "full_name": profile.get("full_name"),
                    "profile_pic_url": profile.get("profile_pic_url")
                }
            }

        # Fallback to simple keyword-based analysis if AI fails
        interests = []
        gift_suggestions = []

        bio = (profile.get("bio") or "").lower()
        captions = " ".join([p.get("caption", "") or "" for p in profile.get("recent_posts", [])]).lower()
        combined_text = f"{bio} {captions}"

        # Interest detection
        interest_keywords = {
            "travel": ["travel", "wanderlust", "adventure", "explore", "trip", "vacation"],
            "food": ["food", "foodie", "eat", "cook", "chef", "restaurant", "recipe"],
            "fitness": ["fitness", "gym", "workout", "health", "yoga", "running"],
            "music": ["music", "concert", "band", "spotify", "playlist", "guitar"],
            "photography": ["photo", "camera", "canon", "nikon", "shoot", "photography"],
            "gaming": ["gaming", "gamer", "playstation", "xbox", "pc", "twitch"],
            "fashion": ["fashion", "style", "outfit", "ootd", "clothes", "shopping"],
            "books": ["book", "reading", "read", "author", "literature", "novel"],
            "tech": ["tech", "developer", "coding", "startup", "entrepreneur"],
            "art": ["art", "artist", "paint", "draw", "creative", "design"],
            "pets": ["dog", "cat", "pet", "puppy", "kitten", "animal"],
            "coffee": ["coffee", "cafe", "espresso", "latte", "caffeine"],
        }

        for interest, keywords in interest_keywords.items():
            if any(kw in combined_text for kw in keywords):
                interests.append(interest)

        # Gift suggestions based on interests
        gift_mapping = {
            "travel": ["Travel journal", "World map poster", "Portable charger"],
            "food": ["Cooking masterclass", "Exotic spice set", "Food delivery subscription"],
            "fitness": ["Fitness tracker", "Yoga mat", "Protein shaker"],
            "music": ["Spotify premium", "Vinyl record", "Concert tickets"],
            "photography": ["Camera strap", "Photo printing credits", "Lightroom subscription"],
            "gaming": ["Gaming headset", "Game gift card", "RGB lights"],
            "fashion": ["Accessories", "Gift card to their fav brand", "Sunglasses"],
            "books": ["Book subscription box", "Kindle credits", "Bookmarks set"],
            "tech": ["Gadget accessories", "Tech subscription", "Desk organizer"],
            "art": ["Art supplies", "Museum membership", "Custom portrait"],
            "pets": ["Pet treats", "Pet accessories", "Pet photo shoot"],
            "coffee": ["Coffee subscription", "Fancy mug", "Coffee maker"],
        }

        for interest in interests:
            gift_suggestions.extend(gift_mapping.get(interest, []))

        # Default suggestions if nothing detected
        if not gift_suggestions:
            gift_suggestions = ["Gift card", "Experience voucher", "Surprise box"]

        return {
            "success": True,
            "username": username,
            "detected_interests": interests[:5],
            "gift_suggestions": list(set(gift_suggestions))[:10],
            "vibe_tags": ["classic"], # Default
            "ai_summary": "Analysis based on keywords.",
            "profile_summary": {
                "followers": profile.get("follower_count"),
                "posts": profile.get("post_count"),
                "bio": profile.get("bio"),
                "full_name": profile.get("full_name"),
                "profile_pic_url": profile.get("profile_pic_url")
            }
        }
