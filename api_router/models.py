from django.db import models
from . import api

# Create your models here.

class Plan(models.Model):
    nombre_comercial = models.CharField(max_length=80,unique=True)
    nombre_lista = models.CharField(max_length=80,unique=True)
    carga = models.CharField(max_length=10,unique=True)
    descarga = models.CharField(max_length=10,unique=True)
    precio = models.FloatField()

    class Meta:
        verbose_name_plural = 'planes'

    def __str__(self):
        return self.nombre_comercial.upper()
    
class Router(models.Model):
    hostname = models.CharField(max_length=100,unique=True)
    puerto_api = models.IntegerField(default=8728)
    direccion_ip = models.CharField(max_length=35,unique=True)
    usuario = models.CharField(max_length=100,default='NETCOM')
    password = models.CharField(max_length=100)

    class Meta:
        ordering = ['hostname']
        verbose_name_plural = 'routers'
        unique_together = ('hostname','direccion_ip')
    
    def __str__(self):
        return self.hostname.upper()
    
    def abrir_sesion(self):
        s = api.open_socket(self.direccion_ip, self.puerto_api)
        if s is None:
            print ('Conexión fallida')
            api.sys.exit(1)
        apiros = api.ApiRos(s)
        if not apiros.login(self.usuario, self.password):
            return None
        else:
            return apiros
    
    def talk(self, instruccion):
        if not instruccion:
            return False
        else:
            apiros = self.abrir_sesion()
            resp = apiros.talk(instruccion)
            return resp
    
    def buscar_id(self, address_, list_ = None) -> str:
        '''
        devuelve el .id de una entrada en una lista address-list
        address_: es la direccion a buscar
        list_: el nombre de la lista donde se necesita buscar la entrada.
                si no se especifica, se devuelve el primer match de cualquier lista
        '''
        instruccion = ["/ip/firewall/address-list/print"]
        resp = self.talk(instruccion=instruccion)
        id_ = None
        for item in resp:
            if item[0] == '!re':
                ent = item[1]
                if not list_:
                    if ent['=address'] == address_:
                        id_ = ent['=.id']
                        break
                else:
                    if ent['=address'] == address_ and ent['=list'] == list_:
                        id_ = ent['=.id']
                        break
        if id_:
            return ent
        else:
            return None
    
class Estado(models.Model):
    estatus = models.CharField(max_length=15)

    def __str__(self):
        return self.estatus.upper()
    
class Servicio(models.Model):
    hostname = models.CharField(max_length=80,unique=True)
    nombre_cliente = models.CharField(max_length=80,unique=True)
    router = models.ForeignKey(Router,on_delete=models.CASCADE)
    direccion_ip = models.CharField(max_length=15,unique=True)
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE,related_name='servicio')
    estado = models.ForeignKey(Estado,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'servicios'

    def __str__(self):
        return self.nombre_cliente.upper()
    
    def add_servicio(self):
        """
        Agrega el servicio al router. 
        Esto implica crear una entrada en un address_list, con la direccion ip del servicio, y el nombre_lista
        del cliente como comentario.
        router es una instancia de la clase Router
        servicio es una instancia de la clase Servicio
        """
        lista = self.plan.nombre_lista
        address = self.direccion_ip
        comentario = self.nombre_cliente
        # se envia la instruccion al router 
        resp = self.router.talk(instruccion=['/ip/firewall/address-list/add', f'=list={lista}', f'=address={address}', f'=comment={comentario}'])
        return resp


    def set_entry(self, direccion_nueva = None, comentario_nuevo = None, lista_nueva = None ):
        """
        Para setear algo en el servicio (es decir, una entrada en un address-list). Se usaría para cambiarle la direccion ip,
        comentario  o cambiarlo la lista. Ejemplo: un servicio que cambia de nombre, o de plan y por lo tanto debe agregarse 
        en una lista diferente.
        """
        lista = self.plan.nombre_lista
        address = self.direccion_ip
        comentario = self.nombre_cliente
        if comentario_nuevo:
            comentario = comentario_nuevo
        if lista_nueva:
            lista = lista_nueva
        if direccion_nueva:
            address = direccion_nueva
        
        # chequeamos que la entrada exista en el router
        entrada = self.router.buscar_id(address_= self.direccion_ip)
        if entrada:
           # la entrada existe en el router
            resp = self.router.talk(
                instruccion=['/ip/firewall/address-list/set', f'=list={lista}', f'=address={address}', f'=comment={comentario}', f'=.id={entrada["=.id"]}']
                )
        else:
            #la entrada no existe en el router
            resp = self.router.talk(
                instruccion=['/ip/firewall/address-list/add', f'=list={lista}', f'=address={address}', f'=comment={comentario}']
                )        
        return resp


    def remove_servicio(self):
        """
        Para borrar el servicio del router. Por ejemplo, si el cliente cancela el servicio.
        """
        entrada = self.router.buscar_id(address_= self.direccion_ip, list_= self.plan.nombre_lista)
        
        if entrada == None:
            entrada = self.router.buscar_id(address_= self.direccion_ip, list_= 'Moroso')

        if entrada:
            return self.router.talk(['/ip/firewall/address-list/remove', f'=.id={entrada["=.id"]}'])
        else:
            return None


    def suspender_servicio(self):
        """
        Para suspender el servicio. 
        Por ejemplo, si un cliente tiene deuda vencida. La accion consiste en agregar el servicio en el address_list 'Moroso'.
        """
        entrada = self.router.buscar_id(address_= self.direccion_ip , list_= 'Moroso') 
        if not entrada:
            #El cliente no esta suspendido
            self.set_entry(lista_nueva = 'Moroso')
            print(f'\nServicio {self.id} suspendido.\n')
        return


    def activar_servicio(self):
        """
        Para activar el servicio. 
        Por ejemplo, si el cliente estaba suspendido por pago, pero ya saldó su deuda. La accion consiste en borrar el servicio 
        del address_list 'Moroso', y agregarlo en su plan correspondiente
        """
        # primero, lo buscamos en su plan
        entrada = self.router.buscar_id(address_= self.direccion_ip, list_= self.plan.nombre_lista)
        if not entrada:
            self.add_servicio()

        # buscamos el servicio en la lista Moroso
        entrada = self.router.buscar_id(address_= self.direccion_ip, list_= 'Moroso')
        if entrada:
            # estaba en Moroso. Procedemos a borrarlo
            self.router.talk(["/ip/firewall/address-list/remove", f'=.id={entrada["=.id"]}'])