import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { vi } from 'vitest';
import PlanBPage from './PlanB';
import { api } from '../api/client';

vi.mock('../api/client', () => ({
  api: {
    getRisks: vi.fn(),
    generateRisks: vi.fn(),
    simulateRisk: vi.fn(),
  },
}));

describe('Plan B', () => {
  it('simulates a scenario and displays before/after totals', async () => {
    vi.mocked(api.getRisks).mockResolvedValue([
      { id: 'risk-1', scenario_type: 'weather', trigger_name: 'Torrential rain', mitigation_plan: 'Move indoors', budget_impact: 15, is_activated: false },
    ]);
    vi.mocked(api.simulateRisk).mockResolvedValue({
      before_budget: { total: 1000 },
      after_budget: { total: 1200 },
      affected_tasks: [{ title: 'Move ceremony indoors' }],
      fallback_steps: 'Shift venue and confirm tent backup.',
    });

    render(
      <MemoryRouter initialEntries={['/plan/evt-1/plan-b']}>
        <Routes>
          <Route path="/plan/:id/plan-b" element={<PlanBPage />} />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => expect(api.getRisks).toHaveBeenCalled());
    fireEvent.click(screen.getByRole('button', { name: /Simulate/i }));
    await waitFor(() => expect(api.simulateRisk).toHaveBeenCalled());
    expect(screen.getByText(/before/i)).toBeInTheDocument();
  });
});
