function createNavbar(currentPath = '') {
  const navItems = [
    { href: '/', label: 'Beranda', path: '/', icon: '🏠' },
    { href: '/analytic', label: 'Analisis', path: '/analytic', icon: '📊' },
    { href: '/title', label: 'Title', path: '/title', icon: '🏆' },
    { href: '/trending', label: 'Trending', path: '/trending', icon: '🔥' },
    { href: '/search', label: 'Searching', path: '/search', icon: '🔍' }
  ];

  const navLinks = navItems.map(item => {
    const isActive = currentPath === item.path;
    const activeClass = isActive ? 
      'bg-gradient-to-r from-sky-500 to-cyan-500 text-white shadow-lg shadow-sky-500/50 scale-105' : 
      'text-gray-300 hover:text-white hover:bg-slate-700/80 hover:shadow-md hover:shadow-sky-500/30 hover:scale-105';
    
    return `
      <a href="${item.href}" class="${activeClass} px-4 py-2 rounded-xl font-medium transition-all duration-300 ease-out flex items-center gap-2 backdrop-blur-sm">
        <span class="text-sm">${item.icon}</span>
        <span class="hidden sm:inline">${item.label}</span>
      </a>
    `;
  }).join('');

  return `
    <header class="bg-slate-900/95 backdrop-blur-md shadow-2xl shadow-slate-900/50 sticky top-0 z-50 border-b border-slate-700/50">
      <div class="max-w-7xl mx-auto px-4 py-3">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-sky-400 via-cyan-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-sky-500/30">
              <span class="text-white font-bold text-lg">🎮</span>
            </div>
            <div class="text-xl font-bold bg-gradient-to-r from-sky-400 via-cyan-400 to-blue-400 bg-clip-text text-transparent">
              GameTrend
            </div>
          </div>

          <nav class="flex items-center gap-2">
            ${navLinks}
          </nav>

          <button class="md:hidden p-2 rounded-lg bg-slate-800 text-gray-300 hover:text-white hover:bg-slate-700 transition-colors duration-200">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
        </div>
      </div>

      <div class="absolute inset-x-0 -bottom-px h-px bg-gradient-to-r from-transparent via-sky-500/50 to-transparent"></div>
    </header>
  `;
}

function injectNavbar(currentPath = '') {
  document.addEventListener('DOMContentLoaded', function() {
    const navbarContainer = document.getElementById('navbar-container');
    if (navbarContainer) {
      navbarContainer.innerHTML = createNavbar(currentPath);
    } else {
      const navbar = createNavbar(currentPath);
      document.body.insertAdjacentHTML('afterbegin', navbar);
    }
  });
}

function autoInjectNavbar() {
  const currentPath = window.location.pathname;
  injectNavbar(currentPath);
}

function toggleMobileMenu() {
  document.addEventListener('DOMContentLoaded', function() {
    const mobileButton = document.querySelector('[data-mobile-menu]');
    const mobileMenu = document.querySelector('[data-mobile-nav]');
    
    if (mobileButton && mobileMenu) {
      mobileButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
        mobileMenu.classList.toggle('animate-fadeIn');
      });
    }
  });
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { createNavbar, injectNavbar, autoInjectNavbar, toggleMobileMenu };
}