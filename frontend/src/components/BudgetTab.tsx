import Card from './Card';
import type { DashboardTabProps } from './dashboard_types';

export default function BudgetTab({
  warnings, budgetItems, budgetTotal,
}: DashboardTabProps) {
  return (
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
  );
}
