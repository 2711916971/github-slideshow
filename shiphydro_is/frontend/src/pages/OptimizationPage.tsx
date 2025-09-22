import { useEffect, useState } from 'react';

type Candidate = {
  id: number;
  Rt: number;
  Ct: number;
};

export default function OptimizationPage() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);

  useEffect(() => {
    setCandidates(
      Array.from({ length: 5 }).map((_, idx) => ({
        id: idx,
        Rt: 100 + idx * 5,
        Ct: 0.003 - idx * 0.0002
      }))
    );
  }, []);

  return (
    <section className="optimization-page">
      <h2>Optimization Experiments</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Rt (N)</th>
            <th>Ct</th>
          </tr>
        </thead>
        <tbody>
          {candidates.map((candidate) => (
            <tr key={candidate.id}>
              <td>{candidate.id}</td>
              <td>{candidate.Rt.toFixed(2)}</td>
              <td>{candidate.Ct.toFixed(4)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
