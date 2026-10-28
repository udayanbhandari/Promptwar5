import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { vi } from 'vitest';
import DashboardPage from './Dashboard';
import { api } from '../api/client';

vi.mock('../api/client', () => ({
  api: {
    getPlan: vi.fn(),
    updateTask: vi.fn(),
    generateVendorBrief: vi.fn(),
  },
}));

describe('Dashboard', () => {
  it('toggles task completion', async () => {
    vi.mocked(api.getPlan).mockResolvedValue({
      event_id: 'evt-1',
      used_fallback: false,
      budget: [{ id: 'b1', category: 'Venue', item_name: 'Venue', estimated_cost: 1000, actual_cost: 0, is_paid: false, priority: 1 }],
      ideas: [],
      vendor_categories: [],
      tasks: [{ id: 'task-1', title: 'Book venue', category: 'Venue', due_date: '2030-03-01', status: 'pending', owner: 'Host', depends_on: [], is_day_of: false }],
      vendors: [],
      warnings: [],
    });
    vi.mocked(api.updateTask).mockResolvedValue({
      id: 'task-1',
      title: 'Book venue',
      category: 'Venue',
      due_date: '2030-03-01',
      status: 'completed',
      owner: 'Host',
      depends_on: [],
      is_day_of: false,
      event_id: 'evt-1',
      created_at: '2026-01-01T00:00:00Z',
    });

    render(
      <MemoryRouter initialEntries={['/plan/evt-1']}>
        <Routes>
          <Route path="/plan/:id" element={<DashboardPage />} />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => expect(api.getPlan).toHaveBeenCalled());
    fireEvent.click(screen.getByRole('tab', { name: /timeline/i }));
    fireEvent.click(screen.getByRole('button', { name: /Book venue/i }));

    await waitFor(() => expect(api.updateTask).toHaveBeenCalled());
  });
});
