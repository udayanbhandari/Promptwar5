import Card from './Card';
import ProgressBar from './ProgressBar';
import type { DashboardTabProps } from './dashboard_types';

export default function OverviewTab({
  tasks, warnings, budgetTotal, taskProgress,
}: DashboardTabProps) {
  return (
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
  );
}
