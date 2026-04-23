import React, { useState, useEffect } from "react";
import {
  Grid,
  TextField,
  Button,
  Typography,
  Paper,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  OutlinedInput,
  Checkbox,
  ListItemText,
  Box
} from "@mui/material";

import { DataGrid } from "@mui/x-data-grid";

import { runPlugins, getStatus, getResults } from "../services/api";
import volPluginsService from "../services/volPluginsService";

export default function RunPage() {
  const [form, setForm] = useState({
    memory_file: "",
    plugins: [],
    os: "windows",
    address: null,
    dump: false,
    process: null
  });

  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);

  const [availablePlugins, setAvailablePlugins] = useState([]);

  const osOptions = ["windows", "linux", "mac"];

  const normalizePlugin = (fullName) => {
    const parts = fullName.split(".");
    if (parts.length < 3) return fullName;
    parts.shift();
    parts.pop();
    return parts.join(".");
  };

  useEffect(() => {
    loadPlugins(form.os);
  }, [form.os]);

  const loadPlugins = async (os) => {
    const data = await volPluginsService.getPlugins(os);

    const list = (data || [])
      .filter((p) => p.enabled)
      .map((p) => ({
        id: p.name,
        label: normalizePlugin(p.name)
      }));

    setAvailablePlugins(list);

    const first = list.length > 0 ? list[0].label : "";

    setForm((prev) => ({
      ...prev,
      plugins: first ? [first] : []
    }));
  };

  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      const res = await getStatus(jobId);
      setStatus(res.data.status);

      if (res.data.status === "done") {
        clearInterval(interval);
        const r = await getResults(jobId);
        setResults(r.data);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId]);

  const handleSubmit = async () => {
    const payload = {
      ...form,
      process: form.process ? parseInt(form.process) : null
    };

    const res = await runPlugins(payload);
    setJobId(res.data.job_id);
  };

  const buildGrid = (data) => {
    if (!data || data.length === 0)
      return { rows: [], columns: [] };

    const columns = Object.keys(data[0]).map((key) => ({
      field: key,
      headerName: key,
      flex: 1,
      minWidth: 150
    }));

    const rows = data.map((row, i) => ({
      id: i,
      ...row
    }));

    return { rows, columns };
  };

  // ✅ EXPORT JSON
  const exportToJson = (plugin, data) => {
    const blob = new Blob(
      [JSON.stringify(data, null, 2)],
      { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `${plugin}.json`;
    a.click();

    URL.revokeObjectURL(url);
  };

  // ✅ EXPORT CSV
  const exportToCsv = (plugin, data) => {
    if (!data || data.length === 0) return;

    const headers = Object.keys(data[0]);

    const csvRows = [
      headers.join(","), // header
      ...data.map((row) =>
        headers.map((field) => `"${row[field] ?? ""}"`).join(",")
      )
    ];

    const blob = new Blob([csvRows.join("\n")], {
      type: "text/csv"
    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `${plugin}.csv`;
    a.click();

    URL.revokeObjectURL(url);
  };

  return (
    <Grid container spacing={3} sx={{ minWidth: 0, overflowX: "hidden" }}>
      
      {/* FORM */}
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5">Run Plugins</Typography>

          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Memory File"
                value={form.memory_file}
                onChange={(e) =>
                  setForm({ ...form, memory_file: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Plugins</InputLabel>
                <Select
                  multiple
                  value={form.plugins}
                  label="Plugins"
                  onChange={(e) =>
                    setForm({ ...form, plugins: e.target.value })
                  }
                  input={<OutlinedInput label="Plugins" />}
                  renderValue={(selected) =>
                    selected.length > 0 ? selected.join(", ") : "Plugins"
                  }
                >
                  {availablePlugins.map((plugin) => (
                    <MenuItem key={plugin.id} value={plugin.label}>
                      <Checkbox checked={form.plugins.includes(plugin.label)} />
                      <ListItemText primary={plugin.label} />
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>OS</InputLabel>
                <Select
                  value={form.os}
                  label="OS"
                  onChange={(e) =>
                    setForm({ ...form, os: e.target.value, plugins: [] })
                  }
                >
                  {osOptions.map((os) => (
                    <MenuItem key={os} value={os}>{os}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6}>
              <TextField
                fullWidth
                label="PID (optional)"
                value={form.process}
                onChange={(e) =>
                  setForm({ ...form, process: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Address (optional)"
                value={form.address}
                onChange={(e) =>
                  setForm({ ...form, address: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={12}>
              <Button variant="contained" onClick={handleSubmit}>
                Run
              </Button>
            </Grid>
          </Grid>

          {jobId && (
            <Typography sx={{ mt: 2 }}>
              Job: {jobId} | Status: {status}
            </Typography>
          )}
        </Paper>
      </Grid>

      {/* RESULTS */}
      {results &&
        Object.entries(results).map(([plugin, data]) => {
          const { rows, columns } = buildGrid(data);

          return (
            <Grid item xs={12} key={plugin}>
              <Paper sx={{ p: 2 }}>
                
                {/* HEADER */}
                <Box
                  display="flex"
                  justifyContent="space-between"
                  alignItems="center"
                  sx={{ mb: 2 }}
                >
                  <Typography variant="h6">{plugin}</Typography>

                  {/* BUTTONS */}
                  <Box display="flex" gap={1}>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => exportToJson(plugin, data)}
                    >
                      JSON
                    </Button>

                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => exportToCsv(plugin, data)}
                    >
                      CSV
                    </Button>
                  </Box>
                </Box>

                {/* TABLE */}
                <div style={{ height: 420, width: "100%", overflowX: "auto" }}>
                  <DataGrid
                    rows={rows}
                    columns={columns}
                    pageSizeOptions={[5, 10, 25]}
                    initialState={{
                      pagination: {
                        paginationModel: { pageSize: 10 }
                      }
                    }}
                    sx={{ border: 0, minWidth: 0 }}
                    disableRowSelectionOnClick
                  />
                </div>

              </Paper>
            </Grid>
          );
        })}
    </Grid>
  );
}
