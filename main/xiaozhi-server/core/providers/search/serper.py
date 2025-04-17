import aiohttp
from typing import List, Dict, Any, Optional

from config.logger import setup_logging
from core.providers.search.base import SearchProviderBase

TAG = __name__
logger = setup_logging()


class SerperProvider(SearchProviderBase):
    """Serper搜索提供者"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.api_url = "https://google.serper.dev/search"
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """执行Web搜索"""
        try:
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "q": query,
                "num": max_results
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload, headers=headers) as response:
                    if response.status != 200:
                        logger.bind(tag=TAG).error(f"Serper搜索失败: {response.status}")
                        return []
                    
                    data = await response.json()
                    organic_results = data.get("organic", [])
                    
                    # 格式化结果为统一格式
                    formatted_results = []
                    for result in organic_results[:max_results]:
                        formatted_results.append({
                            "title": result.get("title", ""),
                            "href": result.get("link", ""),
                            "body": result.get("snippet", ""),
                            # "date": result.get("date", ""),
                            # "position": result.get("position", ""),
                            # "source": "Serper"
                        })
                    
                    return formatted_results
        except Exception as e:
            logger.bind(tag=TAG).error(f"Serper搜索异常: {e}")
            return []
    
    # async def search_images(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    #     """执行图片搜索"""
    #     try:
    #         headers = {
    #             "X-API-KEY": self.api_key,
    #             "Content-Type": "application/json"
    #         }
    #         payload = {
    #             "q": query,
    #             "searchType": "images",
    #             "num": max_results
    #         }
            
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(self.api_url, json=payload, headers=headers) as response:
    #                 if response.status != 200:
    #                     logger.bind(tag=TAG).error(f"Serper图片搜索失败: {response.status}")
    #                     return []
                    
    #                 data = await response.json()
    #                 image_results = data.get("images", [])
                    
    #                 # 格式化结果为统一格式
    #                 formatted_results = []
    #                 for result in image_results[:max_results]:
    #                     formatted_results.append({
    #                         "title": result.get("title", ""),
    #                         "thumbnail": result.get("thumbnailUrl", ""),
    #                         "image": result.get("imageUrl", ""),
    #                         "source": "Serper"
    #                     })
                    
    #                 return formatted_results
    #     except Exception as e:
    #         logger.bind(tag=TAG).error(f"Serper图片搜索异常: {e}")
    #         return []
    
    # async def search_news(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    #     """执行新闻搜索"""
    #     try:
    #         headers = {
    #             "X-API-KEY": self.api_key,
    #             "Content-Type": "application/json"
    #         }
    #         payload = {
    #             "q": query,
    #             "searchType": "news",
    #             "num": max_results
    #         }
            
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(self.api_url, json=payload, headers=headers) as response:
    #                 if response.status != 200:
    #                     logger.bind(tag=TAG).error(f"Serper新闻搜索失败: {response.status}")
    #                     return []
                    
    #                 data = await response.json()
    #                 news_results = data.get("news", [])
                    
    #                 # 格式化结果为统一格式
    #                 formatted_results = []
    #                 for result in news_results[:max_results]:
    #                     formatted_results.append({
    #                         "title": result.get("title", ""),
    #                         "link": result.get("link", ""),
    #                         "snippet": result.get("snippet", ""),
    #                         "date": result.get("date", ""),
    #                         "source": result.get("source", "Serper")
    #                     })
                    
    #                 return formatted_results
    #     except Exception as e:
    #         logger.bind(tag=TAG).error(f"Serper新闻搜索异常: {e}")
    #         return []
