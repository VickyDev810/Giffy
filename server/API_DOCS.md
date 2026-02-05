# Giffy API Documentation

Base URL: `http://localhost:8000/api`

---

## Authentication

### POST `/auth/signup`
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "cooluser",
  "password": "securepass123",
  "full_name": "Cool User",
  "phone": "+919876543210"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "cooluser",
  "full_name": "Cool User",
  "phone": "+919876543210",
  "avatar_url": null,
  "bio": null,
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### POST `/auth/login`
Login and get JWT access token.

**Request:** Form data (OAuth2)
- `username`: email address
- `password`: user password

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Usage:** Add header to all protected routes:
```
Authorization: Bearer <access_token>
```

---

## Users

### GET `/users/me`
Get current logged-in user's profile.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "cooluser",
  "full_name": "Cool User",
  "phone": "+919876543210",
  "avatar_url": "https://...",
  "bio": "Living my best life",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### PUT `/users/me`
Update current user's profile.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "full_name": "Updated Name",
  "phone": "+919999999999",
  "avatar_url": "https://example.com/avatar.jpg",
  "bio": "New bio here"
}
```

**Response:** `200 OK` - Updated user object

---

### GET `/users/search?q={query}`
Search users by username or email.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `q` (required): Search query string

**Response:** `200 OK`
```json
[
  {
    "id": 2,
    "username": "friend123",
    "full_name": "Friend Name",
    "avatar_url": "https://..."
  }
]
```

---

### GET `/users/{user_id}`
Get a specific user's public profile.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK` - User object

---

## Friends

### POST `/friends/request`
Send a friend request to another user.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "receiver_id": 2,
  "message": "Hey! Let's be friends on Giftify!"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "sender_id": 1,
  "receiver_id": 2,
  "status": "pending",
  "message": "Hey! Let's be friends on Giftify!",
  "created_at": "2024-01-15T10:30:00Z",
  "sender_username": "cooluser",
  "receiver_username": "friend123"
}
```

**Note:** If receiver already sent you a request, friendship is auto-created (mutual add).

---

### GET `/friends/requests/incoming`
Get all pending friend requests received.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "sender_id": 3,
    "receiver_id": 1,
    "status": "pending",
    "message": "Add me!",
    "sender_username": "newguy",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### GET `/friends/requests/outgoing`
Get all pending friend requests sent.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK` - Array of friend request objects

---

### POST `/friends/requests/{request_id}/respond`
Accept or reject a friend request.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "action": "accept"  // or "reject"
}
```

**Response:** `200 OK` - Updated friend request object

**Note:** On accept, mutual friendship is created for both users.

---

### GET `/friends/`
Get all your friends.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "friend_id": 2,
    "nickname": "Bestie",
    "created_at": "2024-01-15T10:30:00Z",
    "friend_username": "friend123",
    "friend_full_name": "Friend Name",
    "friend_avatar_url": "https://..."
  }
]
```

---

### PUT `/friends/{friend_id}/nickname`
Set a nickname for a friend.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "nickname": "Bestie"
}
```

**Response:** `200 OK` - Updated friendship object

---

### DELETE `/friends/{friend_id}`
Remove a friend (unfriend).

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

---

## Persona

### GET `/persona/me`
Get your persona (preferences, vibe tags, interests).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "budget_preference": "medium",
  "gift_style": "chaotic",
  "vibe_tags": ["memer", "foodie", "techie"],
  "interests": ["gaming", "anime", "coffee"],
  "dislikes": ["spicy food", "loud colors"],
  "shirt_size": "L",
  "shoe_size": "10",
  "default_address": "123 Main St, Bangalore",
  "city": "Bangalore",
  "pincode": "560001",
  "ai_summary": "Tech-savvy memer who loves gaming and coffee",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T12:00:00Z"
}
```

---

### PUT `/persona/me`
Update your persona.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "budget_preference": "high",
  "gift_style": "thoughtful",
  "vibe_tags": ["creative", "bookworm"],
  "interests": ["photography", "travel", "music"],
  "dislikes": ["cheap plastic stuff"],
  "shirt_size": "M",
  "shoe_size": "9",
  "default_address": "456 New Address, Mumbai",
  "city": "Mumbai",
  "pincode": "400001"
}
```

**Budget Preferences:** `low`, `medium`, `high`, `yolo`

**Gift Styles:** `funny`, `thoughtful`, `chaotic`, `practical`

**Response:** `200 OK` - Updated persona object

---

### GET `/persona/friend/{friend_id}`
Get a friend's persona (for gift selection).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK` - Friend's persona object

**Note:** Only works for actual friends (mutual friendship required).

---

### GET `/persona/vibe-tags?category={category}`
Get all available vibe tags.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `category` (optional): Filter by category (humor, lifestyle, interests)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "memer",
    "category": "humor",
    "description": "Lives for memes and internet culture"
  },
  {
    "id": 2,
    "name": "foodie",
    "category": "lifestyle",
    "description": "Food is life"
  }
]
```

---

### POST `/persona/me/vibe-tags/{tag_name}`
Add a vibe tag to your persona.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Added 'techie' to your vibe tags"
}
```

---

### DELETE `/persona/me/vibe-tags/{tag_name}`
Remove a vibe tag from your persona.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Removed 'techie' from your vibe tags"
}
```

---

## Gifts

### POST `/gifts/`
Send a gift to a friend.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "recipient_id": 2,
  "vibe_prompt": "send something chaotic and funny",
  "budget_min": 200,
  "budget_max": 1000,
  "is_surprise": false,
  "sender_message": "Happy birthday! Hope this makes you laugh 😂",
  "delivery_address": "Optional override address"
}
```

**Fields:**
- `recipient_id`: Friend's user ID
- `vibe_prompt`: Natural language description of desired gift vibe
- `budget_min/max`: Budget range in INR
- `is_surprise`: If `true`, skips approval (YOLO mode)
- `sender_message`: Optional message to recipient
- `delivery_address`: Optional (uses friend's default if not provided)

**Response:** `201 Created`
```json
{
  "id": 1,
  "sender_id": 1,
  "recipient_id": 2,
  "vibe_prompt": "send something chaotic and funny",
  "budget_min": 200,
  "budget_max": 1000,
  "gift_name": null,
  "gift_description": null,
  "gift_image_url": null,
  "gift_price": null,
  "agent_reasoning": null,
  "platform": null,
  "order_id": null,
  "tracking_url": null,
  "delivery_address": "123 Main St, Bangalore",
  "status": "agent_picking",
  "is_surprise": false,
  "sender_message": "Happy birthday!",
  "recipient_reaction": null,
  "created_at": "2024-01-15T10:30:00Z",
  "sender_username": "cooluser",
  "recipient_username": "friend123"
}
```

**Gift Status Flow:**
1. `pending` - Gift created
2. `agent_picking` - AI agent selecting gift
3. `awaiting_approval` - Waiting for sender to approve (if not surprise)
4. `ordered` - Order placed
5. `shipped` - Out for delivery
6. `delivered` - Delivered!
7. `cancelled` - Cancelled

---

### GET `/gifts/sent?status_filter={status}`
Get all gifts you've sent.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `status_filter` (optional): Filter by status

**Response:** `200 OK` - Array of gift objects

---

### GET `/gifts/received?status_filter={status}`
Get all gifts you've received.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK` - Array of gift objects

---

### GET `/gifts/{gift_id}`
Get details of a specific gift.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK` - Gift object

**Note:** Only sender or recipient can view.

---

### POST `/gifts/{gift_id}/approve`
Approve or reject the AI's gift selection (sender only).

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "approved": true  // or false to reject
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "status": "ordered",
  "gift_name": "Screaming Goat Toy",
  "gift_price": 299,
  "agent_reasoning": "Based on the chaotic vibe requested, I picked this because it's absolutely unhinged!",
  "ordered_at": "2024-01-15T11:00:00Z"
}
```

---

### POST `/gifts/{gift_id}/reaction`
Add recipient's reaction to a received gift.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "reaction": "OMG I love it! 😂🎉 Best gift ever!"
}
```

**Response:** `200 OK` - Updated gift object

---

### POST `/gifts/surprise/{friend_id}`
Quick surprise gift - YOLO mode (no approval needed).

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `budget_max` (required): Maximum budget
- `budget_min` (optional): Minimum budget (default: 0)
- `vibe_prompt` (optional): Gift vibe (default: "something chaotic and fun")

**Example:** `POST /gifts/surprise/2?budget_max=500&vibe_prompt=roast-worthy`

**Response:** `201 Created` - Gift object with `is_surprise: true`

**Note:** Gift is automatically picked and ordered without sender approval!

---

## Gift Subscriptions (Recurring Gifts)

### POST `/gifts/subscriptions`
Create automated recurring gift subscription.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "recipient_id": 2,
  "frequency": "weekly",
  "day_of_week": 5,
  "time_of_day": "10:00",
  "vibe_prompt": "something fun to start the weekend",
  "budget_min": 200,
  "budget_max": 500
}
```

**Fields:**
- `frequency`: `daily`, `weekly`, `monthly`
- `day_of_week`: 0-6 (Monday-Sunday) for weekly
- `day_of_month`: 1-31 for monthly
- `time_of_day`: HH:MM format (24hr)

**Response:** `201 Created`
```json
{
  "id": 1,
  "sender_id": 1,
  "recipient_id": 2,
  "frequency": "weekly",
  "day_of_week": 5,
  "day_of_month": null,
  "time_of_day": "10:00",
  "vibe_prompt": "something fun to start the weekend",
  "budget_min": 200,
  "budget_max": 500,
  "is_active": true,
  "last_sent_at": null,
  "next_send_at": "2024-01-19T10:00:00Z",
  "total_gifts_sent": 0,
  "recipient_username": "friend123"
}
```

---

### GET `/gifts/subscriptions`
Get all your gift subscriptions.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK` - Array of subscription objects

---

### PUT `/gifts/subscriptions/{subscription_id}`
Update a gift subscription.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "is_active": false,
  "budget_max": 800,
  "vibe_prompt": "something more thoughtful"
}
```

**Response:** `200 OK` - Updated subscription object

---

### DELETE `/gifts/subscriptions/{subscription_id}`
Cancel/delete a gift subscription.

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

---

## Social Connections

### GET `/social/connections`
Get all connected social accounts.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "platform": "instagram",
    "platform_username": "cooluser_insta",
    "follower_count": 1234,
    "following_count": 567,
    "post_count": 89,
    "bio": "Living life one post at a time",
    "last_synced_at": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-10T08:00:00Z"
  }
]
```

---

### POST `/social/instagram/connect`
Connect Instagram account by username.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "username": "cooluser_insta"
}
```

**Response:** `200 OK` - Social connection object

**Note:** Profile data is fetched in background using instaloader.

---

### POST `/social/instagram/sync`
Manually trigger Instagram profile sync.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Sync started"
}
```

---

### GET `/social/instagram/profile/{username}`
Fetch any public Instagram profile data.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "username": "someuser",
  "full_name": "Some User",
  "bio": "Bio text here",
  "follower_count": 5000,
  "following_count": 300,
  "post_count": 150,
  "is_private": false,
  "profile_pic_url": "https://...",
  "recent_posts": [
    {
      "shortcode": "ABC123",
      "caption": "Great day!",
      "likes": 234,
      "comments": 12,
      "date": "2024-01-14T15:00:00Z",
      "is_video": false,
      "url": "https://instagram.com/p/ABC123/"
    }
  ]
}
```

---

### DELETE `/social/instagram`
Disconnect Instagram account.

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

---

### POST `/social/instagram/analyze-for-gifts?username={username}`
Analyze Instagram profile to get gift suggestions.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `username` (required): Instagram username to analyze

**Response:** `200 OK`
```json
{
  "success": true,
  "username": "friend_insta",
  "detected_interests": ["travel", "photography", "coffee", "fitness"],
  "gift_suggestions": [
    "Travel journal",
    "Camera strap",
    "Coffee subscription",
    "Fitness tracker",
    "Photo printing credits"
  ],
  "profile_summary": {
    "followers": 2500,
    "posts": 180,
    "bio": "Wanderlust | Coffee addict | Capturing moments"
  }
}
```

---

## Health & Info

### GET `/`
Root endpoint - API info.

**Response:** `200 OK`
```json
{
  "message": "Welcome to Giftify API! 🎁",
  "docs": "/docs",
  "health": "/health"
}
```

---

### GET `/health`
Health check endpoint.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "giftify-api",
  "version": "1.0.0"
}
```

---

## Error Responses

All endpoints may return these errors:

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "You can only send gifts to your friends"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Rate Limits

Currently no rate limits implemented. Add in production!

---

## Interactive Docs

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
