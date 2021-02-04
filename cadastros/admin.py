from django.contrib import admin
from .models import Autor
from .models import Avaliador
from .models import Avaliacao
from .models import Premio
from .models import Projeto
from .models import Telefone
from .models import Cronograma


# # Class inline
class TelefoneInline(admin.TabularInline):
    model = Telefone


# Class admin
class AutorAdmin(admin.ModelAdmin):
    fields = ("nome", "endereco", "email")

    inlines = [TelefoneInline]


# Register your models here.
admin.site.register(Autor, AutorAdmin)
admin.site.register(Avaliador)
admin.site.register(Avaliacao)
admin.site.register(Premio)
admin.site.register(Projeto)
admin.site.register(Cronograma)
admin.site.register(Telefone)


