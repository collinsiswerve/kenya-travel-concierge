(() => {
  'use strict';
  const serviceTrigger = document.querySelector('.nav-service-trigger');
  const serviceMenu = document.querySelector('#service-menu');
  const mobileToggle = document.querySelector('.menu-toggle');
  const mobileMenu = document.querySelector('#mobile-menu');
  const closeServiceMenu = () => {
    serviceTrigger?.setAttribute('aria-expanded', 'false');
    if (serviceMenu) serviceMenu.hidden = true;
  };
  const closeMobileMenu = () => {
    mobileToggle?.setAttribute('aria-expanded', 'false');
    mobileToggle?.setAttribute('aria-label', 'Open navigation');
    if (mobileMenu) mobileMenu.hidden = true;
  };
  serviceTrigger?.addEventListener('click', () => {
    const open = serviceTrigger.getAttribute('aria-expanded') !== 'true';
    serviceTrigger.setAttribute('aria-expanded', String(open));
    serviceMenu.hidden = !open;
  });
  mobileToggle?.addEventListener('click', () => {
    const open = mobileToggle.getAttribute('aria-expanded') !== 'true';
    mobileToggle.setAttribute('aria-expanded', String(open));
    mobileToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    mobileMenu.hidden = !open;
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.nav-dropdown')) closeServiceMenu();
    if (!event.target.closest('.site-header')) closeMobileMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      if (serviceTrigger?.getAttribute('aria-expanded') === 'true') {
        closeServiceMenu();
        serviceTrigger.focus();
      }
      if (mobileToggle?.getAttribute('aria-expanded') === 'true') {
        closeMobileMenu();
        mobileToggle.focus();
      }
    }
  });
  mobileMenu?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMobileMenu));
  window.matchMedia('(max-width: 900px)').addEventListener('change', () => {
    closeServiceMenu();
    closeMobileMenu();
  });
  const tabs = [...document.querySelectorAll('.finder-tabs [role="tab"]')];
  const activateTab = (tab) => {
    tabs.forEach((item) => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activateTab(tab));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
      if (event.key === 'ArrowLeft') next = tabs[(index + tabs.length - 1) % tabs.length];
      if (event.key === 'Home') next = tabs[0];
      if (event.key === 'End') next = tabs[tabs.length - 1];
      if (next) {
        event.preventDefault();
        activateTab(next);
        next.focus();
      }
    });
  });
  const filters = [...document.querySelectorAll('[data-filter]')];
  const serviceCards = [...document.querySelectorAll('[data-category]')];
  const applyFilter = (category, updateUrl = false) => {
    const known = filters.some((button) => button.dataset.filter === category);
    if (!known) category = 'all';
    filters.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    let count = 0;
    serviceCards.forEach((card) => {
      card.hidden = category !== 'all' && card.dataset.category !== category;
      if (!card.hidden) count += 1;
    });
    const status = document.querySelector('.filter-status');
    if (status) status.textContent = `Showing ${count} ${category === 'all' ? '' : filters.find(b => b.dataset.filter === category).textContent.replace(/\d+/g, '').trim() + ' '}services`;
    if (updateUrl) {
      const url = new URL(window.location.href);
      category === 'all' ? url.searchParams.delete('category') : url.searchParams.set('category', category);
      window.history.replaceState(null, '', url);
    }
  };
  if (filters.length) {
    applyFilter(new URLSearchParams(window.location.search).get('category') || 'all');
    filters.forEach((button) => button.addEventListener('click', () => applyFilter(button.dataset.filter, true)));
    window.addEventListener('popstate', () => applyFilter(new URLSearchParams(window.location.search).get('category') || 'all'));
  }
  const enquiry = document.querySelector('#enquiry-form');
  if (enquiry) {
    const selected = new URLSearchParams(window.location.search).get('service');
    const service = enquiry.elements.namedItem('service');
    if ([...service.options].some((option) => option.value === selected)) service.value = selected;
    enquiry.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!enquiry.reportValidity()) return;
      const data = new FormData(enquiry);
      const label = service.selectedOptions[0].textContent;
      const message = [
        'Hello Kenya Travel Concierge,', '',
        `I would like to enquire about: ${label}.`, '',
        `Name: ${String(data.get('name')).trim()}`,
        `Email: ${String(data.get('email')).trim()}`,
        data.get('phone') ? `Phone: ${String(data.get('phone')).trim()}` : '',
        data.get('timing') ? `Timing: ${String(data.get('timing')).trim()}` : '',
        '', String(data.get('message')).trim()
      ].filter((line) => line !== undefined).join('\n').replace(/\n{3,}/g, '\n\n');
      const viaEmail = event.submitter?.value === 'email';
      const target = viaEmail
        ? `mailto:info.kenyatravelconcierge@gmail.com?subject=${encodeURIComponent('KTC enquiry — ' + label)}&body=${encodeURIComponent(message)}`
        : `https://wa.me/254717762323?text=${encodeURIComponent(message)}`;
      const result = document.querySelector('#enquiry-result');
      result.replaceChildren();
      const status = document.createElement('p');
      status.textContent = 'Your enquiry is ready to review and send.';
      const fallback = document.createElement('a');
      fallback.href = target;
      fallback.textContent = viaEmail ? 'Open your prepared email enquiry' : 'Open your prepared WhatsApp enquiry';
      if (!viaEmail) { fallback.target = '_blank'; fallback.rel = 'noopener noreferrer'; }
      result.append(status, fallback);
      result.hidden = false;
      if (viaEmail) window.location.href = target;
      else window.open(target, '_blank', 'noopener,noreferrer');
    });
  }
})();
