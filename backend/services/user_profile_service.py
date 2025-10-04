from abc import ABC, abstractmethod
from typing import List

from constants.search_models import UserProfile


class UserProfileService(ABC):
    @abstractmethod
    async def get_user_profiles(self, query: str) -> List[UserProfile]:
        pass