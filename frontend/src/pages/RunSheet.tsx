import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';

const defaultSchedule = [
  { time: '08:00', title: 'Hair & makeup', type: 'buffer' },
  { time: '09:30', title: 'Room check', type: 'task' },
  { time: '12:00', title: 'Lunch break', type: 'buffer' },
  { time: '14:00', title: 'Guest arrival', type: 'task' },
  { time: '15:30', title: 'Ceremony', type: 'task' },
  { time: '17:00', title: 'Cocktail hour', type: 'buffer' },
  { time: '18:30', title: 'Dinner', type: 'task' },
  { time: '22:00', title: 'Cleanup window', type: 'buffer' },
];

export default function RunSheetPage() {
  const { id } = useParams();
  const [runsheet, setRunsheet] = useState(defaultSchedule);

  useEffect(() => {
    if (!id) return;
    api.getRunsheet(id).then((result) => {
      if (Array.isArray(result.runsheet) && result.runsheet.length) setRunsheet(result.runsheet as typeof defaultSchedule);
    }).catch(() => undefined);
  }, [id]);

  return (
    <main className="app-shell">
      <div className="page">
        <header className="topbar">
          <div>
            <p className="eyebrow">Run sheet</p>
            <h1>Day-of schedule</h1>
          </div>
        </header>
        <div className="run-sheet" aria-label="Run sheet timeline">
          {runsheet.map((slot) => (
            <div key={`${slot.time}-${slot.title}`} className={`run-item ${slot.type}`}>
              <time>{slot.time}</time>
              <div>
                <strong>{slot.title}</strong>
                <span>{slot.type === 'buffer' ? 'Buffer slot' : 'Planned activity'}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
