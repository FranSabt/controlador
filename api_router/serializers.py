from rest_framework import serializers
from . models import *
from rest_framework.reverse import reverse


class RouterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Router
        fields = ['url','id','hostname','puerto_api','direccion_ip','usuario','password']
        required_fields = ['hostname','puerto_api','direccion_ip','usuario','password']
    
    def create(self, validated_data):
        return Router.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.hostname = validated_data.get('hostname',instance.nombre)
        instance.puerto_api = validated_data.get('puerto_api',instance.puerto_api)
        instance.direccion_ip = validated_data.get('direccion_ip',instance.direccion_ip)
        instance.usuario = validated_data.get('usuario',instance.usuario)
        instance.password = validated_data.get('password',instance.password)
        instance.save()
        return instance

class PlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Plan
        fields = ['url','id','nombre_comercial','nombre_lista','carga','descarga','precio']
    
    def create(self, validated_data):
        return Plan.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nombre_comercial = validated_data.get('nombre_comercial',instance.nombre_comercial)
        instance.nombre_lista = validated_data.get('nombre',instance.nombre_lista)
        instance.carga = validated_data.get('carga',instance.carga)
        instance.descarga = validated_data.get('descarga',instance.descarga)
        instance.precio = validated_data.get('precio',instance.precio)
        instance.save()
        return instance

class RouterRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
         return reverse('router-detail', args=(value.pk,), request=self.context['request'])
    
    def to_internal_value(self, data):
        try:
            router = Router.objects.get(id=data)
        except:
            router = Router.objects.get(id=int(data.split('/')[-1]))
        finally:
            return router
    
class PlanRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
         return reverse('plan-detail', args=(value.pk,), request=self.context['request'])
    
    def to_internal_value(self, data):
        try:
            plan = Plan.objects.get(id=data)
        except:
            plan = Plan.objects.get(id=int(data.split('/')[-1]))
        finally:
            return plan
        
class EstadoRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
         return reverse('estado-detail', args=(value.pk,), request=self.context['request'])
    
    def to_internal_value(self, data):
        try:
            estado = Estado.objects.get(id=data)
        except:
            estado = Estado.objects.get(id=int(data.split('/')[-1]))
        finally:
            return estado

class CambiarPlanSerializer(serializers.HyperlinkedModelSerializer):
    plan = PlanRelatedField(queryset = Plan.objects.all())
    class Meta:
        model = Servicio
        fields = ['url','plan']

class EstadoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Estado
        fields = ['url','id','estatus']

class ServicioSerializer(serializers.HyperlinkedModelSerializer):
    router = RouterRelatedField(queryset=Router.objects.all()) 
    plan = PlanRelatedField(queryset = Plan.objects.all())
    estado = EstadoRelatedField(queryset = Estado.objects.all())
    class Meta:
        model=Servicio
        fields = ['url','id','hostname','nombre_cliente','router','direccion_ip','plan','estado']
        read_only_fields = ('url','id','hostname')


    def create(self, validated_data):
        try:
            self.router = validated_data.get('router')
        except:
            self.router = int(validated_data.get('router').split('/')[-1])
        return Servicio.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.hostname = validated_data.get('hostname',instance.hostname)
        instance.nombre_cliente = validated_data.get('nombre_cliente',instance.nombre_cliente)
        instance.router = validated_data.get('router',instance.router)
        instance.direccion_ip = validated_data.get('direccion_ip',instance.direccion_ip)
        instance.plan = validated_data.get('plan',instance.plan)
        instance.save()
        return instance

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        hostname = validated_data.get('hostname')
        nombre_cliente = validated_data.get('nombre_cliente')
        router = validated_data.get('router')
        direccion_ip = validated_data.get('direccion_ip')
        plan = validated_data.get('plan')
        try:
            if {'nombre_cliente': nombre_cliente} in Servicio.objects.values('nombre_cliente'):
                self.error_messages('nombre_cliente','Ya existe otro servicio con este nombre')
            elif {'direccion_ip':direccion_ip} in Servicio.objects.values('direccion_ip'):
                self.error_messages('direccion_ip','Ya existe otro servicio con esta dirección ip')
            return super().validate(attrs)

        except:
            print("Error")
