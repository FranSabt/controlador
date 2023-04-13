from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer,AdminRenderer, BrowsableAPIRenderer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

# Create your views here.

@api_view(['GET'])
@renderer_classes([AdminRenderer,JSONRenderer,BrowsableAPIRenderer])
def api_root(request, format=None):
    return Response({
        'routers': reverse('router-list', request=request, format=format),
        'planes': reverse('plan-list', request=request, format=format),
        'servicios': reverse('servicio-list', request=request, format=format),
        'estados': reverse('estado-list', request=request, format=format)
    })

class RouterViewSet(viewsets.ModelViewSet,AdminRenderer):
    queryset = Router.objects.all().order_by('id')
    serializer_class = RouterSerializer
    renderer_classes=[AdminRenderer,JSONRenderer,BrowsableAPIRenderer]
    pagination_class = PageNumberPagination
    template_name = 'rest_framework/api.html'
    context={'routers':queryset}
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = RouterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = JsonResponse ({"message": 'success'})
            response.status_code = 201 
            return response
        else:
            response = JsonResponse ({'errors':serializer.errors,'data':data,'serializer':serializer.data})
            response.status_code = 403
            return response
    
class EstadoViewSet(viewsets.ModelViewSet,AdminRenderer):
    queryset = Estado.objects.all().order_by('id')
    serializer_class = EstadoSerializer
    renderer_classes=[AdminRenderer,JSONRenderer,BrowsableAPIRenderer]
    pagination_class = PageNumberPagination
    template_name = 'rest_framework/api.html'
    context={'estado':queryset}
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = EstadoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = JsonResponse ({"message": 'success'})
            response.status_code = 201 
            return response
        else:
            response = JsonResponse ({'errors':serializer.errors,'data':data,'serializer':serializer.data})
            response.status_code = 403
            return response




class PlanViewSet(viewsets.ModelViewSet,AdminRenderer):
    queryset = Plan.objects.all().order_by('id')
    serializer_class = PlanSerializer
    renderer_classes=[AdminRenderer,JSONRenderer,BrowsableAPIRenderer]
    #parser_classes = [JSONParser]
    pagination_class = PageNumberPagination
    template_name = 'rest_framework/api.html'
    context={'planes':queryset}

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = PlanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = JsonResponse ({"message": 'success'})
            response.status_code = 201 
            return response
        else:
            response = JsonResponse ({'errors':serializer.errors,'data':data,'serializer':serializer.data})
            response.status_code = 403
            return response
    

class ServicioViewSet(viewsets.ModelViewSet,AdminRenderer):
    queryset = Servicio.objects.all().order_by('id')
    serializer_class = ServicioSerializer
    renderer_classes=[AdminRenderer,JSONRenderer,BrowsableAPIRenderer]
    parser_classes = [JSONParser,]
    pagination_class = PageNumberPagination
    template_name = 'rest_framework/api.html'
    context = {'lista':queryset}

    
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = ServicioSerializer(data=data)
        if serializer.is_valid():
            servicio_args = serializer.validated_data
            servicio=Servicio(**servicio_args)
            try:
                servicio.add_servicio()
            except:
                print('No se pudo conectar con el router. Servicio no agregado al router')
                response = JsonResponse({'mensaje':'No se pudo conectar con el router. Servicio no guardado en la base de datos. Reintente.'})
                response.status_code = 503
                return response
            servicio.save()
            servicio.hostname = f'{servicio.id}.clientes-netcom.com'
            servicio.save()
            response = JsonResponse ({"message":'success','id':servicio.id})
            response.status_code = 201 
            return response
        else:
            response = JsonResponse ({'errors':serializer.errors,'data':data})
            response.status_code = 403
            print(serializer.errors)
            return response

    def suspender(self, request,pk):
        servicio = get_object_or_404(Servicio,pk=pk)
        try:
            servicio.suspender_servicio()
        except:
            response = JsonResponse({'mensaje':'No se pudo conectar con el router. Reintente'})
            response.status_code = 503
            return response
        servicio.estado = Estado.objects.get(estatus="SUSPENDIDO")
        servicio.save()
        return JsonResponse({'mensaje':f'Servicio suspendido'})
    
    def reactivar(self, request,pk):
        servicio = get_object_or_404(Servicio,pk=pk)
        try:
            servicio.activar_servicio()
        except:
            response = JsonResponse({'mensaje':'No se pudo conectar con el router. Reintente'})
            response.status_code = 503
            return response
        servicio.estado = Estado.objects.get(estatus="ACTIVO")
        servicio.save()
        return JsonResponse({'mensaje':'Servicio activo'})
    
    def cancelar(self,request,pk):
        servicio = get_object_or_404(Servicio,pk=pk)
        try:
            servicio.remove_servicio()
        except:
            response = JsonResponse({'mensaje':'No se pudo conectar con el router. Reintente'})
            response.status_code = 503
            return response
        servicio.estado = Estado.objects.get(estatus="CANCELADO")
        servicio.save()
        return JsonResponse({'mensaje':'Servicio cancelado'})
    
    def cambiar_plan(self,request,pk):
        servicio=get_object_or_404(Servicio,pk=pk)
        if servicio.estado.estatus == 'ACTIVO':
            lista = Plan.objects.get(pk=request.data['plan'])
        else:
            response = JsonResponse({'mensaje':'Cliente suspendido o cancelado. No se cambiará el plan'})
            response.status_code = 409
            return response
        try:
            servicio.set_entry(lista_nueva=lista.nombre_lista)
        except:
            response = JsonResponse({'mensaje':'No se pudo conectar con el router. Reintente'})
            response.status_code = 503
            return response
        servicio.plan = lista
        servicio.save(update_fields=['plan'])
        return JsonResponse({'mensaje':'Plan del servicio actualizado'})
 
    
    def cambiar_nombre(self,request,pk):
        servicio=get_object_or_404(Servicio,pk=pk)
        try:
            servicio.set_entry(comentario_nuevo=request.data['nombre_cliente'])
        except:
            response = JsonResponse({'mensaje':'No se pudo conectar con el router. Reintente'})
            response.status_code = 503
            return response
        servicio.nombre_cliente =request.data['nombre_cliente']
        servicio.save(update_fields=['nombre_cliente'])
        return JsonResponse({'mensaje':'Nombre del servicio actualizado'})
    
    def cambiar_direccion(self,request,pk):
        servicio=get_object_or_404(Servicio,pk=pk)
        ip=request.data['direccion_ip']
        if Servicio.objects.filter(direccion_ip=ip):
            response =JsonResponse({'mensaje':f'IP {ip} en uso'})
            response.status_code = 500
            return response
        else:
            try:
                servicio.set_entry(direccion_nueva=request.data['direccion_ip'])
            except:
                response = JsonResponse({'mensaje':'No se pudo conectar con el router. Reintente'})
                response.status_code = 503
                return response
            servicio.direccion_ip = request.data['direccion_ip']
            servicio.save(update_fields=['direccion_ip'])
            return JsonResponse({'mensaje':'Dirección IP del servicio actualizado'})
    
    def actualizar(self,request,pk):
        servicio = get_object_or_404 (Servicio,pk=pk)
        data = dict()
        try:
            data['hostname'] = request.data['hostname']
        except:
            data['hostname'] = servicio.hostname
        try:
            data['nombre_cliente'] = request.data['nombre_cliente']
        except:
            data['nombre_cliente'] = servicio.nombre_cliente
        try:
            data['router'] = request.data['router']
        except:
            data['router'] = servicio.router
        try:
            data['direccion_ip'] = request.data['direccion_ip']
        except:
            data['direccion_ip'] = servicio.direccion_ip
        try:
            data['plan'] = request.data['plan']
        except:
            data['plan'] = servicio.plan
        try:
            data['estado'] = request.data['estado']
        except:
            data['estado'] = servicio.estado
        
        if servicio.estado.estatus == 'ACTIVO':
            lista = data['plan'].nombre_lista
        else:
            lista = 'Moroso'
        ip = data['direccion_ip']
        if Servicio.objects.filter(direccion_ip=data['direccion_ip']):
            response =JsonResponse({'mensaje':f'IP {ip} en uso'})
            response.status_code = 500
            return response
        else:
            try:
                servicio.set_entry(direccion_nueva=data['direccion_ip'],comentario_nuevo=data['nombre_cliente'],lista_nueva=lista)
            except:
                response = JsonResponse({'mensaje':'No se pudo conectar con el router. Reintente'})
                response.status_code = 503
                return response
            s = ServicioSerializer().update(servicio, validated_data=data)
            s.save()
            return JsonResponse({'mensaje':'Servicio actualizado'})