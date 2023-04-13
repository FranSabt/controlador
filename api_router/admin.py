from django.contrib import admin
from . models import *

class ViewRouter(admin.ModelAdmin):
    list_display=('id','hostname','puerto_api','direccion_ip','usuario','password')

class ViewPlan(admin.ModelAdmin):
   list_display=('id','nombre_comercial','nombre_lista','carga','descarga','precio') 

class ViewEstado(admin.ModelAdmin):
   list_display= ('id','estatus')

class ViewServicio(admin.ModelAdmin):
   list_display=('id','hostname','nombre_cliente','router','direccion_ip','plan','estado')

# Register your models here.
admin.site.register(Router,ViewRouter)
admin.site.register(Plan,ViewPlan)
admin.site.register(Servicio,ViewServicio)
admin.site.register(Estado,ViewEstado)