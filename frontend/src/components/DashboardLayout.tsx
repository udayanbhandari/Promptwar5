import { useNavigate } from 'react-router-dom';
import Button from './Button';
import DashboardContent from './DashboardContent';
import Toast from './Toast';
import type { BudgetItem, PersonalizedIdea, TaskItem, VendorItem } from '../types';

type TabKey = 'overview' | 'budget' | 'timeline' | 'vendors' | 'ideas';
type DashboardLayoutProps = {
  id: string;
  title: string;
  tab: TabKey;
  error: string;
  toast: string;
  tasks: TaskItem[];
  warnings: string[];
  budgetItems: BudgetItem[];
  vendors: VendorItem[];
  ideas: PersonalizedIdea[];
  budgetTotal: number;
  taskProgress: number;
  onTabChange: (tab: TabKey) => void;
  onTaskToggle: (task: TaskItem) => Promise<void>;
  onGenerateBrief: (vendor: VendorItem) => Promise<void>;
  onShare: () => void;
  onCloseToast: () => void;
};

function DashboardHeader({ id, title, onShare }: Pick<DashboardLayoutProps, 'id' | 'title' | 'onShare'>) {
  const navigate = useNavigate();
  return <header className="topbar"><div><p className="eyebrow">Plan dashboard</p><h1>{title || id}</h1></div><div className="row"><Button variant="secondary" onClick={() => navigate(`/plan/${id}/plan-b`)}>Plan B</Button><Button variant="secondary" onClick={() => navigate(`/plan/${id}/run-sheet`)}>Run sheet</Button><Button onClick={onShare}>Share link</Button></div></header>;
}

function TabNavigation({ tab, onTabChange }: Pick<DashboardLayoutProps, 'tab' | 'onTabChange'>) {
  const tabs: TabKey[] = ['overview', 'budget', 'timeline', 'vendors', 'ideas'];
  return <div className="tablist" role="tablist" aria-label="Plan tabs">{tabs.map((tabKey) => <button key={tabKey} role="tab" aria-selected={tab === tabKey} className={`tab ${tab === tabKey ? 'active' : ''}`} onClick={() => onTabChange(tabKey)}>{tabKey}</button>)}</div>;
}

export default function DashboardLayout(props: DashboardLayoutProps) {
  return <main className="app-shell"><div className="page"><DashboardHeader id={props.id} title={props.title} onShare={props.onShare} /><TabNavigation tab={props.tab} onTabChange={props.onTabChange} />{props.error && <div className="error-box" role="alert">{props.error}</div>}<DashboardContent tab={props.tab} tasks={props.tasks} warnings={props.warnings} budgetItems={props.budgetItems} vendors={props.vendors} ideas={props.ideas} budgetTotal={props.budgetTotal} taskProgress={props.taskProgress} onTaskToggle={props.onTaskToggle} onGenerateBrief={props.onGenerateBrief} /></div>{props.toast && <Toast message={props.toast} onClose={props.onCloseToast} />}</main>;
}
