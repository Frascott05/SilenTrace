import React, { useEffect, useState } from "react";
import {
  Grid,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Button,
  CircularProgress
} from "@mui/material";

import volPluginsService from "../services/volPluginsService";

const osOptions = ["windows", "linux", "mac"];

export default function PluginsPage() {
  const [selectedOs, setSelectedOs] = useState("windows");
  const [plugins, setPlugins] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    init();
  }, []);

  useEffect(() => {
    load();
  }, [selectedOs]);

  const init = async () => {
    setLoading(true);
    await volPluginsService.init();
    await load();
    setLoading(false);
  };

  const load = async () => {
    const data = await volPluginsService.getPlugins(selectedOs);
    setPlugins(data);
  };

  const refresh = async () => {
    await load();
  };

  const toggle = async (name) => {
    await volPluginsService.toggle(selectedOs, name);
    await refresh();
  };

  const enableAll = async () => {
    await volPluginsService.setAll(selectedOs, true);
    await refresh();
  };

  const disableAll = async () => {
    await volPluginsService.setAll(selectedOs, false);
    await refresh();
  };

  return (
    <Grid container spacing={3}>
      
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5">
            Volatility Plugins Manager (IndexedDB)
          </Typography>

          <Grid container spacing={2} sx={{ mt: 1 }}>
            
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>OS</InputLabel>
                <Select
                  value={selectedOs}
                  onChange={(e) => setSelectedOs(e.target.value)}
                  label="OS"
                >
                  {osOptions.map((os) => (
                    <MenuItem key={os} value={os}>
                      {os}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6} sx={{ display: "flex", gap: 2 }}>
              <Button variant="contained" onClick={enableAll}>
                Enable All
              </Button>
              <Button variant="outlined" onClick={disableAll}>
                Disable All
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </Grid>

      <Grid item xs={12}>
        <Paper sx={{ p: 2, minHeight: 400 }}>
          
          <Typography variant="h6">
            Plugins ({selectedOs})
          </Typography>

          {loading ? (
            <CircularProgress sx={{ mt: 2 }} />
          ) : (
            <List>
              {plugins.map((plugin) => (
                <ListItem key={plugin.name} divider>
                  <ListItemText
                    primary={plugin.name}
                    secondary={plugin.description}
                  />

                  <ListItemSecondaryAction>
                    <Switch
                      checked={!!plugin.enabled}
                      onChange={() => toggle(plugin.name)}
                    />
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          )}
        </Paper>
      </Grid>
    </Grid>
  );
}