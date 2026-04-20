import json
import pkgutil
import importlib
import logging

import volatility3.framework as framework
from volatility3.framework import contexts
import volatility3.plugins


class VolatilityPluginList:
    """
    Complete explorer of the volatility3 plugins
    """

    def __init__(self, enable_logging: bool = True):
        self.ctx = contexts.Context()
        self._plugins_loaded = False

        if enable_logging:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("volatility_plugin_explorer")

    # -----------------------------
    # LOAD PLUGINS SAFELY
    # -----------------------------
    def _load_plugins(self):
        """
        Loads dinamically all the plugins modules.
        Doesn't stop if a loading failed.
        """

        if self._plugins_loaded:
            return

        self.logger.info("Loading Volatility 3 plugins...")

        for _, module_name, _ in pkgutil.walk_packages(
            volatility3.plugins.__path__,
            volatility3.plugins.__name__ + "."
        ):
            try:
                importlib.import_module(module_name)
            except Exception as e:
                # Log utile (prima era silenziato!)
                self.logger.debug(f"Failed to import {module_name}: {e}")

        self._plugins_loaded = True
        self.logger.info("Plugin loading completed")

    # -----------------------------
    # CORE PLUGIN LIST
    # -----------------------------
    def get_plugins(self):
        """
        Returns all the plugin in a structured form.
        """

        self._load_plugins()

        plugin_classes = framework.list_plugins()

        result = []

        for name, plugin in plugin_classes.items():
            result.append({
                "name": name,
                "module": getattr(plugin, "__module__", None),
                "description": (plugin.__doc__ or "").strip() if plugin.__doc__ else None,
                "class": plugin.__name__ if hasattr(plugin, "__name__") else str(plugin),
            })

        return result

    # -----------------------------
    # FILTER BY OS (ROBUST)
    # -----------------------------
    def get_plugins_by_os(self, os_name: str):
        """
        Filter all the plugins by os.
        Use of module path + Volatility namin based euristic.
        """

        self._load_plugins()

        os_name = os_name.lower()

        plugin_classes = framework.list_plugins()
        result = []

        for name, plugin in plugin_classes.items():

            module = (getattr(plugin, "__module__", "") or "").lower()

            # euristic
            is_match = (
                os_name in module
                or module.startswith(f"volatility3.plugins.{os_name}.")
                or f".{os_name}." in module
            )

            if is_match:
                result.append({
                    "name": name,
                    "module": module,
                    "description": (plugin.__doc__ or "").strip() if plugin.__doc__ else None,
                })

        return result

    # -----------------------------
    # SEARCH PLUGINS
    # -----------------------------
    def search_plugins(self, keyword: str):
        """
        Searchs plugin for keyword (name or description).
        Not used but it could become useful for a CLI version of the backend
        """

        self._load_plugins()

        keyword = keyword.lower()
        plugin_classes = framework.list_plugins()

        result = []

        for name, plugin in plugin_classes.items():
            desc = (plugin.__doc__ or "").lower()

            if keyword in name.lower() or keyword in desc:
                result.append({
                    "name": name,
                    "module": getattr(plugin, "__module__", None),
                    "description": (plugin.__doc__ or "").strip() if plugin.__doc__ else None,
                })

        return result

    # -----------------------------
    # RAW JSON OUTPUT
    # -----------------------------
    def get_plugins_json(self):
        """
        Complete Json output
        """

        return json.dumps(self.get_plugins(), indent=2)

    def get_plugins_by_os_json(self, os_name: str):
        """
        JSON output filtered by OS.
        """

        return json.dumps(self.get_plugins_by_os(os_name), indent=2)

    def search_plugins_json(self, keyword: str):
        """
        JSON outoput by search.
        """

        return json.dumps(self.search_plugins(keyword), indent=2)