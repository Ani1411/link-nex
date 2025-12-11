export default function UrlShortenerForm() {
  return (
    <div className="bg-slate-800/90 backdrop-blur-md p-4 sm:p-6 md:p-8 lg:p-10 rounded-2xl sm:rounded-3xl shadow-2xl w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg mx-4 border border-slate-700/50">
      <div className="text-center mb-6 sm:mb-8">
        <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white mb-2">
          Shorten Your URL
        </h2>
        <p className="text-gray-300 text-xs sm:text-sm">Create short, shareable links in seconds</p>
      </div>
      
      <form className="space-y-4 sm:space-y-6">
        <div className="relative">
          <label className="block text-xs sm:text-sm font-semibold text-gray-200 mb-2 sm:mb-3">
            URL to be shortened *
          </label>
          <input 
            type="url" 
            required
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
            className="w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base border-2 border-slate-600 rounded-xl sm:rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-slate-700/50 hover:bg-slate-700 text-white"
          />
        </div>
        
        <button 
          type="submit"
          className="w-full bg-linear-to-r from-blue-600 to-purple-600 text-white py-3 sm:py-4 px-4 sm:px-6 text-sm sm:text-base md:text-lg rounded-xl sm:rounded-2xl hover:from-blue-700 hover:to-purple-700 transform hover:scale-[1.02] hover:-translate-y-1 transition-all duration-300 font-bold shadow-xl hover:shadow-2xl cursor-pointer"
        >
          🚀 Create Magic Link
        </button>
      </form>
    </div>
  );
}