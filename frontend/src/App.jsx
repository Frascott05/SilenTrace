import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import RunPage from "./pages/RunPage";
import IocPage from "./pages/IocPage";
import PluginsPage from "./pages/PluginsPage";
import TimelinePage from "./pages/TimelinePage";

export default function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<RunPage />} />
          <Route path="/timeline" element={<TimelinePage />} />
          <Route path="/ioc" element={<IocPage />} />
          <Route path="/plugins" element={<PluginsPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}


