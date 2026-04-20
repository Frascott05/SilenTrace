import Dexie from "dexie";

const db = new Dexie("VolPluginsDB");

db.version(1).stores({
  plugins: "os" // key = os (windows/linux/mac)
});

export default db;