'use client'

import React, { JSX, useCallback, useMemo, useTransition } from 'react';
import { URLResponse, FormData } from '../interfaces/url.interface';
import { useState } from 'react';
import { urlService } from '@/services/url.service';

import toast from 'react-hot-toast';


export default function UrlShortenerForm(): JSX.Element {
  const [isPending, startTransition] = useTransition();
  const [formData, setFormData] = useState<FormData>({
    originalUrl: '',
    customAlias: '',
    expiryDays: 30,
  });
  const [result, setResult] = useState<URLResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [fieldErrors, setFieldErrors] = useState<{ [key: string]: boolean }>({});

  const isValidUrl = useMemo(() => {
    try {
      return formData.originalUrl ? new URL(formData.originalUrl) : false;
    } catch {
      return false;
    }
  }, [formData.originalUrl]);

  const handleSubmit = useCallback((e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();

    if (!isValidUrl) {
      toast.error('Please enter a valid URL');
      setFieldErrors({ originalUrl: true });
      return;
    }

    startTransition(async () => {
      setError('');
      setResult(null);
      setFieldErrors({});

      try {
        const response = await urlService.createShortUrl(formData);
        setResult(response);
        toast.success('Short URL created successfully!');
      } catch (err: any) {
        const errorMessage = typeof err.response?.data?.detail === 'string'
          ? err.response.data.detail
          : err.response?.data?.detail?.message || 'Failed to create short URL';
        setError(errorMessage);
        toast.error(errorMessage);

        // Highlight fields based on error type
        const errors: { [key: string]: boolean } = {};
        if (errorMessage.toLowerCase().includes('url') || errorMessage.toLowerCase().includes('invalid')) {
          errors.originalUrl = true;
        }
        if (errorMessage.toLowerCase().includes('alias') || errorMessage.toLowerCase().includes('custom')) {
          errors.customAlias = true;
        }
        if (errorMessage.toLowerCase().includes('expir') || errorMessage.toLowerCase().includes('day')) {
          errors.expiryDays = true;
        }
        setFieldErrors(errors);
      }
    });
  }, [formData, isValidUrl]);

  const copyToClipboard = useCallback(async (text: string): Promise<void> => {
    try {
      await navigator.clipboard.writeText(text);
      toast.success('Copied to clipboard! 📋');
    } catch {
      toast.error('Failed to copy to clipboard');
    }
  }, []);

  const resetForm = useCallback((): void => {
    setResult(null);
    setFormData({ originalUrl: '', customAlias: '', expiryDays: 30 });
    setError('');
    setFieldErrors({});
  }, []);

  if (result) {
    return (
      <div className="bg-slate-800/90 backdrop-blur-md p-4 sm:p-6 md:p-8 lg:p-10 rounded-2xl sm:rounded-3xl shadow-2xl w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg mx-4 border border-slate-700/50">
        <div className="space-y-4">
          <div className="bg-green-900/30 border border-green-500/50 rounded-xl p-4">
            <h3 className="text-green-400 font-semibold mb-2">✅ URL Created Successfully!</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between bg-slate-700/50 rounded-lg p-3">
                <span className="text-white text-sm truncate mr-2">{result.short_url}</span>
                <button
                  onClick={() => copyToClipboard(result.short_url)}
                  className="text-blue-400 hover:text-blue-300 text-xs px-2 py-1 bg-blue-900/30 rounded cursor-pointer"
                >
                  Copy
                </button>
              </div>
              {result.expires_at && (
                <p className="text-gray-400 text-xs">
                  Expires: {new Date(result.expires_at).toLocaleDateString()}
                </p>
              )}
            </div>
          </div>
          <button
            onClick={resetForm}
            className="w-full bg-slate-600 hover:bg-slate-500 text-white py-2 px-4 rounded-xl transition-colors"
          >
            Create Another
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/90 backdrop-blur-md p-4 sm:p-6 md:p-8 lg:p-10 rounded-2xl sm:rounded-3xl shadow-2xl w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg mx-4 border border-slate-700/50">
      <div className="text-center mb-6 sm:mb-8">
        <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white mb-2">
          Shorten Your URL
        </h2>
        <p className="text-gray-300 text-xs sm:text-sm">Create short, shareable links in seconds</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
        <div className="relative">
          <label className="block text-xs sm:text-sm font-semibold text-gray-200 mb-2 sm:mb-3">
            URL to be shortened *
          </label>
          <input
            type="url"
            required
            value={formData.originalUrl}
            onChange={(e) => setFormData({ ...formData, originalUrl: e.target.value })}
            className={`w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base border-2 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 transition-all duration-300 bg-slate-700/50 hover:bg-slate-700 placeholder-gray-400 text-white ${fieldErrors.originalUrl
              ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
              : 'border-slate-600 focus:ring-blue-500 focus:border-transparent'
              }`}
            placeholder="https://your-long-url.com/path"
          />
        </div>

        <div className="relative">
          <label className="block text-xs sm:text-sm font-semibold text-gray-200 mb-2 sm:mb-3">
            Custom alias (optional)
          </label>
          <input
            type="text"
            value={formData.customAlias}
            onChange={(e) => setFormData({ ...formData, customAlias: e.target.value })}
            className={`w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base border-2 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 transition-all duration-300 bg-slate-700/50 hover:bg-slate-700 placeholder-gray-400 text-white ${fieldErrors.customAlias
              ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
              : 'border-slate-600 focus:ring-blue-500 focus:border-transparent'
              }`}
            placeholder="my-awesome-link"
          />
        </div>

        <div className="relative">
          <label className="block text-xs sm:text-sm font-semibold text-gray-200 mb-2 sm:mb-3">
            Expiry (days)
          </label>
          <input
            type="number"
            min="1"
            max="365"
            value={formData.expiryDays}
            onChange={(e) => setFormData({ ...formData, expiryDays: parseInt(e.target.value) || 30 })}
            className={`w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base border-2 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 transition-all duration-300 bg-slate-700/50 hover:bg-slate-700 text-white ${fieldErrors.expiryDays
              ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
              : 'border-slate-600 focus:ring-blue-500 focus:border-transparent'
              }`}
          />
        </div>

        <button
          type="submit"
          disabled={isPending || !isValidUrl}
          className="w-full bg-linear-to-r from-blue-600 to-purple-600 text-white py-3 sm:py-4 px-4 sm:px-6 text-sm sm:text-base md:text-lg rounded-xl sm:rounded-2xl hover:from-blue-700 hover:to-purple-700 transform hover:scale-[1.02] hover:-translate-y-1 transition-all duration-300 font-bold shadow-xl hover:shadow-2xl cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          {isPending ? '⏳ Creating...' : '🚀 Create Magic Link'}
        </button>
      </form>
    </div>
  );
}