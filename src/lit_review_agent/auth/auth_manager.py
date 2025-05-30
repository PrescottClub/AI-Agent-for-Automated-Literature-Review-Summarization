"""Authentication manager for API security."""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Union
from abc import ABC, abstractmethod

from pydantic import BaseModel
from ..utils.logger import get_logger
from ..exceptions import AuthenticationError, AuthorizationError

logger = get_logger(__name__)


class User(BaseModel):
    """User model for authentication."""
    user_id: str
    username: str
    email: Optional[str] = None
    api_keys: List[str] = []
    roles: List[str] = ["user"]
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None


class APIKey(BaseModel):
    """API key model."""
    key_id: str
    user_id: str
    key_hash: str
    name: str
    permissions: List[str] = []
    is_active: bool = True
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None


class AuthProvider(ABC):
    """Abstract base class for authentication providers."""

    @abstractmethod
    async def authenticate(self, credentials: Dict) -> Optional[User]:
        """Authenticate user with credentials."""
        pass

    @abstractmethod
    async def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Validate API key."""
        pass


class APIKeyAuth(AuthProvider):
    """API key authentication provider."""

    def __init__(self):
        self.api_keys: Dict[str, APIKey] = {}
        self.users: Dict[str, User] = {}
        self._initialize_default_users()

    def _initialize_default_users(self):
        """Initialize default users and API keys."""
        # Create admin user
        admin_user = User(
            user_id="admin",
            username="admin",
            email="admin@localhost",
            roles=["admin", "user"],
            created_at=datetime.utcnow()
        )
        self.users["admin"] = admin_user

        # Create default API key for admin
        admin_key = self.generate_api_key(
            user_id="admin",
            name="default_admin_key",
            permissions=["read", "write", "admin"]
        )
        logger.info(f"Default admin API key created: {admin_key[:8]}...")

    def generate_api_key(
        self, 
        user_id: str, 
        name: str, 
        permissions: List[str] = None,
        expires_in_days: Optional[int] = None
    ) -> str:
        """Generate a new API key."""
        if user_id not in self.users:
            raise AuthenticationError(f"User {user_id} not found")

        # Generate secure random key
        raw_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)

        api_key = APIKey(
            key_id=secrets.token_hex(16),
            user_id=user_id,
            key_hash=key_hash,
            name=name,
            permissions=permissions or ["read"],
            created_at=datetime.utcnow(),
            expires_at=expires_at
        )

        self.api_keys[raw_key] = api_key
        self.users[user_id].api_keys.append(raw_key)

        logger.info(f"API key '{name}' generated for user {user_id}")
        return raw_key

    async def authenticate(self, credentials: Dict) -> Optional[User]:
        """Authenticate user with username/password."""
        username = credentials.get("username")
        password = credentials.get("password")

        if not username or not password:
            return None

        # Simple password check (in production, use proper hashing)
        if username == "admin" and password == "admin":
            user = self.users.get("admin")
            if user:
                user.last_login = datetime.utcnow()
                return user

        return None

    async def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Validate API key."""
        try:
            key_obj = self.api_keys.get(api_key)
            if not key_obj:
                return None

            # Check if key is active
            if not key_obj.is_active:
                return None

            # Check if user exists and is active
            user = self.users.get(key_obj.user_id)
            if not user or not user.is_active:
                return None

            # Check expiration
            if key_obj.expires_at and datetime.utcnow() > key_obj.expires_at:
                key_obj.is_active = False
                return None

            # Update last used
            key_obj.last_used = datetime.utcnow()
            
            logger.debug(f"API key validated for user {key_obj.user_id}")
            return key_obj

        except Exception as e:
            logger.error(f"Error validating API key: {e}")
            return None

    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key."""
        key_obj = self.api_keys.get(api_key)
        if key_obj:
            key_obj.is_active = False
            logger.info(f"API key '{key_obj.name}' revoked for user {key_obj.user_id}")
            return True
        return False

    def get_user_api_keys(self, user_id: str) -> List[APIKey]:
        """Get all API keys for a user."""
        user = self.users.get(user_id)
        if not user:
            return []

        return [
            self.api_keys[key] for key in user.api_keys 
            if key in self.api_keys
        ]


class TokenAuth(AuthProvider):
    """JWT token authentication provider."""

    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.tokens: Dict[str, Dict] = {}  # Simple in-memory store

    def generate_token(self, user_id: str, expires_in_hours: int = 24) -> str:
        """Generate a JWT-like token."""
        # Simplified token generation (use proper JWT in production)
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
        
        self.tokens[token] = {
            "user_id": user_id,
            "expires_at": expires_at,
            "created_at": datetime.utcnow()
        }

        logger.info(f"Token generated for user {user_id}")
        return token

    async def authenticate(self, credentials: Dict) -> Optional[User]:
        """Authenticate with token."""
        token = credentials.get("token")
        if not token:
            return None

        token_data = self.tokens.get(token)
        if not token_data:
            return None

        # Check expiration
        if datetime.utcnow() > token_data["expires_at"]:
            del self.tokens[token]
            return None

        # Return a basic user object (would fetch from DB in production)
        return User(
            user_id=token_data["user_id"],
            username=token_data["user_id"],
            created_at=token_data["created_at"]
        )

    async def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Not implemented for token auth."""
        return None

    def revoke_token(self, token: str) -> bool:
        """Revoke a token."""
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False


class AuthManager:
    """Main authentication manager."""

    def __init__(self, providers: List[AuthProvider] = None):
        self.providers = providers or [APIKeyAuth()]
        self.sessions: Dict[str, Dict] = {}

    async def authenticate(self, credentials: Dict) -> Optional[User]:
        """Authenticate user using available providers."""
        for provider in self.providers:
            try:
                user = await provider.authenticate(credentials)
                if user:
                    logger.info(f"User {user.username} authenticated successfully")
                    return user
            except Exception as e:
                logger.error(f"Authentication error with provider {provider.__class__.__name__}: {e}")
                continue

        logger.warning("Authentication failed for all providers")
        return None

    async def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Validate API key using available providers."""
        for provider in self.providers:
            try:
                key_obj = await provider.validate_api_key(api_key)
                if key_obj:
                    return key_obj
            except Exception as e:
                logger.error(f"API key validation error with provider {provider.__class__.__name__}: {e}")
                continue

        return None

    def create_session(self, user: User) -> str:
        """Create a user session."""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "user": user,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }

        logger.info(f"Session created for user {user.username}")
        return session_id

    def get_session_user(self, session_id: str) -> Optional[User]:
        """Get user from session."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        # Check session expiration (1 hour)
        if datetime.utcnow() - session["last_activity"] > timedelta(hours=1):
            del self.sessions[session_id]
            return None

        # Update last activity
        session["last_activity"] = datetime.utcnow()
        return session["user"]

    def revoke_session(self, session_id: str) -> bool:
        """Revoke a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info("Session revoked")
            return True
        return False

    def has_permission(self, user: User, permission: str) -> bool:
        """Check if user has a specific permission."""
        # Admin role has all permissions
        if "admin" in user.roles:
            return True

        # Check role-based permissions
        role_permissions = {
            "user": ["read"],
            "researcher": ["read", "search"],
            "admin": ["read", "write", "admin", "search"]
        }

        for role in user.roles:
            if permission in role_permissions.get(role, []):
                return True

        return False

    def get_stats(self) -> Dict:
        """Get authentication statistics."""
        total_users = len({provider.users for provider in self.providers if hasattr(provider, 'users')})
        active_sessions = len(self.sessions)
        
        api_key_stats = {}
        for provider in self.providers:
            if hasattr(provider, 'api_keys'):
                active_keys = sum(1 for key in provider.api_keys.values() if key.is_active)
                api_key_stats[provider.__class__.__name__] = active_keys

        return {
            "total_users": total_users,
            "active_sessions": active_sessions,
            "api_key_providers": api_key_stats,
            "session_cleanup_threshold": "1 hour"
        }


# Global auth manager instance
auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get the global auth manager instance."""
    global auth_manager
    if auth_manager is None:
        auth_manager = AuthManager()
    return auth_manager


def initialize_auth(providers: List[AuthProvider] = None) -> AuthManager:
    """Initialize the global auth manager."""
    global auth_manager
    auth_manager = AuthManager(providers)
    return auth_manager 