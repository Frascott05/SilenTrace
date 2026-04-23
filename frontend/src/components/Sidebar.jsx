import { useState } from "react";
import { NavLink } from "react-router-dom";
import { Play, BarChart3, Brain, Plug, Menu, X } from "lucide-react";

const linkStyle = () => ({ isActive }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-start",
  gap: "12px",
  padding: "12px 16px",
  textDecoration: "none",
  color: isActive ? "white" : "#333",
  backgroundColor: isActive ? "#4f46e5" : "transparent",
  borderRadius: "8px",
  marginBottom: "8px",
});

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
      <div
        style={{
          width: collapsed ? "70px" : "220px",
          minWidth: collapsed ? "70px" : "220px",
          maxWidth: collapsed ? "70px" : "220px",
          height: "100vh",
          padding: "20px 10px",
          borderRight: "1px solid #ddd",
          display: "flex",
          flexDirection: "column",
          transition: "all 0.2s ease",
          flexShrink: 0,
          boxSizing: "border-box",

          position: "sticky",
          top: 0,
        }}
      >
      {/* HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: collapsed ? "center" : "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        {/* MENU TEXT (only when opened) */}
        {!collapsed && (
          <h2 style={{ margin: 0, fontSize: "18px" }}>
            Menu
          </h2>
        )}

        <button
          onClick={() => setCollapsed((prev) => !prev)}
          style={{
            border: "none",
            background: "#eee",
            borderRadius: "6px",
            padding: "6px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {collapsed ? <Menu size={18} /> : <X size={18} />}
        </button>
      </div>

      {/* LINKS */}
      <NavLink to="/" style={linkStyle()}>
        <Play size={20} />
        {!collapsed && "Run Plugins"}
      </NavLink>

      <NavLink to="/timeline" style={linkStyle()}>
        <BarChart3 size={20} />
        {!collapsed && "Timeline"}
      </NavLink>

      <NavLink to="/ioc" style={linkStyle()}>
        <Brain size={20} />
        {!collapsed && "AI Ioc"}
      </NavLink>

      <NavLink to="/plugins" style={linkStyle()}>
        <Plug size={20} />
        {!collapsed && "Plugins"}
      </NavLink>
    </div>
  );
}
