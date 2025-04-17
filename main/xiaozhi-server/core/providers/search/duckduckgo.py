import aiohttp
from typing import List, Dict, Any, Optional

from config.logger import setup_logging
from core.providers.search.base import SearchProviderBase
from duckduckgo_search import DDGS
from itertools import islice

TAG = __name__
logger = setup_logging()


class DuckDuckGoProvider(SearchProviderBase):
    """DuckDuckGo搜索提供者"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_url = config.get("api_url", "https://api.duckduckgo.com")
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        results = []
        with DDGS() as ddgs:
            # 使用DuckDuckGo搜索关键词
            ddgs_gen = ddgs.text(query, safesearch='Off', timelimit='y', backend="lite")
            # 从搜索结果中获取最大结果数
            for r in islice(ddgs_gen, max_results):
                results.append(r)

        # 返回一个json响应，包含搜索结果
        # return {'results': results}
        return results # 返回list[dict], 每个dict包含{"title", "href", "body"}

