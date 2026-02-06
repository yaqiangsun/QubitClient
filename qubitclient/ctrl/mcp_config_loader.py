# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/06 13:45:24
########################################################################

"""
.mcp.json configuration file loader
Supports auto discovery, multi-format parsing, and environment overrides
"""
import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerType(Enum):
    """Supported server type enumeration"""
    HTTP = "http"
    STREAMABLE_HTTP = "streamable_http"
    STDIO = "stdio"
    UNKNOWN = "unknown"

@dataclass
class MCPConfig:
    """MCP server configuration data class"""
    name: str
    server_type: ServerType
    url: Optional[str] = None
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    
    def to_langchain_format(self) -> Dict[str, Any]:
        """Convert to format usable by LangChain MCP Adapters"""
        if self.server_type in [ServerType.HTTP, ServerType.STREAMABLE_HTTP]:
            config = {
                "transport": self.server_type.value,
                "url": self.url
            }
            if self.headers:
                config["headers"] = self.headers
            return config
        
        elif self.server_type == ServerType.STDIO:
            return {
                "transport": "stdio",
                "command": self.command,
                "args": self.args,
                "env": self.env
            }
        
        raise ValueError(f"Unsupported server type: {self.server_type}")

class MCPConfigLoader:
    """Elegant MCP configuration loader"""
    
    # Standard configuration file paths (by priority)
    STANDARD_PATHS = [
        Path.home() / ".config" / "mcp.json",  # Standard location
        Path.cwd() / ".mcp.json",              # Project root directory
        Path.cwd() / "config" / "mcp.json",    # Project config directory
    ]
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration loader
        
        Args:
            config_path: Optional specified configuration file path, auto-discovery if None
        """
        self.config_path = config_path
        self._config_cache: Dict[str, MCPConfig] = {}
    
    def discover_config_file(self) -> Optional[Path]:
        """Automatically discover configuration file"""
        # 1. Use specified path if provided
        if self.config_path and self.config_path.exists():
            logger.info(f"Using specified configuration file: {self.config_path}")
            return self.config_path
        
        # 2. Check path specified by environment variable
        env_path = os.getenv("MCP_CONFIG_PATH")
        if env_path:
            env_path_obj = Path(env_path).expanduser()
            if env_path_obj.exists():
                logger.info(f"Using configuration file specified by environment variable: {env_path_obj}")
                return env_path_obj
        
        # 3. Search standard paths
        for path in self.STANDARD_PATHS:
            expanded_path = path.expanduser()
            if expanded_path.exists():
                logger.info(f"Found configuration file: {expanded_path}")
                return expanded_path
        
        logger.warning("No configuration files found")
        return None
    
    def _parse_server_config(self, name: str, config: Dict[str, Any]) -> MCPConfig:
        """Parse individual server configuration"""
        # Check if it's HTTP bridge mode (common Claude Desktop format)
        if config.get("command") == "npx":
            args = config.get("args", [])
            for arg in args:
                if isinstance(arg, str) and arg.startswith("http"):
                    # This is an HTTP server proxied via npx
                    return MCPConfig(
                        name=name,
                        server_type=ServerType.HTTP,
                        url=arg,
                        headers=config.get("headers", {})
                    )
        
        # Check if transport is directly specified (common programming framework format)
        if "transport" in config:
            transport = config["transport"]
            if transport in ["http", "streamable_http"]:
                return MCPConfig(
                    name=name,
                    server_type=ServerType(transport),
                    url=config.get("url"),
                    headers=config.get("headers", {})
                )
            elif transport == "stdio":
                return MCPConfig(
                    name=name,
                    server_type=ServerType.STDIO,
                    command=config.get("command"),
                    args=config.get("args", []),
                    env=config.get("env", {})
                )
        
        # Try to automatically infer type
        if "url" in config and isinstance(config["url"], str):
            if config["url"].startswith("http"):
                return MCPConfig(
                    name=name,
                    server_type=ServerType.HTTP,
                    url=config["url"],
                    headers=config.get("headers", {})
                )
        
        logger.warning(f"Unable to determine server type for '{name}', using default HTTP type")
        return MCPConfig(
            name=name,
            server_type=ServerType.HTTP,
            url=config.get("url", ""),
            headers=config.get("headers", {})
        )
    
    def load(self) -> Dict[str, MCPConfig]:
        """Load and parse all server configurations"""
        config_file = self.discover_config_file()
        if not config_file:
            return {}
        
        try:
            with open(config_file, 'r') as f:
                raw_config = json.load(f)
            
            servers_config = raw_config.get("mcpServers", {})
            
            # Parse each server configuration
            for name, server_config in servers_config.items():
                self._config_cache[name] = self._parse_server_config(name, server_config)
                logger.debug(f"Parsed server configuration: {name}")
            
            logger.info(f"Successfully loaded {len(self._config_cache)} server configurations")
            return self._config_cache
            
        except json.JSONDecodeError as e:
            logger.error(f"Configuration file JSON format error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration file: {e}")
            raise
    
    def get_server(self, name: str) -> Optional[MCPConfig]:
        """Get server configuration by name"""
        if not self._config_cache:
            self.load()
        return self._config_cache.get(name)
    
    def get_all_for_langchain(self) -> Dict[str, Dict[str, Any]]:
        """Get all configurations converted to LangChain format"""
        if not self._config_cache:
            self.load()
        
        return {
            name: config.to_langchain_format()
            for name, config in self._config_cache.items()
        }
    
    def validate_configs(self) -> List[str]:
        """Validate all configurations, return list of error messages"""
        errors = []
        
        for name, config in self._config_cache.items():
            if config.server_type in [ServerType.HTTP, ServerType.STREAMABLE_HTTP]:
                if not config.url:
                    errors.append(f"Server '{name}' missing URL")
                elif not config.url.startswith("http"):
                    errors.append(f"Server '{name}' has invalid URL format: {config.url}")
            
            elif config.server_type == ServerType.STDIO:
                if not config.command:
                    errors.append(f"Server '{name}' missing command")
        
        return errors

# Example usage
def example_usage():
    """Example usage"""
    # 1. Basic usage: Auto discovery and loading
    loader = MCPConfigLoader()
    configs = loader.load()
    
    # 2. Validate configurations
    errors = loader.validate_configs()
    if errors:
        logger.warning(f"Configuration validation found {len(errors)} issues:")
        for error in errors:
            logger.warning(f"  - {error}")
    
    # 3. Get specific server
    quantum_config = loader.get_server("quantum-service")
    if quantum_config:
        print(f"MCP service URL: {quantum_config.url}")
    
    # 4. Convert to LangChain compatible format
    langchain_configs = loader.get_all_for_langchain()
    
    # 5. Use in LangChain
    from langchain_mcp_adapters.client import MultiServerMCPClient
    
    client = MultiServerMCPClient(langchain_configs)
    # ... subsequent client usage
    
    return configs

# Environment-specific configuration file support
def load_environment_specific_config(env: str = None) -> Dict[str, MCPConfig]:
    """
    Load environment-specific configuration
    
    Args:
        env: Environment name, such as 'dev', 'prod'. Automatically retrieved from environment 
             variable if None
    """
    if env is None:
        env = os.getenv("MCP_ENV", "dev")
    
    # Try to load environment-specific config, such as .mcp.prod.json
    env_config_path = Path.cwd() / f".mcp.{env}.json"
    loader = MCPConfigLoader(env_config_path)
    
    # If environment-specific config doesn't exist, fallback to default config
    if not env_config_path.exists():
        logger.info(f"Environment-specific config does not exist, using default config")
        loader = MCPConfigLoader()
    
    return loader.load()

if __name__ == "__main__":
    # Run example
    configs = example_usage()
    print(f"\nLoaded {len(configs)} server configurations")