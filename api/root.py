"""Root"""
from flask import jsonify
from api import api


@api.route('/ping', methods=['GET'])
def ping():
    """Servicio de estado: brinda una respuesta rápida que permita ser consultada
    para conocer si el servidor se encuentra activo"""
    return jsonify(ping=1)


@api.route('/stats', methods=['GET'])
def stats():
    """Servicio de consulta de datos de uso: brinda datos acerca
     del uso del application server."""
    return jsonify(message='not implemented yet')
