import apiClient from './client';

export interface PurchaseOrder {
  id: string;
  status: string;
  order_date: string;
  expected_date: string;
  supplier: string;
}

export interface GoodsReceipt {
  id: string;
  po: string;
  received_date: string;
}

export interface GRLine {
  id: string;
  gr: string;
  po_line: string;
  qty_received: number;
  qc_status: string;
}

export interface QCHold {
  id: string;
  gr_line: string;
  hold_reason: string;
  state: string;
}

export async function getPurchaseOrders(): Promise<PurchaseOrder[]> {
  const response = await apiClient.get<PurchaseOrder[]>('/procurement/purchase-orders/');
  return response.data;
}

export async function getGoodsReceipts(): Promise<GoodsReceipt[]> {
  const response = await apiClient.get<GoodsReceipt[]>('/procurement/goods-receipts/');
  return response.data;
}

export async function getGRLines(): Promise<GRLine[]> {
  const response = await apiClient.get<GRLine[]>('/procurement/gr-lines/');
  return response.data;
}

export async function getQCHolds(): Promise<QCHold[]> {
  const response = await apiClient.get<QCHold[]>('/procurement/qc-holds/');
  return response.data;
}