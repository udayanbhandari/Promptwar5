import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import Card from '../components/Card';
import EmptyState from '../components/EmptyState';

export default function SharedPage() {
  const { token } = useParams();
  const [plan, setPlan] = useState<any>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) return;
    api.getSharedPlan(token)
      .then((result) => setPlan(result))
      .catch(() => setError('This shared plan is unavailable or expired.'));
  }, [token]);

  if (error) {
    return (
      <main className="app-shell">
        <div className="page"><EmptyState title="View only" description={error} /></div>
      </main>
    );
  }

  if (!plan) {
    return (
      <main className="app-shell">
        <div className="page"><EmptyState title="Loading shared plan" description="Checking the link..." /></div>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <div className="page">
        <header className="topbar">
          <div>
            <p className="eyebrow">View only</p>
            <h1>{plan.title || 'Shared event plan'}</h1>
          </div>
        </header>
        <Card title="Event summary">
          <p>{plan.event_type} · {plan.city}</p>
          <p>{plan.guest_count} guests · {plan.target_date}</p>
        </Card>
      </div>
    </main>
  );
}
