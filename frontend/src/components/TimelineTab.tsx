import Card from './Card';
import type { DashboardTabProps } from './dashboard_types';

export default function TimelineTab({
  tasks, onTaskToggle,
}: DashboardTabProps) {
  return (
<div className="timeline-groups">
            {(['This week', 'This month', 'Later'] as const).map((group) => (
              <Card key={group} title={group}>
                {tasks.filter((task) => {
                  if (group === 'This week') return task.due_date && new Date(task.due_date) <= new Date(Date.now() + 7 * 86400000);
                  if (group === 'This month') return task.due_date && new Date(task.due_date) <= new Date(Date.now() + 30 * 86400000);
                  return task.due_date && new Date(task.due_date) > new Date(Date.now() + 30 * 86400000);
                }).map((task) => (
                  <button key={task.id ?? task.title} type="button" className="task-row" onClick={() => onTaskToggle(task)}>
                    <span>{task.title}</span>
                    <span>{task.status}</span>
                  </button>
                ))}
              </Card>
            ))}
          </div>
  );
}
