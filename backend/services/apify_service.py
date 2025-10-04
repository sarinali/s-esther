from typing import Dict, Any, Optional, List

from apify_client import ApifyClient
from config import config



class ApifyService:
    def __init__(self):

        self.client = ApifyClient(config.APIFY_API_TOKEN)

    def run_actor(
        self,
        actor_id: str,
        run_input: Dict[str, Any],
        timeout_secs: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        actor_client = self.client.actor(actor_id)
        run_result = actor_client.call(run_input=run_input, timeout_secs=timeout_secs)

        return run_result

    def get_dataset_items(
        self,
        dataset_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = 0
    ) -> List[Dict[str, Any]]:
        dataset_client = self.client.dataset(dataset_id)
        result = dataset_client.list_items(limit=limit, offset=offset)

        return result.items

    def run_actor_and_get_results(
        self,
        actor_id: str,
        run_input: Dict[str, Any],
        timeout_secs: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        run_result = self.run_actor(actor_id, run_input, timeout_secs)

        if not run_result:
            return []

        dataset_id = run_result.get("defaultDatasetId")
        if not dataset_id:
            return []

        return self.get_dataset_items(dataset_id, limit=limit)


service = ApifyService()
