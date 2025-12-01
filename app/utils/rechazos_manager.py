"""
Gestor simple de rechazos usando un diccionario global.
{orden_id: [lista_de_delivery_ids_que_rechazaron]}
"""

# Diccionario global para almacenar rechazos
_rechazos_global = {}  # Formato: {orden_id: [delivery_id1, delivery_id2, ...]}

def inicializar_rechazos_orden(orden_id: int):
    """
    Inicializa una entrada para una nueva orden en el diccionario de rechazos.
    Debe llamarse cuando se crea una nueva orden.
    
    Args:
        orden_id: ID de la orden
    """
    _rechazos_global[orden_id] = []

def registrar_rechazo(orden_id: int, delivery_id: int):
    """
    Registra que un delivery ha rechazado una orden.
    
    Args:
        orden_id: ID de la orden rechazada
        delivery_id: ID del delivery que rechazó
    """
    if orden_id in _rechazos_global:
        if delivery_id not in _rechazos_global[orden_id]:
            _rechazos_global[orden_id].append(delivery_id)
    else:
        # Si la orden no estaba inicializada, la inicializamos
        _rechazos_global[orden_id] = [delivery_id]

def obtener_rechazos_orden(orden_id: int) -> list:
    """
    Obtiene la lista de deliveries que han rechazado una orden.
    
    Args:
        orden_id: ID de la orden
    
    Returns:
        Lista de delivery IDs que rechazaron la orden
    """
    return _rechazos_global.get(orden_id, []).copy()

def delivery_ha_rechazado(orden_id: int, delivery_id: int) -> bool:
    """
    Verifica si un delivery específico ha rechazado una orden.
    
    Args:
        orden_id: ID de la orden
        delivery_id: ID del delivery
    
    Returns:
        True si el delivery ya rechazó esta orden
    """
    if orden_id not in _rechazos_global:
        return False
    return delivery_id in _rechazos_global[orden_id]

def limpiar_rechazos_orden(orden_id: int):
    """
    Elimina los registros de rechazos para una orden.
    Útil cuando la orden es completada o cancelada definitivamente.
    
    Args:
        orden_id: ID de la orden a limpiar
    """
    if orden_id in _rechazos_global:
        del _rechazos_global[orden_id]

def obtener_todos_rechazos() -> dict:
    """
    Obtiene todos los rechazos registrados (para debugging/monitoreo).
    
    Returns:
        Diccionario completo de rechazos
    """
    return _rechazos_global.copy()

def limpiar_rechazos_antiguos(ordenes_activas: list):
    """
    Limpia rechazos de órdenes que ya no están activas.
    
    Args:
        ordenes_activas: Lista de IDs de órdenes que SÍ están activas
    """
    ordenes_a_limpiar = []
    for orden_id in _rechazos_global.keys():
        if orden_id not in ordenes_activas:
            ordenes_a_limpiar.append(orden_id)
    
    for orden_id in ordenes_a_limpiar:
        del _rechazos_global[orden_id]