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
  ListItemText
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

  return (
    <Grid container spacing={3} sx={{ minWidth: 0 }}>

      {/* FORM */}
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5">
            Run Plugins
          </Typography>

          <Grid container spacing={2} sx={{ mt: 1 }}>

            {/* MEMORY FILE */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Memory File"
                value={form.memory_file}
                onChange={(e) =>
                  setForm({
                    ...form,
                    memory_file: e.target.value
                  })
                }
              />
            </Grid>

            {/* PLUGINS */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Plugins</InputLabel>

                <Select
                  multiple
                  value={form.plugins}
                  label="Plugins"
                  onChange={(e) =>
                    setForm({
                      ...form,
                      plugins: e.target.value
                    })
                  }
                  input={<OutlinedInput label="Plugins" />}
                  renderValue={(selected) =>
                    selected.length > 0
                      ? selected.join(", ")
                      : "Plugins"
                  }
                  MenuProps={{
                    disablePortal: true,
                    PaperProps: {
                      sx: {
                        mt: 1,
                        maxHeight: 300,
                        minWidth: 280
                      }
                    }
                  }}
                >
                  {availablePlugins.map((plugin) => (
                    <MenuItem
                      key={plugin.id}
                      value={plugin.label}
                    >
                      <Checkbox
                        checked={form.plugins.includes(
                          plugin.label
                        )}
                      />
                      <ListItemText primary={plugin.label} />
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* OS */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>OS</InputLabel>
                <Select
                  value={form.os}
                  label="OS"
                  onChange={(e) =>
                    setForm({
                      ...form,
                      os: e.target.value,
                      plugins: []
                    })
                  }
                >
                  {osOptions.map((os) => (
                    <MenuItem key={os} value={os}>
                      {os}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* PID */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="PID (optional)"
                value={form.process}
                onChange={(e) =>
                  setForm({
                    ...form,
                    process: e.target.value
                  })
                }
              />
            </Grid>

            {/* ADDRESS */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Address (optional)"
                value={form.address}
                onChange={(e) =>
                  setForm({
                    ...form,
                    address: e.target.value
                  })
                }
              />
            </Grid>

            {/* RUN */}
            <Grid item xs={12}>
              <Button
                variant="contained"
                onClick={handleSubmit}
              >
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
                <Typography variant="h6">
                  {plugin}
                </Typography>

                <div style={{ height: 420, width: "100%" }}>
                  <DataGrid
                    rows={rows}
                    columns={columns}
                    pageSizeOptions={[5, 10, 25]}
                    initialState={{
                      pagination: {
                        paginationModel: {
                          pageSize: 10
                        }
                      }
                    }}
                    sx={{ border: 0 }}
                  />
                </div>
              </Paper>
            </Grid>
          );
        })}
    </Grid>
  );
}