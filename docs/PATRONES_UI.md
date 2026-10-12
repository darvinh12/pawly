# Patrones de diseño de interfaz de Pawly

Revisión pedida en el Reto 13: identificar los patrones de diseño de interfaz que usan las pantallas
y comprobar en [ui-patterns.com](https://ui-patterns.com/patterns) si la implementación cumple las
especificaciones de cada solución.

Para cada patrón se leyeron las secciones *Usage* y *Solution* de su página en ui-patterns.com y se
compararon con las plantillas de `PawlyApp/templates`, el CSS y el JS del proyecto.

## Resumen

Se identificaron 25 patrones.

| Resultado | Patrones |
|---|---|
| Cumple | 17 |
| Cumple con una observación | 5 |
| Pendiente para el Reto 14 | 3 |

## Navegación

| Patrón | Dónde se usa | Cumple | Observaciones |
|---|---|---|---|
| [Navigation Tabs](https://ui-patterns.com/patterns/NavigationTabs) | Menú principal: barra inferior en móvil y menú lateral en escritorio (`base_app.html`) | Sí | Tiene seis secciones, entre las 2 y 9 que pide el patrón. Aparece igual y en el mismo orden en todas las pantallas, todo el botón es clicable y la sección actual se marca con `aria-current="page"`. |
| [Home Link](https://ui-patterns.com/patterns/HomeLink) | Logotipo de la barra superior | Sí | El logo lleva a Inicio desde todas las pantallas y siempre está en el mismo lugar. En el panel de administración lleva al panel, que es el inicio del administrador, y se distingue con la palabra "Admin". |
| [Modal](https://ui-patterns.com/patterns/modal-windows) | Postulación, nueva publicación y reporte | Sí | El fondo queda oscurecido e inactivo (`inert`) y el título coincide con la acción ("Postularte para adoptar a Toby" y "Enviar postulación"). Se cierra con la X de la esquina, con el botón Cancelar, con la tecla Escape o con un clic en el fondo. Las dos últimas se agregaron en esta revisión. |
| [Module Tabs](https://ui-patterns.com/patterns/ModuleTabs) | Pestañas de Mi perfil y del perfil de otro usuario | Con observación | Las pestañas son enlaces que bajan a cada sección y todas las secciones se ven a la vez. El patrón pide mostrar una sola sección por vez y cambiarla sin recargar la página. Además, la pestaña "Guardados" apunta a una sección que todavía no existe. |
| [Notifications](https://ui-patterns.com/patterns/notifications) | Pantalla de notificaciones, campana de la barra superior | Sí | Las notificaciones sin leer se distinguen y el contador aparece en la campana y en el menú. Las de un mismo tipo se agrupan ("Hay 3 mascotas nuevas en adopción cerca de ti"). Incluyen acciones directas (Abrir chat, Aceptar, Rechazar, Seguir también) y se pueden marcar todas como leídas. En Ajustes se decide si también llegan por correo. |

## Formularios

| Patrón | Dónde se usa | Cumple | Observaciones |
|---|---|---|---|
| [Account Registration](https://ui-patterns.com/patterns/AccountRegistration) | Iniciar sesión, registro y recuperar contraseña | Sí | Las opciones de entrar, crear cuenta y recuperar la contraseña están siempre a la vista. Los requisitos de la contraseña se explican en palabras simples ("Mínimo 8 caracteres, con un número"). Después de entrar, el usuario vuelve a la página que quería ver gracias al parámetro `next`. El patrón también menciona un medidor de seguridad de la contraseña y el ingreso con redes sociales, que son opcionales y no forman parte del diseño de la Entrega 2. |
| [Wizard](https://ui-patterns.com/patterns/Wizard) | Registro en dos pasos: cuenta y perfil humano | Con observación | Muestra el paso actual y la barra de progreso, tiene el botón "Volver al paso 1" y un botón final claro ("Listo, entrar a Pawly"). Falta avisar que se pierden los datos si el usuario abandona a mitad del registro. |
| [Steps Left](https://ui-patterns.com/patterns/StepsLeft) | Indicador "Paso 1 de 2" del registro | Con observación | El patrón recomienda no usar un bloque de pasos cuando el proceso tiene solo dos. Pawly usa una barra de progreso sencilla en lugar del bloque completo, que es la forma ligera que pide el Wizard. Se mantiene porque así está en la Entrega 2. |
| [Input Feedback](https://ui-patterns.com/patterns/InputFeedback) | Todos los formularios | Sí | Se valida la presencia, el formato del correo, el largo y el número de la contraseña, que las contraseñas coincidan y que el usuario y el correo no estén repetidos. El error aparece junto al campo en rojo, explica cómo corregirlo y el cursor va al primer campo con error. Al terminar bien se muestra un aviso verde, por ejemplo "Postulación enviada" o "Tu contraseña se guardó". |
| [Input Prompt](https://ui-patterns.com/patterns/InputPrompt) | Buscadores, mensajes, comentarios y nueva publicación | Sí | Los textos de ejemplo invitan a la acción ("Buscar personas, mascotas o publicaciones", "Escribe un mensaje…") y siempre acompañan a una etiqueta, visible o para lectores de pantalla. Desaparecen al escribir. |
| [Inline Hints](https://ui-patterns.com/patterns/inline-hints) | Ayudas bajo los campos | Sí | Por ejemplo "Así te encontrarán otras personas" o "JPG o PNG, máximo 5 MB", asociadas al campo con `aria-describedby`. |
| [Good Defaults](https://ui-patterns.com/patterns/GoodDefaults) | Mensaje de la postulación, ubicación de la mascota y ajustes | Con observación | La ubicación toma la ciudad del dueño y los ajustes empiezan en español, tema claro y avisos en la aplicación. El mensaje de la postulación y las opciones "Tengo patio" y "Sin otras mascotas" vienen marcadas con datos de ejemplo. Cuando exista el perfil humano conviene tomarlas de ahí, porque el patrón pide usar valores por defecto solo cuando es seguro que el usuario los aceptaría. |
| [Settings](https://ui-patterns.com/patterns/settings) | Ajustes | Sí | Las opciones están agrupadas en Cuenta, Notificaciones y Apariencia e idioma, con menos de siete por grupo, y se ve el valor actual de cada una. |

## Contenido y datos

| Patrón | Dónde se usa | Cumple | Observaciones |
|---|---|---|---|
| [Cards](https://ui-patterns.com/patterns/cards) | Mascotas en adopción, publicaciones, reportes del administrador | Sí | Cada tarjeta reúne foto, título, un resumen corto y la acción. Las listas avanzan en un solo sentido. |
| [Search Filters](https://ui-patterns.com/patterns/LiveFilter) | Filtros del feed de adopción y pestañas de resultados de búsqueda | Pendiente | Los filtros están dibujados con chips (Perros, Gatos, Cachorros, menos de 5 km). Que filtren de verdad, actualizando la lista al instante, es el fragmento UC-17.2 del Reto 14. |
| [Gallery](https://ui-patterns.com/patterns/Gallery) | Fotos en la ficha de la mascota | Pendiente | Las miniaturas se muestran y la primera está resaltada, pero todavía no cambian la foto grande. Hoy cada mascota tiene una sola foto de ejemplo. Al guardar varias fotos por mascota hay que permitir pasar de una a otra. |
| [Blank Slate](https://ui-patterns.com/patterns/BlankSlate) | Feed de adopción sin resultados | Pendiente | Si no hay mascotas aparece "No hay mascotas en adopción cerca de ti por ahora". Falta el botón para ampliar la distancia que describe el flujo alternativo A3.2 de UC-17, que corresponde al fragmento UC-17.3 del Reto 14. |
| [Dashboard](https://ui-patterns.com/patterns/dashboard) | Panel de administración | Sí | Está pensado para un solo objetivo, la moderación de la comunidad: muestra cuatro indicadores y debajo la lista de usuarios y los reportes pendientes, cada uno con su acción. |

## Interacción social

| Patrón | Dónde se usa | Cumple | Observaciones |
|---|---|---|---|
| [Activity Stream](https://ui-patterns.com/patterns/ActivityStream) | Inicio | Sí | Cada publicación muestra quién la hizo, dónde y cuándo, con enlaces al autor y al contenido, y todas tienen el mismo formato. |
| [Chat](https://ui-patterns.com/patterns/direct-messaging) | Mensajes y conversación | Sí | Tiene la bandeja de entrada con los últimos mensajes, la conversación con los mensajes enviados y recibidos, y el campo para escribir con el botón Enviar. Las peticiones de chat aparecen aparte. |
| [Follow](https://ui-patterns.com/patterns/follow) | Sugerencias de Inicio, búsqueda y perfil de otro usuario | Sí | El botón Seguir cambia a Siguiendo y lo que publican las personas seguidas aparece en Inicio. |
| [Favorites](https://ui-patterns.com/patterns/favorites) | Corazón en la ficha de la mascota | Sí | Es un botón de activar y desactivar con forma de corazón junto a la mascota. La lista de favoritos es la pestaña Guardados del perfil (ver la observación de Module Tabs). |
| [Reaction](https://ui-patterns.com/patterns/reaction) | Me gusta en las publicaciones | Sí | Es una reacción de un solo toque, sin escala de estrellas, con el total visible. |
| [Tagging](https://ui-patterns.com/patterns/Tag) | Etiquetados en la nueva publicación | Con observación | En Pawly se etiquetan personas y mascotas en una publicación (UC-11), y cada etiqueta se muestra como un chip que se puede quitar. El patrón de ui-patterns habla de palabras clave que además sirven para buscar. Esa búsqueda por etiquetas no forma parte del alcance actual. |
| [Flagging & Reporting](https://ui-patterns.com/patterns/flagging-and-reporting) | Reportar publicación y cuenta | Sí | El usuario elige un motivo, puede agregar detalles y el reporte es anónimo. Los reportes llegan al panel de administración para su moderación. |

## Cambios hechos en esta revisión

- Las ventanas modales de postulación, nueva publicación y reporte ahora se cierran con la tecla Escape y con un clic en el fondo oscuro, como pide el patrón Modal. El cambio está en `staticfiles/js/pawly.js` (atributo `data-close`) y no modifica cómo se ven las pantallas.

## Pendientes

Para el Reto 14:

1. Hacer que los filtros del feed de adopción filtren la lista al instante (Search Filters, UC-17.2).
2. Agregar el botón para ampliar la distancia cuando el feed está vacío (Blank Slate, UC-17.3).
3. Permitir pasar entre las fotos de la mascota desde las miniaturas cuando haya varias (Gallery).
4. Tomar los valores por defecto de la postulación del perfil humano del usuario (Good Defaults).

Para decidir en el equipo, porque cambian lo que se ve en las pantallas de la Entrega 2:

5. Que las pestañas del perfil muestren una sola sección por vez y crear la sección Guardados (Module Tabs).
6. Avisar que se pierden los datos si el usuario abandona el registro a mitad (Wizard).
