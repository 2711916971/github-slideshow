import { useMemo, useState } from 'react';
import GeometryPage from './pages/GeometryPage';
import RunPage from './pages/RunPage';
import MonitorPage from './pages/MonitorPage';
import OptimizationPage from './pages/OptimizationPage';
import './app.css';

type TabKey = 'geometry' | 'run' | 'monitor' | 'optimization';

const TABS: { key: TabKey; label: string }[] = [
  { key: 'geometry', label: 'Geometry Lab' },
  { key: 'run', label: 'Case Builder' },
  { key: 'monitor', label: 'Run Monitor' },
  { key: 'optimization', label: 'Optimization' }
];

export default function App() {
  const [tab, setTab] = useState<TabKey>('geometry');
  const content = useMemo(() => {
    switch (tab) {
      case 'geometry':
        return <GeometryPage />;
      case 'run':
        return <RunPage onTabChange={setTab} />;
      case 'monitor':
        return <MonitorPage />;
      case 'optimization':
        return <OptimizationPage />;
      default:
        return null;
    }
  }, [tab]);

  return (
    <div className="app">
      <header>
        <h1>ShipHydro-IS Console</h1>
        <nav>
          {TABS.map((item) => (
            <button
              key={item.key}
              className={item.key === tab ? 'active' : ''}
              onClick={() => setTab(item.key)}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </header>
      <main>{content}</main>
    </div>
  );
}
