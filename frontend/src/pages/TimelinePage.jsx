import React, { useState, useEffect } from "react";
import {
  Grid,
  Paper,
  TextField,
  Button,
  Typography,
  Chip,
  Stack,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import { getTimeline, getStatus, getResults } from "../services/api";

export default function TimelineDashboard() {
  const [memoryFile, setMemoryFile] = useState("");
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [data, setData] = useState(null);

  const handleRun = async () => {
    const res = await getTimeline({
      memory_file: memoryFile,
      job_type: "timeliner"
    });
    setJobId(res.data.job_id);
  };

  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      const s = await getStatus(jobId);
      setStatus(s.data.status);

      if (s.data.status === "done") {
        clearInterval(interval);
        const r = await getResults(jobId);
        setData(r.data);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [jobId]);

  const riskColor = (r) => {
    if (!r) return "#ccc";
    if (r.toLowerCase() === "high") return "#ff4d4d";
    if (r.toLowerCase() === "medium") return "#ffa500";
    return "#4caf50";
  };

  // -----------------------------
  // 📊 STATS
  // -----------------------------
  const stats = data?.processes?.reduce(
    (acc, p) => {
      acc.total++;
      acc[p.risk.toLowerCase()]++;
      return acc;
    },
    { total: 0, high: 0, medium: 0, low: 0 }
  );

  const chartData = stats
    ? [
        { name: "High", value: stats.high },
        { name: "Medium", value: stats.medium },
        { name: "Low", value: stats.low }
      ]
    : [];

  // -----------------------------
  // 🕒 GLOBAL TIMELINE
  // -----------------------------
  const flatTimeline = data?.global_timeline?.sort(
    (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
  );

  // -----------------------------
  // 🔴 HIGH RISK ONLY
  // -----------------------------
  const highRiskProcesses = data?.processes?.filter(
    (p) => p.risk === "HIGH"
  );

  return (
    <Grid container spacing={2}>

      {/* INPUT */}
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5">Forensic Timeline (Windows Only)</Typography>

          <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Memory file"
              value={memoryFile}
              onChange={(e) => setMemoryFile(e.target.value)}
            />
            <Button variant="contained" onClick={handleRun}>
              Run
            </Button>
          </Stack>

          {jobId && (
            <Typography sx={{ mt: 2 }}>
              {jobId} | {status}
            </Typography>
          )}
        </Paper>
      </Grid>

      {/* 📊 OVERVIEW */}
      {stats && (
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Overview</Typography>

            <Stack spacing={1} sx={{ mt: 2 }}>
              <Chip label={`Total: ${stats.total}`} />
              <Chip label={`High: ${stats.high}`} sx={{ bgcolor: "#ff4d4d" }} />
              <Chip label={`Medium: ${stats.medium}`} sx={{ bgcolor: "#ffa500" }} />
              <Chip label={`Low: ${stats.low}`} sx={{ bgcolor: "#4caf50" }} />
            </Stack>
          </Paper>
        </Grid>
      )}

      {/* 📊 CHART */}
      {chartData.length > 0 && (
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: 250 }}>
            <Typography variant="h6">Risk Distribution</Typography>

            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      )}

      {/* 🔴 HIGH RISK */}
      {highRiskProcesses?.length > 0 && (
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">⚠ High Risk Processes</Typography>

            <Stack spacing={2} sx={{ mt: 2 }}>
              {highRiskProcesses.map((p) => (
                <Paper
                  key={p.pid}
                  sx={{
                    p: 2,
                    borderLeft: "5px solid red"
                  }}
                >
                  <Typography>
                    {p.name} (PID {p.pid})
                  </Typography>

                  <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                    {p.detections.map((d) => (
                      <Chip key={d} label={d} size="small" />
                    ))}
                  </Stack>
                </Paper>
              ))}
            </Stack>
          </Paper>
        </Grid>
      )}

      {/* 🌳 PROCESS VIEW */}
      {data?.processes && (
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Processes</Typography>

            {data.processes.map((p) => (
              <Accordion key={p.pid}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" spacing={2}>
                    <Typography>
                      {p.name} (PID {p.pid})
                    </Typography>

                    <Chip
                      label={p.risk}
                      sx={{ bgcolor: riskColor(p.risk) }}
                    />

                    <Typography>Score: {p.score}</Typography>
                  </Stack>
                </AccordionSummary>

                <AccordionDetails>
                  <Stack spacing={1}>
                    {p.events.map((e, i) => (
                      <Paper key={i} sx={{ p: 1 }}>
                        <Typography variant="caption">
                          {e.timestamp}
                        </Typography>
                        <Typography>{e.description}</Typography>
                      </Paper>
                    ))}
                  </Stack>
                </AccordionDetails>
              </Accordion>
            ))}
          </Paper>
        </Grid>
      )}

      {/* 🕒 GLOBAL TIMELINE */}
      {flatTimeline && (
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Global Timeline</Typography>
            <Divider sx={{ my: 2 }} />

            <Stack spacing={1}>
              {flatTimeline.map((e, i) => (
                <Paper
                  key={i}
                  sx={{
                    p: 2,
                    borderLeft: `5px solid ${riskColor(e.risk)}`
                  }}
                >
                  <Stack direction="row" spacing={2}>
                    <Typography sx={{ minWidth: 160 }}>
                      {e.timestamp}
                    </Typography>

                    <Typography sx={{ flex: 1 }}>
                      {e.description}
                    </Typography>

                    <Chip label={`PID ${e.pid}`} size="small" />
                  </Stack>
                </Paper>
              ))}
            </Stack>
          </Paper>
        </Grid>
      )}

    </Grid>
  );
}