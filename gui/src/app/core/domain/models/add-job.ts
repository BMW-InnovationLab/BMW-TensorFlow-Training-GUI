export interface AddJob {
  name: string;
  author: string;
  network_architecture: string;
  dataset_path: string;
  gpus: number[];
  tensorboard_port: number;
  api_port: number;
}
