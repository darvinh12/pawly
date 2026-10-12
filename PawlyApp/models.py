from datetime import date

from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Profile(models.Model):
    # Perfil humano del usuario
    GENDERS = [('f', _('Femenino')), ('m', _('Masculino')), ('o', _('Otro'))]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150)
    national_id = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='avatars/', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True)
    city = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Pet(models.Model):
    # Perfil de la mascota
    SPECIES = [('dog', _('Perro')), ('cat', _('Gato'))]
    SEXES = [('m', _('Macho')), ('f', _('Hembra'))]
    TEMPERAMENTS = [
        ('playful', _('Juguetón')),
        ('sociable', _('Sociable')),
        ('shy', _('Tímido')),
        ('calm', _('Tranquilo')),
        ('protective', _('Protector')),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=3, choices=SPECIES)
    sex = models.CharField(max_length=1, choices=SEXES)
    birth_date = models.DateField(null=True, blank=True)
    temperament = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    photo = models.ImageField(upload_to='pets/', blank=True)
    location = models.CharField(max_length=100, blank=True)
    for_adoption = models.BooleanField(default=False)
    family = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def age(self):
        if not self.birth_date:
            return ''
        today = date.today()
        months = (today.year - self.birth_date.year) * 12 + today.month - self.birth_date.month
        if today.day < self.birth_date.day:
            months -= 1
        if months < 12:
            return ngettext('%(count)d mes', '%(count)d meses', months) % {'count': months}
        years = months // 12
        return ngettext('%(count)d año', '%(count)d años', years) % {'count': years}

    def temperament_list(self):
        names = dict(self.TEMPERAMENTS)
        return ', '.join(str(names[value]) for value in self.temperament.split(',') if value in names)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return static('img/logo-mark.png')


class Application(models.Model):
    # Postulación para adoptar una mascota
    STATUSES = [
        ('pending', _('Pendiente')),
        ('accepted', _('Aceptada')),
        ('rejected', _('Rechazada')),
        ('cancelled', _('Cancelada')),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUSES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['pet', 'applicant']

    def __str__(self):
        return f'{self.applicant} - {self.pet}'


class Chat(models.Model):
    # Conversación entre dos usuarios
    application = models.OneToOneField(Application, on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ', '.join(member.username for member in self.members.all())

    def other_member(self, user):
        return self.members.exclude(id=user.id).first()

    def last_message(self):
        return self.messages.last()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.text[:40]
