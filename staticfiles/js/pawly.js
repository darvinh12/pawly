/* Pawly: JS general de las pantallas. Sin librerías.
   Cada comportamiento se activa con atributos en el HTML:
     form[data-validate]                  valida los campos [required] antes de enviar el formulario
     form[data-next]                      pantallas de ejemplo: si todo está bien navega a data-next en vez de enviar
     form[data-autosubmit]                se envía solo cuando cambia una de sus opciones
     [data-confirm]                       pide confirmación antes de seguir (enlaces, o botones con data-next)
     input[data-reveals="id"]             un interruptor muestra u oculta el bloque con ese id
     input[data-confirm-off]              pide confirmación al apagar ese interruptor
     button[data-toggle-password="id"]    muestra u oculta la contraseña del campo con ese id
     button[aria-pressed]                 botones que se activan y desactivan (Me gusta, Seguir, Favorito)
     a[data-close]                        cierre de una ventana modal: también se cierra con Escape o con un clic en el fondo
     [data-show-when] / [data-hide-when]  muestran u ocultan según la URL, p. ej. "postulacion=enviada" */
(function () {
  'use strict';

  /*  Validación de formularios  */
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
      // Si falta algún campo no se envía
      if (!validate(form)) {
        event.preventDefault();
        return;
      }
      // Con data-next se navega a la siguiente pantalla; sin data-next el formulario va al servidor
      if (form.dataset.next) {
        event.preventDefault();
        window.location.href = form.dataset.next;
      }
    });
  }

  /*  Mostrar u ocultar la contraseña  */
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

  /*  Confirmaciones y botones que se activan y desactivan  */
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

    // El botón de mostrar contraseña ya tiene su propio comportamiento
    if (event.target.closest('[data-toggle-password]')) return;

    const pressable = event.target.closest('button[aria-pressed]');
    if (pressable) {
      const pressed = pressable.getAttribute('aria-pressed') === 'true';
      pressable.setAttribute('aria-pressed', String(!pressed));
    }
  });

  /*  Formularios que se envían solos al cambiar una opción (por ejemplo el idioma en Ajustes)  */
  document.querySelectorAll('form[data-autosubmit]').forEach(function (form) {
    form.addEventListener('change', function () {
      form.submit();
    });
  });

  /*  Interruptores que muestran u ocultan un bloque  */
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

  /*  Ventanas modales: Escape o un clic en el fondo oscuro la cierran, igual que el botón X  */
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

  /*  Elementos que se muestran u ocultan según la URL (por ejemplo ?postulacion=enviada)  */
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
