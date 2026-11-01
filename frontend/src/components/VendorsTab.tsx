import Button from './Button';
import Card from './Card';
import type { DashboardTabProps } from './dashboard_types';

export default function VendorsTab({
  vendors, onGenerateBrief,
}: DashboardTabProps) {
  return (
<div className="stack">
            {vendors.length ? vendors.map((vendor) => (
              <Card key={vendor.id ?? vendor.category} title={vendor.category}>
                <p>{vendor.name}</p>
                <p>{vendor.status}</p>
                <Button variant="secondary" onClick={() => onGenerateBrief(vendor)}>Generate brief</Button>
              </Card>
            )) : <Card title="Vendors"><p>No vendors yet.</p></Card>}
          </div>
  );
}
