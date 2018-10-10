"""product model"""
from marshmallow import Schema, fields
from models.model import Model



class LocationSchema(Schema):
    """Location marshmallow schema"""
    x = fields.Float(required=True)
    y = fields.Float(required=True)


class ProductSchema(Schema):
    """Product marshmallow schema"""
    _id = fields.Str()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    seller = fields.Str(required=True)
    units = fields.Int(required=True)
    price = fields.Float(required=True)
    location = fields.Nested(LocationSchema, required=True)
    categories = fields.List(fields.Str())
    payment_methods = fields.List(fields.Str(), required=True)
    pictures = fields.List(fields.Url(), required=True)
    published = fields.Str(required=True)


class Product(Model):
    """product model"""
    collection_name = 'products'
