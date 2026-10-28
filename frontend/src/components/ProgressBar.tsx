interface ProgressBarProps {
  value: number;
  max?: number;
  label?: string;
}

export default function ProgressBar({ value, max = 100, label }: ProgressBarProps) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  return (
    <div aria-label={label || 'Progress'} className="progress">
      <div className="progress-bar" style={{ width: `${percentage}%` }} />
    </div>
  );
}
