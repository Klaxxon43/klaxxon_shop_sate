from datetime import datetime
from . import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    money = db.Column(db.Integer, default=0)
    basket = db.Column(db.String, default='')
    profile_picture = db.Column(db.String, default='default.jpg')
    items = db.relationship('Item', backref='creator', lazy=True)  # Добавляем отношение для товаров

    def add_to_basket(self, item_id):
        import json
        try:
            basket = json.loads(self.basket) if self.basket else []
            basket.append(item_id)
            self.basket = json.dumps(basket)
            print(f"Товар с ID: {item_id} добавлен в корзину пользователя с ID: {self.id}")
        except Exception as e:
            print(f"Ошибка при добавлении товара в корзину: {e}")
            raise

    def update_basket_item(self, item_id, quantity):
        import json
        try:
            basket = json.loads(self.basket) if self.basket else []
            basket = [item for item in basket if item != item_id]  # Удаляем все вхождения item_id
            basket.extend([item_id] * quantity)  # Добавляем item_id нужное количество раз
            self.basket = json.dumps(basket)
        except Exception as e:
            print(f"Ошибка при обновлении товара в корзине: {e}")
            raise

    def remove_from_basket(self, item_id):
        import json
        try:
            basket = json.loads(self.basket) if self.basket else []
            basket = [item for item in basket if item != item_id]  # Удаляем все вхождения item_id
            self.basket = json.dumps(basket)
        except Exception as e:
            print(f"Ошибка при удалении товара из корзины: {e}")
            raise


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))  # URL картинки
    delivery = db.Column(db.String(100))  # способ доставки
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID создателя

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    file_url = db.Column(db.String(255), nullable=True)  # Добавляем поле для URL файла
    sender = db.relationship('Users', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('Users', foreign_keys=[receiver_id], backref='received_messages')
