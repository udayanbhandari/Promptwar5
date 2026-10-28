import { useEffect, useMemo, useState, type KeyboardEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import Button from '../components/Button';
import ProgressBar from '../components/ProgressBar';
import type { CurrencyCode, EventType } from '../types';

const STORAGE_KEY = 'eventpilot-wizard-draft';

const EVENT_OPTIONS: Array<{ value: EventType; label: string; description: string }> = [
  { value: 'wedding', label: 'Wedding', description: 'Celebrate a milestone day' },
  { value: 'birthday', label: 'Birthday', description: 'A fun personal moment' },
  { value: 'community', label: 'Community', description: 'A shared gathering' },
];

const THEME_CHOICES = ['Warm Minimalist', 'Retro Arcade', 'Eco Fair', 'Modern Luxury', 'Garden Glow'];
const REQUIREMENT_CHOICES = ['Wheelchair accessible', 'Vegetarian options', 'Gluten-free', 'Quiet room', 'Stage access'];

type WizardForm = {
  title: string;
  event_type: EventType;
  target_date: string;
  guest_count: number;
  total_budget: number;
  currency: CurrencyCode;
  city: string;
  theme_style: string;
  special_requirements: string;
};

const defaultForm: WizardForm = {
  title: '',
  event_type: 'wedding',
  target_date: '',
  guest_count: 100,
  total_budget: 2000,
  currency: 'USD',
  city: '',
  theme_style: 'Warm Minimalist',
  special_requirements: 'Wheelchair accessible',
};

export default function WizardPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState<WizardForm>(defaultForm);
  const [step, setStep] = useState(0);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved) as Partial<typeof defaultForm>;
        setForm({ ...defaultForm, ...parsed });
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(form));
  }, [form]);

  const totalSteps = 6;
  const canNext = useMemo(() => {
    switch (step) {
      case 0:
        return Boolean(form.event_type);
      case 1:
        return Boolean(form.target_date);
      case 2:
        return form.guest_count > 0;
      case 3:
        return form.total_budget > 0;
      case 4:
        return form.city.length > 1;
      case 5:
        return Boolean(form.theme_style || form.special_requirements);
      default:
        return true;
    }
  }, [form, step]);

  const handleField = <K extends keyof typeof form>(field: K, value: (typeof form)[K]) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    setError('');
  };

  const validateStep = () => {
    if (step === 1 && !form.target_date) {
      setError('Choose a date in the future.');
      return false;
    }
    if (step === 2 && form.guest_count < 1) {
      setError('Guest count must be at least 1.');
      return false;
    }
    if (step === 3 && form.total_budget <= 0) {
      setError('Budget must be greater than zero.');
      return false;
    }
    return true;
  };

  const nextStep = () => {
    if (!validateStep()) return;
    if (step < totalSteps) setStep((current) => current + 1);
  };

  const fillSmartDefaults = () => {
    const defaults: Record<EventType, Partial<typeof defaultForm>> = {
      wedding: { title: 'Wedding Weekend', target_date: '', guest_count: 120, total_budget: 28000, currency: 'USD', city: 'Seattle, WA', theme_style: 'Warm Minimalist', special_requirements: 'Wheelchair accessible' },
      birthday: { title: 'Birthday Bash', target_date: '', guest_count: 35, total_budget: 2200, currency: 'USD', city: 'Austin, TX', theme_style: 'Retro Arcade', special_requirements: 'Gluten-free' },
      community: { title: 'Community Fair', target_date: '', guest_count: 250, total_budget: 6000, currency: 'USD', city: 'Denver, CO', theme_style: 'Eco Fair', special_requirements: 'Wheelchair accessible' },
    };
    setForm((prev) => ({ ...prev, ...defaults[form.event_type] }));
  };

  const handleSubmit = async () => {
    if (!form.title.trim()) {
      setError('Please add a short event title.');
      return;
    }
    setIsSubmitting(true);
    setError('');

    try {
      const created = await api.createEvent({
        title: form.title,
        event_type: form.event_type,
        target_date: form.target_date,
        guest_count: form.guest_count,
        total_budget: Number(form.total_budget),
        currency: form.currency,
        city: form.city,
        theme_style: form.theme_style,
        special_requirements: form.special_requirements,
      });

      await api.generatePlan(created.id);
      localStorage.removeItem(STORAGE_KEY);
      navigate(`/plan/${created.id}`);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unable to create your plan.';
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const onKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Enter' && !isSubmitting) {
      if (step < totalSteps) {
        nextStep();
      } else {
        handleSubmit();
      }
    }
  };

  return (
    <main className="app-shell" onKeyDown={onKeyDown}>
      <div className="page wizard-page">
        <header className="wizard-header">
          <div>
            <p className="eyebrow">EventPilot</p>
            <h1>Build your celebration plan</h1>
          </div>
          <Button variant="secondary" type="button" onClick={fillSmartDefaults}>Use smart defaults</Button>
        </header>

        <ProgressBar value={(step + 1) / (totalSteps + 1) * 100} label="Wizard progress" />

        {step === 0 && (
          <section className="wizard-step stack">
            <h2>What are we celebrating?</h2>
            <div className="choice-grid">
              {EVENT_OPTIONS.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  className={`choice-card ${form.event_type === option.value ? 'selected' : ''}`}
                  onClick={() => handleField('event_type', option.value)}
                  aria-pressed={form.event_type === option.value}
                >
                  <strong>{option.label}</strong>
                  <span>{option.description}</span>
                </button>
              ))}
            </div>
          </section>
        )}

        {step === 1 && (
          <section className="wizard-step stack">
            <h2>When is the big day?</h2>
            <label>
              <span>Event date</span>
              <input
                type="date"
                value={form.target_date}
                onChange={(e) => handleField('target_date', e.target.value)}
              />
            </label>
          </section>
        )}

        {step === 2 && (
          <section className="wizard-step stack">
            <h2>How many people are attending?</h2>
            <input
              type="range"
              min={1}
              max={5000}
              value={form.guest_count}
              onChange={(e) => handleField('guest_count', Number(e.target.value))}
              aria-label="Guest count"
            />
            <label>
              <span>Guest count</span>
              <input
                type="number"
                min={1}
                max={5000}
                value={form.guest_count}
                onChange={(e) => handleField('guest_count', Number(e.target.value || 1))}
              />
            </label>
          </section>
        )}

        {step === 3 && (
          <section className="wizard-step stack">
            <h2>What’s the target budget?</h2>
            <div className="budget-row">
              <label>
                <span>Currency</span>
                <select
                  value={form.currency}
                  onChange={(e) => handleField('currency', e.target.value as 'INR' | 'USD' | 'EUR' | 'GBP' | 'AED')}
                >
                  <option value="USD">USD</option>
                  <option value="INR">INR</option>
                  <option value="EUR">EUR</option>
                  <option value="GBP">GBP</option>
                  <option value="AED">AED</option>
                </select>
              </label>
              <label>
                <span>Budget</span>
                <input
                  type="number"
                  min={1}
                  step="0.01"
                  value={form.total_budget}
                  onChange={(e) => handleField('total_budget', Number(e.target.value || 1))}
                />
              </label>
            </div>
          </section>
        )}

        {step === 4 && (
          <section className="wizard-step stack">
            <h2>Where will this happen?</h2>
            <label>
              <span>City or region</span>
              <input
                type="text"
                value={form.city}
                placeholder="Seattle, WA"
                onChange={(e) => handleField('city', e.target.value)}
              />
            </label>
          </section>
        )}

        {step === 5 && (
          <section className="wizard-step stack">
            <h2>Tell us the vibe and needs</h2>
            <label>
              <span>Style / theme</span>
              <input
                type="text"
                value={form.theme_style}
                placeholder="Warm Minimalist"
                onChange={(e) => handleField('theme_style', e.target.value)}
              />
            </label>
            <div className="chip-list">
              {THEME_CHOICES.map((choice) => (
                <button
                  key={choice}
                  type="button"
                  className={`chip ${form.theme_style === choice ? 'selected' : ''}`}
                  onClick={() => handleField('theme_style', choice)}
                >
                  {choice}
                </button>
              ))}
            </div>
            <label>
              <span>Must-haves and accessibility</span>
              <textarea
                value={form.special_requirements}
                placeholder="Wheelchair accessible, vegetarian options..."
                rows={4}
                onChange={(e) => handleField('special_requirements', e.target.value)}
              />
            </label>
            <div className="chip-list">
              {REQUIREMENT_CHOICES.map((choice) => (
                <button
                  key={choice}
                  type="button"
                  className={`chip ${String(form.special_requirements).includes(choice) ? 'selected' : ''}`}
                  onClick={() => {
                    const next = String(form.special_requirements || '').includes(choice)
                      ? String(form.special_requirements).replace(choice, '').replace(/,\s*,/g, ',').replace(/^,|,$/g, '').trim()
                      : [form.special_requirements, choice].filter(Boolean).join(', ');
                    handleField('special_requirements', next);
                  }}
                >
                  {choice}
                </button>
              ))}
            </div>
          </section>
        )}

        {step === totalSteps && (
          <section className="wizard-step stack">
            <h2>Final details</h2>
            <label>
              <span>Event title</span>
              <input
                type="text"
                value={form.title}
                placeholder="Sunset Wedding"
                onChange={(e) => handleField('title', e.target.value)}
              />
            </label>
            <div className="summary-box">
              <p><strong>{form.event_type}</strong> — {form.city || 'Your city'}</p>
              <p>{form.guest_count} guests · {form.currency} {form.total_budget}</p>
            </div>
          </section>
        )}

        {error && <div className="error-box" role="alert">{error}</div>}

        <div className="wizard-actions">
          <Button type="button" variant="secondary" onClick={() => setStep((current) => Math.max(0, current - 1))} disabled={step === 0}>
            Back
          </Button>
          {step < totalSteps ? (
            <Button type="button" disabled={!canNext} onClick={nextStep}>Next</Button>
          ) : (
            <Button type="button" disabled={isSubmitting} onClick={handleSubmit}>
              {isSubmitting ? 'Creating plan…' : 'Create plan'}
            </Button>
          )}
        </div>
      </div>
    </main>
  );
}
