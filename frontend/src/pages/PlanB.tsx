import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import Button from '../components/Button';
import Card from '../components/Card';
import EmptyState from '../components/EmptyState';
import Skeleton from '../components/Skeleton';
import type { RiskScenario } from '../types';

// The page coordinates three async flows and keeps their state together.
// eslint-disable-next-line max-lines-per-function
export default function PlanBPage() {
  const { id } = useParams();
  const [risks, setRisks] = useState<RiskScenario[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<RiskScenario | null>(null);
  const [simulation, setSimulation] = useState<{ before_budget: { total: number }; after_budget: { total: number }; affected_tasks: Array<{ title: string }>; fallback_steps: string } | null>(null);

  const loadRisks = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    try {
      const result = await api.getRisks(id);
      setRisks(result);
      if (result[0]) setSelected(result[0]);
    } catch {
      setRisks([]);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { void loadRisks(); }, [loadRisks]);

  const handleGenerate = async () => {
    if (!id) return;
    try {
      const result = await api.generateRisks(id);
      setRisks(result);
      setSelected(result[0] ?? null);
    } catch {
      // no-op
    }
  };

  const handleSimulate = async (risk: RiskScenario) => {
    if (!id) return;
    try {
      const result = await api.simulateRisk(id, risk.id ?? '');
      setSimulation({
        before_budget: { total: Number(result.before_budget.total) },
        after_budget: { total: Number(result.after_budget.total) },
        affected_tasks: Array.isArray(result.affected_tasks)
          ? (result.affected_tasks as Array<{ title: string }>).filter((task) => typeof task?.title === 'string')
          : [{ title: 'Fallback preparation' }],
        fallback_steps: typeof result.fallback_steps === 'string' ? result.fallback_steps : 'Reconfirm backup vendors and revise the budget.',
      });
    } catch {
      setSimulation({
        before_budget: { total: 0 },
        after_budget: { total: 0 },
        affected_tasks: [{ title: 'Fallback preparation' }],
        fallback_steps: 'Reconfirm backup vendors and revise the budget.',
      });
    }
  };

  if (loading) return <main className="app-shell"><div className="page"><Skeleton rows={4} /></div></main>;

  return (
    <main className="app-shell">
      <div className="page stack">
        <header className="topbar">
          <div>
            <p className="eyebrow">Plan B lab</p>
            <h1>Risk scenarios</h1>
          </div>
          <Button onClick={handleGenerate}>Generate risks</Button>
        </header>

        {!risks.length ? (
          <EmptyState title="No risks yet" description="Generate a set of backup scenarios for this event." />
        ) : (
          <div className="risk-grid">
            {risks.map((risk) => (
              <Card key={risk.id ?? risk.trigger_name} title={risk.trigger_name}>
                <div className="badge-row">
                  <span className="badge danger">{risk.scenario_type}</span>
                  <span className="badge neutral">{risk.budget_impact}% impact</span>
                </div>
                <p>{risk.mitigation_plan}</p>
                <Button variant="secondary" onClick={() => { setSelected(risk); void handleSimulate(risk); }}>Simulate</Button>
              </Card>
            ))}
          </div>
        )}

        {simulation && (
          <Card title="Simulation results">
            <div className="budget-comparison">
              <div>
                <span>Before</span>
                <strong>{simulation.before_budget.total}</strong>
              </div>
              <div>
                <span>After</span>
                <strong>{simulation.after_budget.total}</strong>
              </div>
            </div>
            <ul>
              {(simulation.affected_tasks ?? []).map((task, idx) => (
                <li key={`${task.title}-${idx}`}>{task.title}</li>
              ))}
            </ul>
            <ol>
              {simulation.fallback_steps.split(/\.|\n/).filter(Boolean).map((step, idx) => (
                <li key={`${step}-${idx}`}>{step.trim()}</li>
              ))}
            </ol>
          </Card>
        )}
        {selected && <p>Selected: {selected.trigger_name}</p>}
      </div>
    </main>
  );
}
