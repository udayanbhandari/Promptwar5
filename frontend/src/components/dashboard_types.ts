import type { PlanResponse, TaskItem, VendorItem } from '../types';

export type DashboardTabProps = {
  tasks: TaskItem[];
  warnings: string[];
  budgetItems: PlanResponse['budget'];
  vendors: VendorItem[];
  ideas: PlanResponse['ideas'];
  budgetTotal: number;
  taskProgress: number;
  onTaskToggle: (task: TaskItem) => void;
  onGenerateBrief: (vendor: VendorItem) => void;
};
