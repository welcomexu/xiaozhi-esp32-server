import json
from typing import Dict, Any, Optional
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action

# Use absolute imports based on the project root
from core.providers.search.duckduckgo import DuckDuckGoProvider
from core.providers.search.serper import SerperProvider

TAG = __name__
logger = setup_logging()

# Function definition that follows the required schema format for function_call
WEB_SEARCH_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the internet for information on a given query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on the internet"
                },
                "search_engine": {
                    "type": "string",
                    "description": "Specify which search engine to use. If not provided, the system default will be used.",
                    "enum": ["duckduckgo", "serper"],
                    "default": "duckduckgo"               
                }
            },
            "required": ["query"]
        }
    }
}

# Register the web_search function
@register_function("web_search", WEB_SEARCH_FUNCTION_DESC, ToolType.SYSTEM_CTL)
def web_search(conn, query: str = None, lang: str = "zh_CN"):
    try:
        search_engine = conn.config["plugins"]["web_search"]["engine"]
        if search_engine is None:
            search_engine = "duckduckgo"
        # 分别调用对应的搜索引擎的search方法执行搜索
        search_provider = None
        if search_engine == "duckduckgo":
            search_config = conn.config["plugins"]["web_search"]["duckduckgo"]
            search_provider = DuckDuckGoProvider(search_config)
                
        elif search_engine == "serper":
            search_config = conn.config["plugins"]["web_search"]["serper"]
            search_provider = SerperProvider(search_config)
        
        if not search_provider:
            return {
                "result": f"Error: Search provider '{search_engine}' not available",
                "success": False
            }
        
        # Perform search
        search_results = search_provider.search(query)
        
        # Format results for better presentation
        formatted_results = format_search_results(search_results, search_engine)

        # 构建搜索报告
        search_report = (
            f"根据以下查询结果，用{lang}回应用户的问题：\n\n"
            f"查询结果：\n{formatted_results}\n"
            f"(综合查询结果，提取出最相关的信息，回答用户的问题"
            f"如果查询结果中没有相关信息，告知用户没有找到相关结果。)"
        )

        return ActionResponse(Action.REQLLM, search_report, None)

    except Exception as e:
        logger.bind(tag=TAG).error(f"联网搜索出错: {e}")
        return ActionResponse(Action.REQLLM, "抱歉，联网搜索时发生错误，请稍后再试。", None)

def format_search_results(results: list, search_engine: str) -> str:
    """
    返回results中的body内容，用回车符拼接成字符串
    """
    if not results:
        return "没有找到相关结果。"

    formatted_results = []
    for result in results:
        title = result.get("title", "未知标题")
        href = result.get("href", "未知链接")
        body = result.get("body", "无内容")
        
        formatted_results.append(f"标题: {title}\n内容: {body}\n\n")

    return "\n".join(formatted_results)
