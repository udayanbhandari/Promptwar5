import type { DashboardTabProps } from './dashboard_types';
import BudgetTab from './BudgetTab';
import IdeasTab from './IdeasTab';
import OverviewTab from './OverviewTab';
import TimelineTab from './TimelineTab';
import VendorsTab from './VendorsTab';

type TabKey = 'overview' | 'budget' | 'timeline' | 'vendors' | 'ideas';

type DashboardContentProps = DashboardTabProps & {
  tab: TabKey;
};

export default function DashboardContent(props: DashboardContentProps) {
  switch (props.tab) {
    case 'overview':
      return <OverviewTab {...props} />;
    case 'budget':
      return <BudgetTab {...props} />;
    case 'timeline':
      return <TimelineTab {...props} />;
    case 'vendors':
      return <VendorsTab {...props} />;
    case 'ideas':
      return <IdeasTab {...props} />;
  }
}
