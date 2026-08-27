import type { Lead, LeadPayload } from '../types/api'
import { apiFetch } from './client'

export function createLead(payload: LeadPayload) {
  return apiFetch<Lead>('/api/v1/leads', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
