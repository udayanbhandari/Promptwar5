import type { CurrencyCode, EventType } from '../types';

export type WizardForm = {
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

type WizardStepsProps = {
  step: number;
  totalSteps: number;
  form: WizardForm;
  onFieldChange: <K extends keyof WizardForm>(field: K, value: WizardForm[K]) => void;
};

const EVENT_OPTIONS = [
  { value: 'wedding' as const, label: 'Wedding', description: 'Celebrate a milestone day' },
  { value: 'birthday' as const, label: 'Birthday', description: 'A fun personal moment' },
  { value: 'community' as const, label: 'Community', description: 'A shared gathering' },
];
const THEME_CHOICES = ['Warm Minimalist', 'Retro Arcade', 'Eco Fair', 'Modern Luxury', 'Garden Glow'];
const REQUIREMENT_CHOICES = ['Wheelchair accessible', 'Vegetarian options', 'Gluten-free', 'Quiet room', 'Stage access'];

function updateRequirements(current: string, choice: string): string {
  if (current.includes(choice)) return current.replace(choice, '').replace(/,\s*,/g, ',').replace(/^,|,$/g, '').trim();
  return [current, choice].filter(Boolean).join(', ');
}

type StepProps = Pick<WizardStepsProps, 'form' | 'onFieldChange'>;

function EventTypeStep({ form, onFieldChange }: StepProps) {
  return <section className="wizard-step stack"><h2>What are we celebrating?</h2><div className="choice-grid">
    {EVENT_OPTIONS.map((option) => <button key={option.value} type="button" className={`choice-card ${form.event_type === option.value ? 'selected' : ''}`} onClick={() => onFieldChange('event_type', option.value)} aria-pressed={form.event_type === option.value}><strong>{option.label}</strong><span>{option.description}</span></button>)}
  </div></section>;
}

function DateStep({ form, onFieldChange }: StepProps) {
  return <section className="wizard-step stack"><h2>When is the big day?</h2><label><span>Event date</span><input type="date" value={form.target_date} onChange={(event) => onFieldChange('target_date', event.target.value)} /></label></section>;
}

function GuestStep({ form, onFieldChange }: StepProps) {
  return <section className="wizard-step stack"><h2>How many people are attending?</h2><input type="range" min={1} max={5000} value={form.guest_count} onChange={(event) => onFieldChange('guest_count', Number(event.target.value))} aria-label="Guest count" /><label><span>Guest count</span><input type="number" min={1} max={5000} value={form.guest_count} onChange={(event) => onFieldChange('guest_count', Number(event.target.value || 1))} /></label></section>;
}

function BudgetStep({ form, onFieldChange }: StepProps) {
  return <section className="wizard-step stack"><h2>What’s the target budget?</h2><div className="budget-row"><label><span>Currency</span><select value={form.currency} onChange={(event) => onFieldChange('currency', event.target.value as CurrencyCode)}><option value="USD">USD</option><option value="INR">INR</option><option value="EUR">EUR</option><option value="GBP">GBP</option><option value="AED">AED</option></select></label><label><span>Budget</span><input type="number" min={1} step="0.01" value={form.total_budget} onChange={(event) => onFieldChange('total_budget', Number(event.target.value || 1))} /></label></div></section>;
}

function LocationStep({ form, onFieldChange }: StepProps) {
  return <section className="wizard-step stack"><h2>Where will this happen?</h2><label><span>City or region</span><input type="text" value={form.city} placeholder="Seattle, WA" onChange={(event) => onFieldChange('city', event.target.value)} /></label></section>;
}

function DetailsStep({ form, onFieldChange }: StepProps) {
  return <section className="wizard-step stack"><h2>Tell us the vibe and needs</h2><label><span>Style / theme</span><input type="text" value={form.theme_style} placeholder="Warm Minimalist" onChange={(event) => onFieldChange('theme_style', event.target.value)} /></label><div className="chip-list">{THEME_CHOICES.map((choice) => <button key={choice} type="button" className={`chip ${form.theme_style === choice ? 'selected' : ''}`} onClick={() => onFieldChange('theme_style', choice)}>{choice}</button>)}</div><label><span>Must-haves and accessibility</span><textarea value={form.special_requirements} placeholder="Wheelchair accessible, vegetarian options..." rows={4} onChange={(event) => onFieldChange('special_requirements', event.target.value)} /></label><div className="chip-list">{REQUIREMENT_CHOICES.map((choice) => <button key={choice} type="button" className={`chip ${form.special_requirements.includes(choice) ? 'selected' : ''}`} onClick={() => onFieldChange('special_requirements', updateRequirements(form.special_requirements, choice))}>{choice}</button>)}</div></section>;
}

function FinalStep({ form, onFieldChange }: StepProps) {
  return <section className="wizard-step stack"><h2>Final details</h2><label><span>Event title</span><input type="text" value={form.title} placeholder="Sunset Wedding" onChange={(event) => onFieldChange('title', event.target.value)} /></label><div className="summary-box"><p><strong>{form.event_type}</strong> — {form.city || 'Your city'}</p><p>{form.guest_count} guests · {form.currency} {form.total_budget}</p></div></section>;
}

export default function WizardSteps({ step, totalSteps, form, onFieldChange }: WizardStepsProps) {
  const props = { form, onFieldChange };
  if (step === 0) return <EventTypeStep {...props} />;
  if (step === 1) return <DateStep {...props} />;
  if (step === 2) return <GuestStep {...props} />;
  if (step === 3) return <BudgetStep {...props} />;
  if (step === 4) return <LocationStep {...props} />;
  if (step === 5) return <DetailsStep {...props} />;
  if (step === totalSteps) return <FinalStep {...props} />;
  return null;
}
