export interface IConfig {
  eval_steps: number;
  training_steps: number;
  num_classes: number;
  batch_size: number;
  learning_rate: number;
  network_architecture: string;
  checkpoint_path?: string;
  width?: number;
  height?: number;
  name: string;
}
