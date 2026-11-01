import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import EmptyState from '../components/EmptyState';
import Skeleton from '../components/Skeleton';
import type { PlanResponse, TaskItem, VendorItem } from '../types';
import DashboardLayout from '../components/DashboardLayout';

type TabKey = 'overview' | 'budget' | 'timeline' | 'vendors' | 'ideas';

// The page coordinates loading, optimistic task updates, and child callbacks.
// eslint-disable-next-line max-lines-per-function
export default function DashboardPage() {
  const { id } = useParams();
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
  if (!plan || !id) return <main className="app-shell"><div className="page"><EmptyState title="Plan not found" description="Create or reopen an event plan." /></div></main>;
  return <DashboardLayout id={id} title={plan.title || plan.event_id} tab={tab} error={error} toast={toast} tasks={tasks} warnings={warnings} budgetItems={budgetItems} vendors={vendors} ideas={ideas} budgetTotal={budgetTotal} taskProgress={taskProgress} onTabChange={setTab} onTaskToggle={handleTaskToggle} onGenerateBrief={handleGenerateBrief} onShare={() => setToast('Share link copied')} onCloseToast={() => setToast('')} />;
}
