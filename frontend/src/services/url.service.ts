import { api } from './api.service';
import { URLCreateRequest, URLResponse } from '../interfaces/url.interface'

export const urlService = {
    createShortUrl: async (data: URLCreateRequest): Promise<URLResponse> => {
        const response = await api.post<URLResponse>('/urls/create', {
            original_url: data.originalUrl,
            custom_alias: data.customAlias || null,
            expires_in_days: data.expiryDays,
        });
        return response.data
    }
}