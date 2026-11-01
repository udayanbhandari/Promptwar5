import { useEffect, useMemo, useState, type KeyboardEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import Button from '../components/Button';
import ProgressBar from '../components/ProgressBar';
import WizardSteps, { type WizardForm } from '../components/WizardSteps';
import type { EventType } from '../types';

const STORAGE_KEY = 'eventpilot-wizard-draft';
const TOTAL_STEPS = 6;

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

const SMART_DEFAULTS: Record<EventType, Partial<WizardForm>> = {
  wedding: { title: 'Wedding Weekend', guest_count: 120, total_budget: 28000, currency: 'USD', city: 'Seattle, WA', theme_style: 'Warm Minimalist', special_requirements: 'Wheelchair accessible' },
  birthday: { title: 'Birthday Bash', guest_count: 35, total_budget: 2200, currency: 'USD', city: 'Austin, TX', theme_style: 'Retro Arcade', special_requirements: 'Gluten-free' },
  community: { title: 'Community Fair', guest_count: 250, total_budget: 6000, currency: 'USD', city: 'Denver, CO', theme_style: 'Eco Fair', special_requirements: 'Wheelchair accessible' },
};

function useWizardDraft(setForm: (form: WizardForm) => void, form: WizardForm) {
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return;
    try {
      setForm({ ...defaultForm, ...(JSON.parse(saved) as Partial<WizardForm>) });
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, [setForm]);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(form));
  }, [form]);
}

// The wizard owns the sequential form flow and submission transaction.
// eslint-disable-next-line max-lines-per-function
export default function WizardPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState<WizardForm>(defaultForm);
  const [step, setStep] = useState(0);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  useWizardDraft(setForm, form);

  const canNext = useMemo(() => {
    const checks = [
      Boolean(form.event_type),
      Boolean(form.target_date),
      form.guest_count > 0,
      form.total_budget > 0,
      form.city.length > 1,
      Boolean(form.theme_style || form.special_requirements),
    ];
    return checks[step] ?? true;
  }, [form, step]);

  const handleField = <K extends keyof WizardForm>(field: K, value: WizardForm[K]) => {
    setForm((previous) => ({ ...previous, [field]: value }));
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
    if (validateStep() && step < TOTAL_STEPS) setStep((current) => current + 1);
  };

  const handleSubmit = async () => {
    if (!form.title.trim()) {
      setError('Please add a short event title.');
      return;
    }
    setIsSubmitting(true);
    setError('');
    try {
      const created = await api.createEvent(form);
      await api.generatePlan(created.id);
      localStorage.removeItem(STORAGE_KEY);
      navigate(`/plan/${created.id}`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Unable to create your plan.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const onKeyDown = (event: KeyboardEvent) => {
    if (event.key !== 'Enter' || isSubmitting) return;
    if (step < TOTAL_STEPS) nextStep();
    else void handleSubmit();
  };

  return (
    <main className="app-shell" onKeyDown={onKeyDown}>
      <div className="page wizard-page">
        <header className="wizard-header">
          <div>
            <p className="eyebrow">EventPilot</p>
            <h1>Build your celebration plan</h1>
          </div>
          <Button variant="secondary" type="button" onClick={() => setForm((previous) => ({ ...previous, ...SMART_DEFAULTS[form.event_type] }))}>
            Use smart defaults
          </Button>
        </header>
        <ProgressBar value={(step + 1) / (TOTAL_STEPS + 1) * 100} label="Wizard progress" />
        <WizardSteps step={step} totalSteps={TOTAL_STEPS} form={form} onFieldChange={handleField} />
        {error && <div className="error-box" role="alert">{error}</div>}
        <div className="wizard-actions">
          <Button type="button" variant="secondary" onClick={() => setStep((current) => Math.max(0, current - 1))} disabled={step === 0}>
            Back
          </Button>
          {step < TOTAL_STEPS ? (
            <Button type="button" disabled={!canNext} onClick={nextStep}>Next</Button>
          ) : (
            <Button type="button" disabled={isSubmitting} onClick={() => void handleSubmit()}>
              {isSubmitting ? 'Creating plan…' : 'Create plan'}
            </Button>
          )}
        </div>
      </div>
    </main>
  );
}
