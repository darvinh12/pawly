(function () {
  // Validación de formularios
  function isEmpty(field) {
    if (field.type === 'checkbox' || field.type === 'radio') return !field.checked;
    return field.value.trim() === '';
  }

  function setError(form, field, message) {
    const box = form.querySelector('[data-error-for="' + field.id + '"]');
    field.setAttribute('aria-invalid', message ? 'true' : 'false');
    if (box) {
      box.textContent = message;
      box.hidden = !message;
    }
  }

  function validate(form) {
    let firstInvalid = null;
    form.querySelectorAll('[required]').forEach(function (field) {
      const inUse = !field.disabled && !field.closest('[hidden]');
      const message = inUse && isEmpty(field) ? field.dataset.error : '';
      setError(form, field, message);
      if (message && !firstInvalid) firstInvalid = field;
    });
    if (firstInvalid) firstInvalid.focus();
    return firstInvalid === null;
  }

  function enableValidation(form) {
    form.addEventListener('submit', function (event) {
      // Si falta un campo no se envía
      if (!validate(form)) {
        event.preventDefault();
        return;
      }
      // Con data-next pasa a la siguiente pantalla
      if (form.dataset.next) {
        event.preventDefault();
        window.location.href = form.dataset.next;
      }
    });
  }

  // Mostrar u ocultar la contraseña
  function enablePasswordToggle(button) {
    button.addEventListener('click', function () {
      const input = document.getElementById(button.dataset.togglePassword);
      const show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      button.setAttribute('aria-pressed', String(show));
    });
  }

  document.querySelectorAll('form[data-validate]').forEach(enableValidation);
  document.querySelectorAll('[data-toggle-password]').forEach(enablePasswordToggle);

  // Confirmaciones y botones que se activan
  document.addEventListener('click', function (event) {
    const confirmTrigger = event.target.closest('[data-confirm]');
    if (confirmTrigger && confirmTrigger.tagName !== 'INPUT') {
      if (!window.confirm(confirmTrigger.dataset.confirm)) {
        event.preventDefault();
        return;
      }
      if (confirmTrigger.tagName === 'BUTTON' && confirmTrigger.dataset.next) {
        window.location.href = confirmTrigger.dataset.next;
      }
      return;
    }

    // El botón de la contraseña ya tiene su propio evento
    if (event.target.closest('[data-toggle-password]')) return;

    const pressable = event.target.closest('button[aria-pressed]');
    if (pressable) {
      const pressed = pressable.getAttribute('aria-pressed') === 'true';
      pressable.setAttribute('aria-pressed', String(!pressed));
    }
  });

  // Formularios que se envían solos al cambiar una opción
  document.querySelectorAll('form[data-autosubmit]').forEach(function (form) {
    form.addEventListener('change', function () {
      form.submit();
    });
  });

  // Interruptores que muestran u ocultan un bloque
  document.querySelectorAll('input[data-reveals]').forEach(function (input) {
    const target = document.getElementById(input.dataset.reveals);

    function sync() {
      if (target) target.hidden = !input.checked;
    }

    input.addEventListener('change', function () {
      if (!input.checked && input.dataset.confirmOff && !window.confirm(input.dataset.confirmOff)) {
        input.checked = true;
      }
      sync();
    });
    sync();
  });

  // Cerrar las ventanas con Escape o con un clic en el fondo
  const closeLink = document.querySelector('a[data-close]');
  if (closeLink) {
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') window.location.href = closeLink.href;
    });
    const backdrop = document.querySelector('.overlay-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', function () {
        window.location.href = closeLink.href;
      });
    }
  }

  // Mostrar u ocultar según la dirección de la página
  const params = new URLSearchParams(window.location.search);

  function matches(rule) {
    const pair = rule.split('=');
    return params.get(pair[0]) === pair[1];
  }

  document.querySelectorAll('[data-show-when]').forEach(function (el) {
    el.hidden = !matches(el.dataset.showWhen);
  });
  document.querySelectorAll('[data-hide-when]').forEach(function (el) {
    el.hidden = matches(el.dataset.hideWhen);
  });
})();
