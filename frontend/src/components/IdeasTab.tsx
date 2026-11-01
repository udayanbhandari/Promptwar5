import Button from './Button';
import Card from './Card';
import type { DashboardTabProps } from './dashboard_types';

export default function IdeasTab({
  ideas,
}: DashboardTabProps) {
  return (
<div className="stack">
            {ideas.length ? ideas.map((idea) => (
              <Card key={`${idea.aspect}-${idea.title}`} title={idea.title}>
                <p>{idea.description}</p>
                <div className="row">
                  <Button variant="secondary">Skip</Button>
                  <Button>Save</Button>
                </div>
              </Card>
            )) : <Card title="Ideas"><p>No ideas yet.</p></Card>}
          </div>
  );
}
