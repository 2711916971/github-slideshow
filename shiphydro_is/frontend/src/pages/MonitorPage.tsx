import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import type { MetricPoint, RunMetrics, RunStatus } from '../types';

export default function MonitorPage() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<RunStatus | null>(null);
  const [metrics, setMetrics] = useState<RunMetrics | null>(null);

  useEffect(() => {
    const id = localStorage.getItem('shiphydro-job');
    if (id) {
      setJobId(id);
    }
  }, []);

  useEffect(() => {
    if (!jobId) return;
    const timer = setInterval(async () => {
      const statusResp = await fetch(`/api/v1/jobs/${jobId}`);
      if (statusResp.ok) {
        const statusData = await statusResp.json();
        setStatus(statusData);
        if (statusData.state === 'SUCCEEDED') {
          const metricResp = await fetch(`/api/v1/results/${jobId}`);
          if (metricResp.ok) {
            const metricData = await metricResp.json();
            setMetrics(metricData);
          }
        }
      }
    }, 2000);
    return () => clearInterval(timer);
  }, [jobId]);

  const residualData: MetricPoint[] = metrics?.residuals ?? [];

  return (
    <section className="monitor-page">
      <h2>Run Monitor</h2>
      {jobId ? <p>Monitoring job {jobId}</p> : <p>No job submitted yet.</p>}
      {status && (
        <div className="status">
          <p>State: {status.state}</p>
          <p>Stage: {status.stage}</p>
          <p>Progress: {(status.progress * 100).toFixed(1)}%</p>
        </div>
      )}
      {metrics && (
        <div className="metrics">
          <p>Total resistance Rt: {metrics.resistance_total.toFixed(3)} N</p>
          <p>Resistance coefficient Ct: {metrics.resistance_coefficient.toFixed(5)}</p>
        </div>
      )}
      {residualData.length > 0 && (
        <LineChart width={500} height={300} data={residualData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" hide />
          <YAxis domain={[0, 'dataMax']} />
          <Tooltip />
          <Line type="monotone" dataKey="residual" stroke="#8884d8" />
        </LineChart>
      )}
    </section>
  );
}
