import type { PropsWithChildren, ReactNode } from 'react';

interface CardProps extends PropsWithChildren {
  title?: string;
  action?: ReactNode;
  className?: string;
}

export default function Card({ title, action, className = '', children }: CardProps) {
  return (
    <section className={`card ${className}`.trim()}>
      {(title || action) && (
        <header className="card-header">
          {title && <h3>{title}</h3>}
          {action && <div>{action}</div>}
        </header>
      )}
      {children}
    </section>
  );
}
