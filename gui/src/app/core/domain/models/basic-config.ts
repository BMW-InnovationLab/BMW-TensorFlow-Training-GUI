export interface BasicConfig {
  num_classes: number;
  batch_size: number;
  learning_rate: number;
  checkpoint_name: string;
  width: number;
  height: number;
  network_architecture: string;
  training_steps: number;
  eval_steps: number;
  name: string;
  allow_growth: boolean;
}
