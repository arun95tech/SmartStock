import apiClient from './client';

export interface ReorderRecommendation {
  id: string;
  item: string;
  current_stock: number;
  reorder_point: number;
  recommended_qty: number;
  reason: string;
  status: string;
}

export async function checkReorder(itemId: string, locationId: string): Promise<ReorderRecommendation | null> {
  const response = await apiClient.post('/planning/recommendations/check/', {
    item_id: itemId,
    location_id: locationId,
  });
  if (response.data.recommendation === null) {
    return null;
  }
  return response.data;
}