import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../api/client';
import Button from '../components/Button';
import Card from '../components/Card';
import EmptyState from '../components/EmptyState';
import ProgressBar from '../components/ProgressBar';
import Skeleton from '../components/Skeleton';
import Toast from '../components/Toast';
import type { PlanResponse, TaskItem, VendorItem } from '../types';

type TabKey = 'overview' | 'budget' | 'timeline' | 'vendors' | 'ideas';

export default function DashboardPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [toast, setToast] = useState('');
  const [tab, setTab] = useState<TabKey>('overview');

  useEffect(() => {
    if (!id) return;
    api.getPlan(id)
      .then((result) => setPlan(result))
      .catch((err) => setError(err instanceof Error ? err.message : 'Unable to load plan'))
      .finally(() => setLoading(false));
  }, [id]);

  const tasks = useMemo(() => Array.isArray(plan?.tasks) ? plan.tasks : [], [plan?.tasks]);
  const warnings = useMemo(() => Array.isArray(plan?.warnings) ? plan.warnings : [], [plan?.warnings]);
  const budgetItems = useMemo(() => Array.isArray(plan?.budget) ? plan.budget : [], [plan?.budget]);
  const vendors = useMemo(() => Array.isArray(plan?.vendors) ? plan.vendors : [], [plan?.vendors]);
  const ideas = useMemo(() => Array.isArray(plan?.ideas) ? plan.ideas : [], [plan?.ideas]);

  const budgetTotal = useMemo(
    () => budgetItems.reduce((sum, item) => sum + Number(item.estimated_cost || 0), 0),
    [budgetItems],
  );

  const taskProgress = useMemo(() => {
    if (!Array.isArray(tasks) || tasks.length === 0) return 0;
    const complete = tasks.filter((task) => task?.status === 'completed').length;
    return Math.round((complete / tasks.length) * 100);
  }, [tasks]);

  const handleTaskToggle = async (task: TaskItem) => {
    if (!id) return;
    const nextStatus = task.status === 'completed' ? 'pending' : 'completed';
    const originalStatus = task.status;
    setPlan((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        tasks: prev.tasks.map((item) => (item.id === task.id ? { ...item, status: nextStatus } : item)),
      };
    });
    try {
      await api.updateTask(task.id ?? '', { status: nextStatus });
      setToast('Task updated');
    } catch {
      setPlan((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          tasks: prev.tasks.map((item) => (item.id === task.id ? { ...item, status: originalStatus } : item)),
        };
      });
      setError('Update failed — reverted');
    }
  };

  const handleGenerateBrief = async (vendor: VendorItem) => {
    if (!id) return;
    try {
      const brief = await api.generateVendorBrief(id, vendor.category);
      await navigator.clipboard.writeText(brief.enquiry_message);
      setToast('Brief copied to clipboard');
    } catch {
      setError('Could not generate vendor brief');
    }
  };

  if (loading) return <main className="app-shell"><div className="page"><Skeleton rows={5} /></div></main>;
  if (!plan) return <main className="app-shell"><div className="page"><EmptyState title="Plan not found" description="Create or reopen an event plan." /></div></main>;

  return (
    <main className="app-shell">
      <div className="page">
        <header className="topbar">
          <div>
            <p className="eyebrow">Plan dashboard</p>
            <h1>{plan.title || plan.event_id}</h1>
          </div>
          <div className="row">
            <Button variant="secondary" onClick={() => navigate(`/plan/${id}/plan-b`)}>Plan B</Button>
            <Button variant="secondary" onClick={() => navigate(`/plan/${id}/run-sheet`)}>Run sheet</Button>
            <Button onClick={() => setToast('Share link copied')}>Share link</Button>
          </div>
        </header>

        <div className="tablist" role="tablist" aria-label="Plan tabs">
          {(['overview','budget','timeline','vendors','ideas'] as TabKey[]).map((tabKey) => (
            <button
              key={tabKey}
              role="tab"
              aria-selected={tab === tabKey}
              className={`tab ${tab === tabKey ? 'active' : ''}`}
              onClick={() => setTab(tabKey)}
            >
              {tabKey}
            </button>
          ))}
        </div>

        {error && <div className="error-box" role="alert">{error}</div>}

        {tab === 'overview' && (
          <div className="stack">
            <section className="stats-row">
              <Card title="Budget health"><strong>{budgetTotal.toLocaleString()}</strong><span>Allocated</span></Card>
              <Card title="Timeline"><strong>{tasks.length}</strong><span>Tasks</span></Card>
              <Card title="Progress"><strong>{taskProgress}%</strong><span>Complete</span></Card>
            </section>
            <div className="stack-row">
              <Card title="Critical tasks">
                {tasks.slice(0, 3).map((task) => (
                  <div key={task.id ?? task.title} className="list-row">
                    <span>{task.title}</span>
                    <span>{task.status}</span>
                  </div>
                ))}
              </Card>
              <Card title="Budget warnings">
                {warnings.length ? warnings.map((warning) => <p key={warning}>{warning}</p>) : <p>All clear.</p>}
              </Card>
            </div>
            <Card title="Completion">
              <ProgressBar value={taskProgress} label="Task completion" />
            </Card>
          </div>
        )}

        {tab === 'budget' && (
          <div className="stack-row">
            <Card title="Budget split">
              <div className="donut-wrap">
                <svg viewBox="0 0 100 100" className="donut">
                  <circle cx="50" cy="50" r="36" className="donut-bg" />
                  <circle cx="50" cy="50" r="36" className="donut-ring" strokeDasharray="226" strokeDashoffset="50" />
                </svg>
                <div className="donut-center">{budgetTotal}</div>
              </div>
              {budgetItems.length ? budgetItems.map((item) => (
                <div key={item.id ?? item.category} className="slider-row">
                  <label>{item.category}</label>
                  <input type="range" min={0} max={200000} value={Number(item.estimated_cost ?? 0)} readOnly />
                  <span>{Number(item.estimated_cost ?? 0)}</span>
                </div>
              )) : <p>No budget items yet.</p>}
            </Card>
            <Card title="Warnings">
              {warnings.length ? warnings.map((warning) => <p key={warning}>{warning}</p>) : <p>Healthy budget posture.</p>}
            </Card>
          </div>
        )}

        {tab === 'timeline' && (
          <div className="timeline-groups">
            {(['This week', 'This month', 'Later'] as const).map((group) => (
              <Card key={group} title={group}>
                {tasks.filter((task) => {
                  if (group === 'This week') return task.due_date && new Date(task.due_date) <= new Date(Date.now() + 7 * 86400000);
                  if (group === 'This month') return task.due_date && new Date(task.due_date) <= new Date(Date.now() + 30 * 86400000);
                  return task.due_date && new Date(task.due_date) > new Date(Date.now() + 30 * 86400000);
                }).map((task) => (
                  <button key={task.id ?? task.title} type="button" className="task-row" onClick={() => handleTaskToggle(task)}>
                    <span>{task.title}</span>
                    <span>{task.status}</span>
                  </button>
                ))}
              </Card>
            ))}
          </div>
        )}

        {tab === 'vendors' && (
          <div className="stack">
            {vendors.length ? vendors.map((vendor) => (
              <Card key={vendor.id ?? vendor.category} title={vendor.category}>
                <p>{vendor.name}</p>
                <p>{vendor.status}</p>
                <Button variant="secondary" onClick={() => handleGenerateBrief(vendor)}>Generate brief</Button>
              </Card>
            )) : <Card title="Vendors"><p>No vendors yet.</p></Card>}
          </div>
        )}

        {tab === 'ideas' && (
          <div className="stack">
            {ideas.length ? ideas.map((idea) => (
              <Card key={`${idea.aspect}-${idea.title}`} title={idea.title}>
                <p>{idea.description}</p>
                <div className="row">
                  <Button variant="secondary">Skip</Button>
                  <Button>Save</Button>
                </div>
              </Card>
            )) : <Card title="Ideas"><p>No ideas yet.</p></Card>}
          </div>
        )}
      </div>
      {toast && <Toast message={toast} onClose={() => setToast('')} />}
    </main>
  );
}
