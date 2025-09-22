import { useState } from 'react';
import type { CaseSpec, GeometryParam, RunRequest } from '../types';

type Props = {
  onTabChange: (tab: 'monitor') => void;
};

const defaultGeometry: GeometryParam = {
  name: 'demo_hull',
  lpp: 120,
  beam: 20,
  depth: 12,
  draft: 7.5,
  cb: 0.62,
  bulbous_bow_length: 0.08,
  bulbous_bow_radius: 0.12,
  sections: []
};

const defaultCase: CaseSpec = {
  geometry_id: 'demo_hull',
  speed: 8,
  draft: 7,
  froude_number: 0.25,
  reynolds_number: 1.5e8,
  fluid: { density: 1025, viscosity: 0.0011 },
  turbulence_model: 'k-omega-sst',
  solver_options: {}
};

export default function RunPage({ onTabChange }: Props) {
  const [geometry, setGeometry] = useState(defaultGeometry);
  const [caseSpec, setCaseSpec] = useState(defaultCase);
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('Idle');

  const submitRun = async () => {
    const payload: RunRequest = { geometry, case: caseSpec, use_mock: true };
    const response = await fetch('/api/v1/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    setJobId(data.job_id);
    localStorage.setItem('shiphydro-job', data.job_id);
    setStatus(`Submitted job ${data.job_id}`);
    onTabChange('monitor');
  };

  return (
    <section className="run-page">
      <h2>Case Builder</h2>
      <div className="grid">
        <label>
          Speed (m/s)
          <input
            type="number"
            value={caseSpec.speed}
            onChange={(event) => setCaseSpec({ ...caseSpec, speed: Number(event.target.value) })}
          />
        </label>
        <label>
          Draft (m)
          <input
            type="number"
            value={caseSpec.draft}
            onChange={(event) => setCaseSpec({ ...caseSpec, draft: Number(event.target.value) })}
          />
        </label>
      </div>
      <button onClick={submitRun}>Submit Mock Run</button>
      {status && <p>{status}</p>}
    </section>
  );
}
