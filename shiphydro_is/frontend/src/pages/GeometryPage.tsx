import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useEffect, useState } from 'react';
import type { GeometryParam } from '../types';

const defaultGeom: GeometryParam = {
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

function HullPreview({ geometry }: { geometry: GeometryParam }) {
  const points = Array.from({ length: 40 }).map((_, idx) => {
    const x = (geometry.lpp * idx) / 40;
    const radius = (geometry.beam / 2) * Math.sin((Math.PI * idx) / 40);
    return [x / 20 - 3, radius / 10, 0];
  });
  return (
    <line>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={points.length}
          array={new Float32Array(points.flat())}
          itemSize={3}
        />
      </bufferGeometry>
      <lineBasicMaterial color="teal" linewidth={2} />
    </line>
  );
}

export default function GeometryPage() {
  const [geometry, setGeometry] = useState<GeometryParam>(defaultGeom);

  useEffect(() => {
    fetch('/api/v1/jobs', { method: 'HEAD' }).catch(() => undefined);
  }, []);

  return (
    <section className="geometry-page">
      <div className="form">
        <h2>Geometry Parameters</h2>
        <div className="grid">
          {(['lpp', 'beam', 'depth', 'draft', 'cb'] as const).map((key) => (
            <label key={key}>
              {key.toUpperCase()}
              <input
                type="number"
                value={geometry[key] as number}
                onChange={(event) => setGeometry({ ...geometry, [key]: Number(event.target.value) })}
              />
            </label>
          ))}
        </div>
      </div>
      <div className="viewer">
        <Canvas camera={{ position: [0, 0, 10], fov: 45 }}>
          <ambientLight intensity={0.3} />
          <pointLight position={[10, 10, 10]} />
          <HullPreview geometry={geometry} />
          <OrbitControls />
        </Canvas>
      </div>
    </section>
  );
}
