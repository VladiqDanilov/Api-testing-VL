import os
from httpx import Client, Response
from typing import Optional, Any

from utilities.logger_utils import logger


class ApiClient(Client):
    """Extension of the standard httpx client with enhanced logging."""
    
    def __init__(self):
        base_url = self._get_validated_base_url()
        super().__init__(base_url=base_url)
        self.logging_enabled = self._parse_logging_setting()

    def _get_validated_base_url(self) -> str:
        """Validate and construct base URL from environment variable."""
        resource_url = os.getenv('RESOURCE_URL')
        if not resource_url:
            raise ValueError("RESOURCE_URL environment variable is not set")
        return f"https://{resource_url}"

    def _parse_logging_setting(self) -> bool:
        """Safely parse logging setting from environment."""
        log_setting = os.getenv("USE_LOGS", "").lower().strip()
        return log_setting in ("true", "1", "t", "yes")

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """Extended httpx request method with conditional logging.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: URL path for the request
            **kwargs: Additional arguments for the request
            
        Returns:
            Response: The response from the server
        """
        if self.logging_enabled:
            try:
                logger.info(f'{method} {url}')
                if kwargs.get('params'):
                    logger.debug(f'Params: {kwargs["params"]}')
                if kwargs.get('json'):
                    logger.debug(f'Request body: {kwargs["json"]}')
            except Exception as e:
                logger.error(f"Logging failed: {str(e)}")

        return super().request(method, url, **kwargs)