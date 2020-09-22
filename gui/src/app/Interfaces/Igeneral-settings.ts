export interface IgeneralSettings {
  containerName: string;
  networkArchitecture: string;
  gPUs: string[];
  tensorBoard: number;
  APIPort: number;
  checkPoints ?: string;

}
