CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    service TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    summary TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO incidents (id, title, service, severity, status, summary)
VALUES
  ('INC-2048', 'Checkout API latency elevated', 'checkout', 'SEV-2', 'investigating',
   'p95 latency increased after the latest checkout-api release.'),
  ('INC-2047', 'Image processing queue delayed', 'media-worker', 'SEV-3', 'monitoring',
   'Queue depth briefly exceeded the warning threshold.')
ON CONFLICT (id) DO NOTHING;
