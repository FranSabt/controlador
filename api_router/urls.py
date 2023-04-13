from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . views import *
from rest_framework.authtoken.views import obtain_auth_token

router_list = RouterViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
router_detail = RouterViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
router_create = RouterViewSet.as_view({
    'get': 'create',
    'post': 'create'
})
plan_list = PlanViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
plan_detail = PlanViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
plan_create = PlanViewSet.as_view({
    'get': 'create',
    'post': 'create'
})
estado_list = EstadoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
estado_detail = EstadoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
estado_create = EstadoViewSet.as_view({
    'get': 'create',
    'post': 'create'
})
servicio_list = ServicioViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

servicio_detail = ServicioViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

servicio_create = ServicioViewSet.as_view({
    'get': 'create',
    'post' : 'create'
})

servicio_plan = ServicioViewSet.as_view({
    'patch' : 'cambiar_plan',
    'post' : 'cambiar_plan'
})

servicio_nombre = ServicioViewSet.as_view({
    'patch' : 'cambiar_nombre',
    'post' : 'cambiar_nombre'
})

servicio_direccion = ServicioViewSet.as_view({
    'patch' : 'cambiar_direccion',
    'post' : 'cambiar_direccion'
})

suspender = ServicioViewSet.as_view({
    'patch':'suspender',
    'get':'suspender',
    'post':'suspender'
})

reactivar = ServicioViewSet.as_view({
    'patch':'reactivar',
    'get':'reactivar',
    'post':'reactivar'
})

cancelar = ServicioViewSet.as_view({
    'patch':'cancelar',
    'get':'cancelar',
    'post':'cancelar'
})

servicio_actualizar = ServicioViewSet.as_view({
    'patch':'actualizar',
    'post':'actualizar'
})

urlpatterns = format_suffix_patterns([
    path('', api_root,name='api_root'),
    path('router-list/',router_list, name='router-list'),
    path('router-list/<int:pk>',router_detail,name='router-detail'),
    path('router-list/router-create',router_create,name='router-create'),
    path('estado-list/',estado_list, name='estado-list'),
    path('estado-list/<int:pk>',estado_detail,name='estado-detail'),
    path('estado-list/estado-create',estado_create,name='estado-create'),
    path('plan-list/',plan_list, name='plan-list'),
    path('plan-list/<int:pk>',plan_detail,name='plan-detail'),
    path('plan-list/plan-create',plan_create,name='plan-create'),
    path('servicio-list/',servicio_list, name='servicio-list'),
    path('servicio-list/<int:pk>',servicio_detail,name='servicio-detail'),
    path('servicio-list/servicio-create',servicio_create,name='servicio-create'),
    path('servicio-list/<int:pk>/suspender',suspender,name='suspender-servicio'),
    path('servicio-list/<int:pk>/reactivar',reactivar,name='reactivar-servicio'),
    path('servicio-list/<int:pk>/cancelar',cancelar,name='cancelar-servicio'),
    path('servicio-list/<int:pk>/cambiar_plan',servicio_plan,name='plan-servicio'),
    path('servicio-list/<int:pk>/cambiar_nombre',servicio_nombre,name='nombre-servicio'),
    path('servicio-list/<int:pk>/cambiar_direccion',servicio_direccion,name='direccion-servicio'),
    path('servicio-list/<int:pk>/actualizar',servicio_actualizar,name='actalizar-servicio'),
])