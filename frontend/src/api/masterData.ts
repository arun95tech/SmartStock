import apiClient from './client';

export interface Item {
  id: string;
  sku: string;
  name: string;
  reorder_point: number;
  safety_stock: number;
}

export async function getItems(): Promise<Item[]> {
  const response = await apiClient.get<Item[]>('/master-data/items/');
  return response.data;
}