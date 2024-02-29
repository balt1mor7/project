from app import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from functools import wraps
from datetime import date, datetime
from models import Auction, Item

bp = Blueprint('item', __name__, url_prefix='/item')


@bp.route('/show_sort_date', methods=['GET', 'POST'])
def show_sort_date():
    if request.method == 'POST':
        form_data = None
        try:
            form_data = {
                "start": datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
                "end": datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date(),
            }
            items_data = Item.query.filter(
                form_data["start"] <= Item.date_of_sale
            ).filter(
                Item.date_of_sale <= form_data["end"]
            ).all()
            if not items_data:
                items_data = 'not_found'
            return render_template('item/show_sort_date.html', items_data=items_data)
        except:
            flash('Введите корректный диапазон дат', 'danger')
    return render_template('item/show_sort_date.html')

@bp.route('/sale/<int:item_id>', methods=["GET", "POST"])
def sale_item(item_id):
    item = Item.query.get(item_id)
    if request.method == "POST":
        item.sale_price = request.form.get('sale_price')
        item.buyer_id = request.form.get('buyer_id')
        item.date_of_sale = date.today()
        try:
            db.session.commit()
            flash('Предмет успешно продан', "success")
            return redirect(url_for('auction.show', auction_id=item.auction.id))
        except:
            flash('Во время продажи предмета произошла ошибка...', "danger")
            db.session.rollback()
    buyers = User.query.all()
    return render_template('item/sale.html', item=item, buyers=buyers)