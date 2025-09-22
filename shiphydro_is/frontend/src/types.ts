export interface GeometryParam {
  name: string;
  lpp: number;
  beam: number;
  depth: number;
  draft: number;
  cb: number;
  bulbous_bow_length: number;
  bulbous_bow_radius: number;
  sections?: number[][];
}

export interface FluidProperties {
  density: number;
  viscosity: number;
}

export interface CaseSpec {
  geometry_id: string;
  speed: number;
  draft: number;
  froude_number: number;
  reynolds_number: number;
  fluid: FluidProperties;
  turbulence_model: string;
  solver_options: Record<string, unknown>;
}

export interface RunRequest {
  geometry: GeometryParam;
  case: CaseSpec;
  use_mock?: boolean;
}

export interface RunStatus {
  job_id: string;
  state: string;
  progress: number;
  stage?: string;
  solver_used: string;
  created_at: string;
  updated_at: string;
  message?: string;
}

export interface MetricPoint {
  timestamp: string;
  residual: number;
}

export interface RunMetrics {
  job_id: string;
  resistance_total: number;
  resistance_coefficient: number;
  residuals: MetricPoint[];
  timestamps: string[];
}

export interface DriverDryRun {
  commands: string[];
  scripts: string[];
  env: string[];
}
