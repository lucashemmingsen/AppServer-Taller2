"""Product Services"""
from datetime import datetime
import bson
from appserver.models.product import ProductSchema
from appserver.models.question import QuestionSchema
from appserver.models.answer import AnswerSchema
from appserver.data.product_mapper import ProductMapper
from appserver.services.exceptions import NotFoundError, ForbiddenError
from appserver.models.query import ProductsQuerySchema


class ProductsService:
    """Product Services"""
    schema = ProductSchema()

    @classmethod
    def add_product(cls, product_json, uid):
        """Add product services:"""
        product_json['seller'] = uid
        product = cls.schema.load(product_json)
        product.published = str(datetime.now())
        return ProductMapper.insert(product)

    @classmethod
    def get_product_by_id(cls, product_id):
        """Get product by id services:"""
        product = ProductMapper.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product not found.")
        return cls.schema.dump(product)

    @classmethod
    def get_products(cls, filters=None):
        """Get products services: returns all the
         products that match with filters parameters"""

        query = None
        if filters is not None:
            products_query_schema = ProductsQuerySchema()
            query_builder = products_query_schema.load(filters)
            query = query_builder.get_query()
        ret = []
        products = ProductMapper.get_many(query)
        if not products:
            raise NotFoundError("No product matches the query.")
        for product in products:
            ret.append(cls.schema.dump(product))
        return ret

    @classmethod
    def delete_product(cls, uid, product_id):
        """Delete product services: deletes product product_id from user uid."""
        if cls._product_exists_and_belongs_to_user(uid, product_id):
            if not ProductMapper.delete_one_by_id(product_id):
                raise NotFoundError("Product not found.")
        return True

    @classmethod
    def add_question(cls, question_dict, product_id, uid):
        """Add question services: adds a question by the user with id uid to the product
        with id product_id. Returns the product with the added question."""
        question_schema = QuestionSchema()
        question = question_schema.load(question_dict)
        question.question_id = bson.ObjectId()
        question.uid = uid
        question.datetime = str(datetime.now())
        product = ProductMapper.add_question(product_id, question_schema.dump(question))
        if product is None:
            raise NotFoundError("Product not found.")
        return cls.schema.dump(product)

    @classmethod
    def add_answer(cls, answer_dict, product_id, question_id, uid):
        """Add answer services: adds an answer to question_id question in
         product_id product"""
        answer_schema = AnswerSchema()
        answer = answer_schema.load(answer_dict)
        answer.answer_id = bson.ObjectId()
        answer.uid = uid
        answer.datetime = str(datetime.now())
        product = ProductMapper.add_answer(product_id, question_id, answer_schema.dump(answer))
        if product is None:
            raise NotFoundError("Product not found.")
        return cls.schema.dump(product)

    @classmethod
    def buy(cls, seller_id, buyer_id, quantity):
        """Buy product services:"""
        pass

    @classmethod
    def _product_exists_and_belongs_to_user(cls, uid, product_id):
        """Checks if product exists and belongs to user."""
        product = ProductMapper.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product does not exist.")
        if product.seller != uid:
            raise ForbiddenError("User can only delete his own products")
        return True
