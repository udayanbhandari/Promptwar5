import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { vi } from 'vitest';
import WizardPage from './Wizard';
import { api } from '../api/client';

vi.mock('../api/client', () => ({
  api: {
    createEvent: vi.fn(),
    generatePlan: vi.fn(),
  },
}));

describe('Wizard flow', () => {
  it('runs a full event creation flow', async () => {
    const createEvent = vi.mocked(api.createEvent);
    const generatePlan = vi.mocked(api.generatePlan);

    createEvent.mockResolvedValue({
      id: 'evt-123',
      title: 'Sunset Wedding',
      event_type: 'wedding',
      target_date: '2030-06-15',
      guest_count: 120,
      total_budget: 28000,
      currency: 'USD',
      city: 'Seattle, WA',
      theme_style: 'Warm Minimalist',
      special_requirements: 'Wheelchair accessible',
      created_at: '2026-01-01T00:00:00Z',
      updated_at: '2026-01-01T00:00:00Z',
    });
    generatePlan.mockResolvedValue({
      event_id: 'evt-123',
      used_fallback: false,
      budget: [],
      ideas: [],
      vendor_categories: [],
      tasks: [],
      vendors: [],
      warnings: [],
    });

    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<WizardPage />} />
        </Routes>
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByRole('button', { name: /Wedding/i }));
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    fireEvent.change(screen.getByLabelText(/Event date/i), { target: { value: '2030-06-15' } });
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    fireEvent.change(screen.getByRole('spinbutton'), { target: { value: '120' } });
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    fireEvent.change(screen.getByLabelText(/Budget/i), { target: { value: '28000' } });
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    fireEvent.change(screen.getByLabelText(/City or region/i), { target: { value: 'Seattle, WA' } });
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    fireEvent.change(screen.getByLabelText(/Style \/ theme/i), { target: { value: 'Warm Minimalist' } });
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    fireEvent.change(screen.getByLabelText(/Event title/i), { target: { value: 'Sunset Wedding' } });
    fireEvent.click(screen.getByRole('button', { name: /Create plan/i }));

    await waitFor(() => {
      expect(createEvent).toHaveBeenCalled();
      expect(generatePlan).toHaveBeenCalledWith('evt-123');
    });
  });
});
