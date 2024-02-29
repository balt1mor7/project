from app import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from functools import wraps
from datetime import date, datetime
from models import Auction, Item

bp = Blueprint('buyer', __name__, url_prefix='/buyer')


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
            buyers_dict = {}
            if not items_data:
                buyers_dict = 'not_found'
            else:
                for item in items_data:
                    if item.buyer in buyers_dict:
                        buyers_dict[item.buyer] += item.sale_price
                    else:
                        buyers_dict[item.buyer] = item.sale_price
            return render_template('buyer/show_sort_date.html', buyers_dict=buyers_dict)
        except:
            flash('Введите корректный диапазон дат', 'danger')
    return render_template('buyer/show_sort_date.html')
