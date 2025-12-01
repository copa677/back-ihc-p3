"""
Utilidades para cálculo de distancias entre coordenadas
CON gestión de rechazos usando diccionario global.
"""
import math
from typing import List, Tuple, Optional
from app.models.user_delivery import UserDelivery
from app.utils.rechazos_manager import delivery_ha_rechazado

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula la distancia en kilómetros entre dos puntos geográficos."""
    R = 6371.0
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def find_closest_delivery(
    restaurant_lat: float, 
    restaurant_lon: float,
    orden_id: Optional[int] = None,
    include_only_available: bool = True
) -> Optional[Tuple[UserDelivery, float]]:
    """
    Encuentra el delivery más cercano al restaurante,
    EXCLUYENDO los deliveries que ya rechazaron esta orden.
    
    Args:
        restaurant_lat: Latitud del restaurante
        restaurant_lon: Longitud del restaurante
        orden_id: ID de la orden (para excluir deliveries que la rechazaron)
        include_only_available: Si True, solo deliveries sin orden asignada
    
    Returns:
        Tupla (delivery, distancia_en_km) o None si no hay deliveries
    """
    # Obtener todos los deliveries activos
    query = UserDelivery.query.filter_by(esta_activo=True)
    
    if include_only_available:
        query = query.filter_by(id_orden=None)
    
    deliveries = query.all()
    
    if not deliveries:
        return None
    
    # Filtrar deliveries que ya rechazaron esta orden (si se especificó orden_id)
    if orden_id:
        deliveries_filtrados = []
        for delivery in deliveries:
            # EXCLUIR si el delivery ya rechazó esta orden
            if not delivery_ha_rechazado(orden_id, delivery.id):
                deliveries_filtrados.append(delivery)
        
        # Si después de filtrar no quedan deliveries
        if not deliveries_filtrados:
            return None
        
        deliveries = deliveries_filtrados
    
    # Calcular distancia de cada delivery al restaurante
    closest_delivery = None
    min_distance = float('inf')
    
    for delivery in deliveries:
        if delivery.latitud is None or delivery.longitud is None:
            continue
            
        distance = haversine_distance(
            restaurant_lat, restaurant_lon,
            float(delivery.latitud), float(delivery.longitud)
        )
        
        if distance < min_distance:
            min_distance = distance
            closest_delivery = delivery
    
    if closest_delivery:
        return (closest_delivery, min_distance)
    
    return None


def assign_order_to_closest_delivery(
    orden_cod: int, 
    restaurant_lat: float, 
    restaurant_lon: float
) -> Tuple[bool, str, Optional[UserDelivery]]:
    """
    Asigna una orden al delivery más cercano al restaurante.
    Automáticamente excluye deliveries que ya rechazaron esta orden.
    
    Args:
        orden_cod: Código de la orden a asignar
        restaurant_lat: Latitud del restaurante
        restaurant_lon: Longitud del restaurante
    
    Returns:
        Tuple (success, message, delivery_asignado)
    """
    from app import db
    
    try:
        # Buscar el delivery más cercano disponible QUE NO HAYA RECHAZADO ESTA ORDEN
        result = find_closest_delivery(
            restaurant_lat, restaurant_lon,
            orden_id=orden_cod,  # ¡IMPORTANTE! Excluye rechazos
            include_only_available=True
        )
        
        if not result:
            return False, "No hay deliveries disponibles para esta orden", None
        
        delivery, distance = result
        
        # Doble verificación (por si acaso)
        if delivery.id_orden is not None:
            return False, f"El delivery {delivery.username} ya tiene una orden asignada", None
        
        # Asignar la orden al delivery
        delivery.id_orden = orden_cod
        db.session.commit()
        
        return True, f"Orden {orden_cod} asignada a {delivery.username} (distancia: {distance:.2f} km)", delivery
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al asignar orden: {str(e)}", None


def registrar_rechazo_y_liberar_delivery(orden_id: int, delivery_id: int) -> bool:
    """
    Registra un rechazo y libera al delivery de la orden.
    
    Args:
        orden_id: ID de la orden rechazada
        delivery_id: ID del delivery que rechazó
    
    Returns:
        True si se procesó correctamente
    """
    from app import db
    from app.utils.rechazos_manager import registrar_rechazo
    
    try:
        # 1. Liberar al delivery (quitarle la orden asignada)
        delivery = UserDelivery.query.get(delivery_id)
        if delivery and delivery.id_orden == orden_id:
            delivery.id_orden = None
            db.session.commit()
        
        # 2. Registrar el rechazo en el diccionario global
        registrar_rechazo(orden_id, delivery_id)
        
        return True
        
    except Exception:
        db.session.rollback()
        return False