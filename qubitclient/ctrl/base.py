# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/06 11:46:58
########################################################################

import logging
logger = logging.getLogger(__name__)
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from .mcp_config_loader import MCPConfigLoader

class AsyncMCPClient(MultiServerMCPClient):
    def __init__(self, mcpServers: list[str]|dict = None,*args, **kwargs):
        if mcpServers is None:
            loader = MCPConfigLoader()
            errors = loader.validate_configs()
            if errors:
                logger.error(f"Configuration validation found {len(errors)} issues:")
                for error in errors:
                    logger.error(f"  - {error}")
                raise Exception("Configuration validation found errors")
            langchain_configs = loader.get_all_for_langchain()
            mcpServers = langchain_configs
        elif type(mcpServers) == list:
            mcp_servers_dict = {}
            for index,mcpserver in enumerate(mcpServers):
                mcp_servers_dict[f"qubit_{index}"] = {
                        "transport": "streamable_http",
                        "url": mcpserver,
                    }
            mcpServers = mcp_servers_dict
        super().__init__(mcpServers, *args, **kwargs)
    async def call(self, method: str, *args, **kwargs):
        all_tools = await self.get_tools()
        target_tool = next((tool for tool in all_tools if tool.name == method), None)
        if target_tool is None:
            logging.warning(f"Tool named '{method}' not found.")
            return
        # Combine args and kwargs into a single input dictionary
        # For now, we'll pass kwargs as the input since args are typically empty in our use case
        input_data = kwargs if kwargs else {}
        if args:
            # If there are positional arguments, we need to handle them appropriately
            for arg in args:
                if type(arg) == dict:
                    input_data.update(arg)
                else:
                    logging.warning(f"Unexpected argument type: {type(arg)}")
        result = await target_tool.ainvoke(input_data)
        return result


class MCPClient(AsyncMCPClient):
    def __init__(self, mcpServers: list[str]|dict,*args, **kwargs):
        super().__init__(mcpServers, *args, **kwargs)
    def call(self, method: str, *args, **kwargs):
        return asyncio.run(super().call(method, *args, **kwargs))
    
# mcpServers = [
#     "http://127.0.0.1:8008/mcp"
# ]
# mcpServers = {
#     "quantum-service": {
#         "transport": "streamable_http",
#         "url": "http://127.0.0.1:8008/mcp",
#         # Optional
#         # "headers": {
#         #     "Authorization": "Bearer YOUR_TOKEN"
#         # }
#     }
#     # ADD MORE SERVERS HERE
# }