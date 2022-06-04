from dataclasses import dataclass
from email.policy import default
from ecommerce import db


@dataclass
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    activated = db.Column(db.Boolean, default=True)

    def __init__(self, id, username, email, password, activated):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.activated = activated

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def add_user(cls, username, email, password):
        user = cls(None, username, email, password, True)

        db.session.add(user)
        db.session.commit()

    @classmethod
    def update_user(cls, id, username, email, password):
        user = cls.query.filter_by(id=id).first()
        user.username = username
        user.email = email
        user.password = password
        db.session.commit()

    @classmethod
    def delete_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

    @classmethod
    def activate_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        user.activated = True
        db.session.commit()

    @classmethod
    def deactivate_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        user.activated = False
        db.session.commit()


@dataclass
class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mod = db.Column(db.Integer, default=0)

    def __init__(self, id, name, email, password, mod):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.mod = mod

    @classmethod
    def get_all_admins(cls):
        return cls.query.all()

    @classmethod
    def get_admin_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_admin_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def add_admin(cls, name, email, password):
        admin = cls(None, name, email, password, 0)
        db.session.add(admin)
        db.session.commit()

    @classmethod
    def update_admin(cls, id, name, email, password):
        admin = cls.query.filter_by(id=id).first()
        admin.name = name
        admin.email = email
        admin.password = password
        db.session.commit()

    @classmethod
    def delete_admin(cls, id):
        admin = cls.query.filter_by(id=id).first()
        db.session.delete(admin)
        db.session.commit()


@dataclass
class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def get_all_categories(cls):
        return cls.query.all()

    @classmethod
    def get_category_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def add_category(cls, name):
        category = cls(None, name)
        db.session.add(category)
        db.session.commit()

    @classmethod
    def update_category(cls, id, name):
        category = cls.query.filter_by(id=id).first()
        category.name = name
        db.session.commit()

    @classmethod
    def delete_category(cls, id):
        category = cls.query.filter_by(id=id).first()
        db.session.delete(category)
        db.session.commit()


@dataclass
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    oldPrice = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    stock = db.Column(db.Integer, default=20)

    def __init__(self, id, name, price, oldPrice, description, category_id, image, stock):
        self.id = id
        self.name = name
        self.price = price
        self.oldPrice = oldPrice
        self.description = description
        self.category_id = category_id
        self.image = image
        self.stock = stock

    @classmethod
    def get_all_products(cls):
        return cls.query.all()

    @classmethod
    def get_product_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def add_product(cls, name, price, oldPrice, description, category_id, image, stock):
        product = cls(None, name, price, oldPrice, description, category_id, image, stock)
        db.session.add(product)
        db.session.commit()

    @classmethod
    def update_product(cls, id, name, price, oldPrice, description, category_id, image, stock):
        product = cls.query.filter_by(id=id).first()
        product.name = name
        product.price = price
        product.oldPrice = oldPrice
        product.description = description
        product.category_id = category_id
        product.image = image
        product.stock = stock

        db.session.commit()

    @classmethod
    def delete_product(cls, id):
        product = cls.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()

    @classmethod
    def get_products_for_category(cls, category_id):
        return cls.query.filter_by(category_id=category_id).all()
