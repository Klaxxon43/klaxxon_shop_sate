from flask import render_template, redirect, flash, url_for, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from . import user_bp
from ..models.User import Users, Item, Message
from ..models import db
from ..forms import RegistrationForm, LoginForm, ItemForm, IncreaseBasketForm, DecreaseBasketForm, RemoveFromBasketForm
from .mail import send_mail
import os
import json
from datetime import datetime

bcrypt = Bcrypt()

@user_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(login=form.login.data, password=hashed_password, email=form.email.data, money=0, basket='', )
        try:
            status_mail = send_mail(form.email.data)
            if status_mail == 'good':
                db.session.add(user)
                db.session.commit()
                flash(f'Регистрация пройдена! {form.login.data}, вы успешно зарегистрировались', 'success')
                return redirect(url_for('user.login'))
            else:
                flash('Неверная почта, попробуйте ещё раз', 'danger')
        except Exception as e:
            print(e)
            flash(f'При регистрации произошла ошибка', 'danger')
    return render_template('register.html', form=form, show_header=True)

@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Добро пожаловать, {form.login.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form, show_header=True)

@user_bp.route('/shop', methods=['POST', 'GET'])
def shop():
    bp_plus = url_for('static', filename='img/BP+.png')
    bp = url_for('static', filename='img/BP.png')
    gems170 = url_for('static', filename='img/170gems.png')
    gems30 = url_for('static', filename='img/30gems.png')
    gems80 = url_for('static', filename='img/80gems.png')
    gems360 = url_for('static', filename='img/360gems.png')
    gems950 = url_for('static', filename='img/950gems.png')
    gems2000 = url_for('static', filename='img/2000gems.png')
    items = Item.query.filter(Item.creator_id != current_user.id).all()
    users = Users.query.filter(Users.id != current_user.id).all()
    return render_template('shop.html', show_footer=True, show_header=True, bp_plus=bp_plus, bp=bp, gems170=gems170, gems30=gems30, gems80=gems80, gems950=gems950, gems360=gems360, gems2000=gems2000, items=items, users=users)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('index'))

@user_bp.route('/profile')
@login_required
def profile():
    user = Users.query.get_or_404(current_user.id)
    created_items = Item.query.filter_by(creator_id=user.id).all()
    return render_template('profile.html', user=user, created_items=created_items, show_header=True, show_footer=True)

@user_bp.route('/add_item', methods=['POST', 'GET'])
@login_required
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        if form.image_url.data:
            f = form.image_url.data
            filename = secure_filename(f.filename)
            filepath = os.path.join(current_app.root_path, 'static/img', filename)
            try:
                f.save(filepath) # Сохраняем файл
                item = Item(
                    name=form.name.data,
                    price=form.price.data,
                    image_url=filename,
                    description=form.description.data,
                    game=form.game.data,
                    category=form.category.data,
                    delivery=form.delivery.data,
                    creator_id=current_user.id # Сохраняем ID текущего пользователя
                )
                db.session.add(item)
                db.session.commit()
                flash('Товар добавлен', 'success')
                return redirect(url_for('user.shop'))
            except OSError as e:
                print(f"Ошибка при сохранении файла: {e}")
                flash('Ошибка при загрузке изображения', 'danger')
        else:
            flash('Необходимо выбрать изображение', 'danger')
    else:
        print('Ошибки в форме:', form.errors)
    return render_template('add_item.html', form=form, show_footer=False, show_header=True)

@user_bp.route('/item/<int:item_id>')
def item_info(item_id):
    item = Item.query.get_or_404(item_id) # Получаем товар по id
    return render_template('item_info.html', item=item, show_footer=True, show_header=True)

@user_bp.route('/item/<int:item_id>/buy', methods=['POST', 'GET'])
@login_required
def buy(item_id):
    item = Item.query.get_or_404(item_id)
    if item.creator_id == current_user.id:
        return jsonify({'message': 'Вы не можете купить свой товар'}), 403
    try:
        print(f"Получен запрос на добавление товара с ID: {item_id}")
        user = Users.query.filter_by(id=current_user.id).first()
        if user:
            user.add_to_basket(item_id)
            db.session.commit()  # Не забудьте сохранить изменения в базе данных
            return jsonify({'message': 'Товар добавлен в корзину!', 'item_id': item_id})
        else:
            return jsonify({'message': 'Пользователь не авторизован'}), 401
    except Exception as e:  # Все остальные исключения
        current_app.logger.exception(f"Ошибка при добавлении товара в корзину: {e}")
        return jsonify({'message': 'Ошибка сервера'}), 500

import json

@user_bp.route('/basket')
@login_required
def basket():
    user = Users.query.get_or_404(current_user.id)
    basket_items = json.loads(user.basket) if user.basket else []
    item_counts = {item_id: basket_items.count(item_id) for item_id in set(basket_items)}
    items = Item.query.filter(Item.id.in_(item_counts.keys())).all()
    increase_form = IncreaseBasketForm() # Создаем экземпляр формы IncreaseBasketForm
    decrease_form = DecreaseBasketForm() # Создаем экземпляр формы DecreaseBasketForm
    remove_form = RemoveFromBasketForm() # Создаем экземпляр формы RemoveFromBasketForm
    return render_template('basket.html', items=items, item_counts=item_counts, increase_form=increase_form, decrease_form=decrease_form, remove_form=remove_form, show_header=True)

@user_bp.route('/basket/update/<int:item_id>', methods=['POST', 'GET'])
@login_required
def update_basket(item_id):
    action = request.form.get('action')
    user = Users.query.get_or_404(current_user.id)
    if action == 'increase':
        user.add_to_basket(item_id)
    elif action == 'decrease':
        user.update_basket_item(item_id, max(0, user.basket.count(str(item_id)) - 1))
    db.session.commit()
    return redirect(url_for('user.basket'))

@user_bp.route('/basket/remove/<int:item_id>', methods=['POST', 'GET'])
@login_required
def remove_from_basket(item_id):
    user = Users.query.get_or_404(current_user.id)
    user.remove_from_basket(item_id)
    db.session.commit()
    return redirect(url_for('user.basket'))

@user_bp.route('/pay/<int:item_id>', methods=['GET'])
@login_required
def pay(item_id):
    item = Item.query.get_or_404(item_id)
    creator_id = item.creator_id
    return redirect(url_for('user.chat', creator_id=creator_id))

@user_bp.route('/chats', methods=['GET'])
@login_required
def chats():
    users = Users.query.filter(Users.id != current_user.id).all()
    return render_template('chats.html', users=users, user=current_user, show_header=True, show_footer=True)

@user_bp.route('/chat/<int:creator_id>', methods=['GET'])
@login_required
def chat(creator_id):
    creator = Users.query.get_or_404(creator_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == creator_id)) |
        ((Message.sender_id == creator_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()
    users = Users.query.filter(Users.id != current_user.id).all()
    return render_template('chats.html', users=users, user=current_user, creator=creator, messages=messages, show_header=True, show_footer=True)


@user_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    message_content = request.form.get('message')
    receiver_id = request.form.get('receiver_id')
    file = request.files.get('file')
    file_url = None

    if not receiver_id:
        return jsonify({'error': 'Receiver ID is required'}), 400

    if file:
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, 'static/uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        file_url = url_for('static', filename='uploads/' + filename)

    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=message_content,
        file_url=file_url,
        timestamp=datetime.utcnow()
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'file_url': file_url
    })

@user_bp.route('/get_messages/<int:creator_id>', methods=['GET'])
@login_required
def get_messages(creator_id):
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == creator_id)) |
        ((Message.sender_id == creator_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return jsonify([{
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'file_url': message.file_url
    } for message in messages])
