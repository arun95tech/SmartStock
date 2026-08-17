import apiClient from './client';

export interface StockLocation {
  id: string;
  name: string;
}

export async function getLocations(): Promise<StockLocation[]> {
  const response = await apiClient.get<StockLocation[]>('/inventory/locations/');
  return response.data;
}