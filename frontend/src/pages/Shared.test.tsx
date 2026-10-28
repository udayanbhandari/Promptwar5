import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { vi } from 'vitest';
import SharedPage from './Shared';
import { api } from '../api/client';

vi.mock('../api/client', () => ({
  api: {
    getSharedPlan: vi.fn(),
  },
}));

describe('Shared page', () => {
  it('shows the invalid-link state when the token is unavailable', async () => {
    vi.mocked(api.getSharedPlan).mockRejectedValue(new Error('not found'));

    render(
      <MemoryRouter initialEntries={['/shared/abc']}>
        <Routes>
          <Route path="/shared/:token" element={<SharedPage />} />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText(/View only/i)).toBeInTheDocument();
    });
  });
});
