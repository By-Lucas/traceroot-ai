export type Incident = {
  id: string;
  title: string;
  description: string;
  logs: string;
  stack_trace: string;
  repository_path: string | null;
  severity: string;
  status: string;
  created_at: string;
};

export type InvestigationListItem = {
  id: string;
  incident_id: string;
  incident_title: string;
  severity: string;
  status: string;
  confidence: number;
  root_cause: string | null;
  duration_ms: number;
  evidence_count: number;
  created_at: string;
};
