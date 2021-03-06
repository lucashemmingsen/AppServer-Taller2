"""Order model"""
from datetime import datetime
import bson
from marshmallow import Schema, fields, post_load, validates, ValidationError, validate
from appserver.utils.mongo import ObjectId
from appserver.models.base import BaseModel
from appserver.models.location import LocationSchema
# pylint: disable=R0903,R0201,C0103,R0902


class EstimateShippingInputData:
    """EstimateInputData"""
    def __init__(self, product_id, units):
        self.product_id = bson.ObjectId(product_id)
        self.units = units


class EstimateShippingInputDataSchema(Schema):
    """"EstimateShippingInput schema"""
    product_id = ObjectId(required=True)
    units = fields.Int(required=True)

    @post_load
    def make_estimate_input_data(self, data):
        """Maskes an EstimateInputData object from a dict"""
        return EstimateShippingInputData(data['product_id'], data['units'])


class OrderUserInfo:
    """OrderUSerInfo"""
    def __init__(self, username, email):
        self.username = username
        self.email = email


class OrderUserInfoSchema(Schema):
    """OrderUserInfo schema"""
    username = fields.Str(required=True)
    email = fields.Email(required=True)


class TrackingInfo:
    """TrackingInfo"""
    def __init__(self, tracking_id, status, update_at):
        self.id = tracking_id
        self.status = status
        self.updateat = update_at


class TrackingInfoSchema(Schema):
    """TackingInfo Schema"""
    id = fields.Int(required=True)
    status = fields.Str(required=True)
    updateat = fields.DateTime(required=True)

    @post_load
    def make_product_tracking_code(self, data):
        """Creates a TrackingInfo from data dictionary"""
        return TrackingInfo(data['id'], data['status'], data['updateat'])


class PaymentInfo:
    """Represents the order payment information"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class PaymentInfoSchema(Schema):
    """PaymentInfo schema"""
    payment_method = fields.Str(required=True, validate=validate.Length(
        min=1, error="Product name cannot be empty"))
    cardholder_name = fields.Str(validate=validate.Length(
        min=1, error="Cardholder name field cannot be empty"))
    card_number = fields.Str(validate=validate.Length(
        min=1, error="Card number field cannot be empty"))
    expiration_date = fields.Str(validate=validate.Length(
        min=1, error="Expiration date field cannot be empty"))
    security_code = fields.Str(validate=validate.Length(
        min=1, error="Security code field cannot be empty"))

    @post_load
    def make_payment_info(self, data):
        """creates a order object from data dictionary"""
        return PaymentInfo(**data)


class Order(BaseModel):
    """Order"""
    def __init__(self, **kwargs):
        self.buyer = None
        self.seller = None
        self.buyer_info = None
        self.seller_info = None
        self.total = None
        self.buyer_location = None
        self.product_location = None
        self.product_name = None
        self.units = None
        self.status = None
        self.shipping_cost = 0
        self.has_to_be_shipped = None
        self.products_total = 0
        self.last_status_update = None
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def prepare(self, product, buyer, seller):
        """Prepares an order from product, buyer and seller info"""
        self.buyer = buyer.uid
        self.seller = seller.uid
        self.buyer_info = OrderUserInfo(buyer.username, buyer.email)
        self.seller_info = OrderUserInfo(seller.username, seller.email)
        self.buyer_location = buyer.location
        self.product_location = product.location
        self.product_name = product.name
        self.products_total = product.price * self.units
        self.total = self.products_total + self.shipping_cost
        self.last_status_update = str(datetime.now())
        self.status = 'COMPRA REALIZADA'


class OrderSchema(Schema):
    """marshmallow order schema"""
    _id = ObjectId()
    product_id = ObjectId(required=True)
    product_name = fields.Str(validate=validate.Length(
        min=1, error="Product name cannot be empty"))
    units = fields.Int(required=True)
    unit_price = fields.Float()
    payment_info = fields.Nested(PaymentInfoSchema, required=True)
    datetime = fields.Str()
    buyer = fields.Str()
    seller = fields.Str()
    buyer_info = fields.Nested(OrderUserInfoSchema)
    seller_info = fields.Nested(OrderUserInfoSchema)
    buyer_location = fields.Nested(LocationSchema)
    product_location = fields.Nested(LocationSchema)
    total = fields.Float()
    tracking_number = fields.Int()
    status = fields.Str()
    last_status_update = fields.Str()
    rate = fields.Str()
    has_to_be_shipped = fields.Bool(required=True)
    shipping_cost = fields.Float()
    products_total = fields.Float()

    @validates('units')
    def validate_units(self, value):
        """Validates that order units are greater than zero"""
        if value <= 0:
            raise ValidationError("Order units must be greater than 0.")

    @validates('unit_price')
    def validate_unit_price(self, value):
        """Validates that order unit price is greater than zero"""
        if value <= 0:
            raise ValidationError("Order unit_price must be greater than 0.")

    @validates('total')
    def validate_total(self, value):
        """Validates that order total is greater than zero"""
        if value <= 0:
            raise ValidationError("Order total must be greater than 0.")

    @post_load
    def make_order(self, data):
        """creates a order object from data dictionary"""
        return Order(**data)
