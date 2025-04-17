from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class SearchProviderBase(ABC):
    """基础搜索提供者抽象类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化搜索提供者
        
        Args:
            config: 配置参数
        """
        self.config = config
        
    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        执行搜索查询
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            搜索结果列表
        """
        pass
    
    @abstractmethod
    async def search_images(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        执行图片搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            图片搜索结果列表
        """
        pass
    
    @abstractmethod
    async def search_news(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        执行新闻搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            新闻搜索结果列表
        """
        pass
