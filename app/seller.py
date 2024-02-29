from app import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from functools import wraps
from datetime import date, datetime
from models import Auction, Item

bp = Blueprint('seller', __name__, url_prefix='/seller')


@bp.route('/show_all_total', methods=['GET', 'POST'])
def show_all_total():
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
            sellers_dict = {}
            if not items_data:
                sellers_dict = 'not_found'
            else:
                for item in items_data:
                    if item.seller in sellers_dict:
                        sellers_dict[item.seller] += item.sale_price
                    else:
                        sellers_dict[item.seller] = item.sale_price
            return render_template('seller/show_all_total.html', sellers_dict=sellers_dict)
        except:
            flash('Введите корректный диапазон дат', 'danger')
    return render_template('seller/show_all_total.html')
