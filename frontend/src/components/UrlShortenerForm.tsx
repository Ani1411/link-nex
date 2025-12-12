'use client'

import React, { JSX } from 'react';
import { URLResponse, FormData } from '../interfaces/url.interface';
import { useState } from 'react';
import { urlService } from '@/services/url.service';


export default function UrlShortenerForm(): JSX.Element {

  const [formData, setFormData] = useState<FormData>({
    originalUrl: '',
    customAlias: '',
    expiryDays: 30,
  });
  const [result, setResult] = useState<URLResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    setLoading(true);
    setError('')
    setResult(null)

    try {
      const response = await urlService.createShortUrl(formData);
      setResult(response);
    }
    catch (err:any) {
      if (err) {
        const errorMessage = typeof err.response?.data?.detail === 'string'
          ? err.response.data.detail
          : err.response?.data?.detail?.message || 'Failed to create short URL';
        setError(errorMessage);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setLoading(false);
    }
  }

  const copyToClipboard = async (text: string): Promise<void> => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const resetForm = (): void => {
    setResult(null);
    setFormData({ originalUrl: '', customAlias: '', expiryDays: 30 });
  };

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
                  className="text-blue-400 hover:text-blue-300 text-xs px-2 py-1 bg-blue-900/30 rounded"
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
        {error && (
          <div className="bg-red-900/30 border border-red-500/50 rounded-xl p-3">
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        )}
        <div className="relative">
          <label className="block text-xs sm:text-sm font-semibold text-gray-200 mb-2 sm:mb-3">
            URL to be shortened *
          </label>
          <input
            type="url"
            required
            value={formData.originalUrl}
            onChange={(e) => setFormData({ ...formData, originalUrl: e.target.value })}
            className="w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base border-2 border-slate-600 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-slate-700/50 hover:bg-slate-700 placeholder-gray-400 text-white"
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
            className="w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base border-2 border-slate-600 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-slate-700/50 hover:bg-slate-700 placeholder-gray-400 text-white"
            placeholder="my-awesome-link"
          />
        </div>

        <div className="relative">
          <label className="block text-xs sm:text-sm font-semibold text-gray-200 mb-2 sm:mb-3">
            Expiry (days)
          </label>
          <input
            type="number"
            defaultValue={30}
            min="1"
            max="365"
            value={formData.expiryDays}
            onChange={(e) => setFormData({ ...formData, expiryDays: parseInt(e.target.value) || 30 })}
            className="w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base border-2 border-slate-600 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-slate-700/50 hover:bg-slate-700 text-white"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-linear-to-r from-blue-600 to-purple-600 text-white py-3 sm:py-4 px-4 sm:px-6 text-sm sm:text-base md:text-lg rounded-xl sm:rounded-2xl hover:from-blue-700 hover:to-purple-700 transform hover:scale-[1.02] hover:-translate-y-1 transition-all duration-300 font-bold shadow-xl hover:shadow-2xl cursor-pointer"
        >
          {loading ? '⏳ Creating...' : '🚀 Create Magic Link'}
        </button>
      </form>
    </div>
  );
}