(function () {
  function getCsrfToken() {
    const el = document.querySelector('meta[name="csrf-token"]');
    return el ? el.content : '';
  }

  const TOKEN = getCsrfToken();

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[method="post"]:not([data-no-csrf])')
      .forEach(form => {
        if (!form.querySelector('input[name="csrf_token"]')) {
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = 'csrf_token';
          input.value = TOKEN;
          form.prepend(input);
        }
      });
  });

  const _fetch = window.fetch;
  window.fetch = function (input, init = {}) {
    init.headers = new Headers(init.headers || {});
    const method = (init.method || 'GET').toUpperCase();
    if (/^(POST|PUT|PATCH|DELETE)$/.test(method) && !init.headers.has('X-CSRFToken')) {
      init.headers.set('X-CSRFToken', TOKEN);
    }
    return _fetch(input, init);
  };
})();
