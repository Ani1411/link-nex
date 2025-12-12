export interface URLResponse {
    short_url: string;
    original_url: string;
    expires_at: string | null;
}
    
export interface URLCreateRequest {
    originalUrl: string;
    customAlias?: string;
    expiryDays: number;
}

export interface FormData {
    originalUrl: string;
    customAlias: string;
    expiryDays: number;
}