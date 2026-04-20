import db from "../pluginsDB";
import { getPluginsList } from "../services/api";

class VolPluginsService {
  async init() {
    const existing = await db.plugins.toArray();

    // if DB is empty → fetch API and inizialization
    if (!existing.length) {
      return await this.loadFromApi();
    }

    return this.getAll();
  }

  async loadFromApi() {
    const osList = ["windows", "linux", "mac"];
    const result = {};

    for (const os of osList) {
      const res = await getPluginsList({ os });
      const plugins = res.data || [];

      result[os] = plugins.map((p) => ({
        name: p.name,
        description: p.description,
        enabled: true
      }));

      await db.plugins.put({
        os,
        plugins: result[os]
      });
    }

    return result;
  }

  async getAll() {
    const rows = await db.plugins.toArray();

    return rows.reduce((acc, row) => {
      acc[row.os] = row.plugins;
      return acc;
    }, {});
  }

  async getPlugins(os) {
    const row = await db.plugins.get(os);
    return row?.plugins || [];
  }

  async toggle(os, pluginName) {
    const row = await db.plugins.get(os);
    if (!row) return;

    row.plugins = row.plugins.map((p) =>
      p.name === pluginName
        ? { ...p, enabled: !p.enabled }
        : p
    );

    await db.plugins.put(row);
  }

  async setAll(os, value) {
    const row = await db.plugins.get(os);
    if (!row) return;

    row.plugins = row.plugins.map((p) => ({
      ...p,
      enabled: value
    }));

    await db.plugins.put(row);
  }
}

export default new VolPluginsService();