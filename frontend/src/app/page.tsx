import UrlShortenerForm from '../components/UrlShortenerForm';

export default function Home() {
  return (
    <div className="h-screen bg-linear-to-br from-gray-900 via-slate-800 to-gray-900">
      <nav className="h-16 sm:h-20 bg-slate-900/95 backdrop-blur-sm border-b border-slate-700/50 flex items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-linear-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">✂️</span>
          </div>
          <h1 className="text-white text-lg sm:text-xl font-bold">SnipUrl</h1>
        </div>
        <div className="text-gray-400 text-xs sm:text-sm hidden sm:block">
          Fast & Secure URL Shortening
        </div>
      </nav>
      
      {/* Main Content */}
      <div className="flex items-center justify-center px-4 sm:px-6 lg:px-8" style={{height: 'calc(100vh - 80px)'}}>
        <UrlShortenerForm />
      </div>
    </div>
  );
}
