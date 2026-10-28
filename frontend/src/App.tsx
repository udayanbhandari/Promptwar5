import { Navigate, Route, Routes } from 'react-router-dom';
import WizardPage from './pages/Wizard';
import DashboardPage from './pages/Dashboard';
import PlanBPage from './pages/PlanB';
import RunSheetPage from './pages/RunSheet';
import SharedPage from './pages/Shared';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<WizardPage />} />
      <Route path="/plan/:id" element={<DashboardPage />} />
      <Route path="/plan/:id/plan-b" element={<PlanBPage />} />
      <Route path="/plan/:id/run-sheet" element={<RunSheetPage />} />
      <Route path="/shared/:token" element={<SharedPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
