(function(){
  // Backdrop-filter support check for graceful fallback
  try{
    if(!(CSS && CSS.supports && (CSS.supports('backdrop-filter','blur(2px)') || CSS.supports('-webkit-backdrop-filter','blur(2px)')))){
      document.documentElement.classList.add('no-backdrop');
    }
  }catch(e){
    document.documentElement.classList.add('no-backdrop');
  }

  const toggleBtn = document.getElementById('nav-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const iconHamburger = document.getElementById('icon-hamburger');
  const iconClose = document.getElementById('icon-close');

  if(!toggleBtn || !mobileMenu) return;

  let open = false;
  const setOpen = (next) => {
    open = next;
    toggleBtn.setAttribute('aria-expanded', String(open));
    if(open){
      mobileMenu.classList.remove('hidden');
      mobileMenu.classList.add('animate-fade-slide');
      if(iconHamburger) iconHamburger.classList.add('hidden');
      if(iconClose) iconClose.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
    }else{
      mobileMenu.classList.add('hidden');
      if(iconHamburger) iconHamburger.classList.remove('hidden');
      if(iconClose) iconClose.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    }
  };

  toggleBtn.addEventListener('click', () => setOpen(!open));

  // Close on link click
  mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setOpen(false)));

  // Close on ESC
  window.addEventListener('keydown', (e) => {
    if(e.key === 'Escape' && open){ setOpen(false); }
  });

  // Close when clicking outside
  document.addEventListener('click', (e) => {
    if(!open) return;
    if(!mobileMenu.contains(e.target) && !toggleBtn.contains(e.target)){
      setOpen(false);
    }
  });
})();