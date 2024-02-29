from app import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from functools import wraps
from datetime import date, datetime
from models import Auction, Item

bp = Blueprint('auction', __name__, url_prefix='/auction')


@bp.route('/')
def index():
    return render_template('auction/index.html')

@bp.route('/show_sort_date', methods=['GET', 'POST'])
def show_sort_date():
    if request.method == 'POST':
        form_data = None
        try:
            form_data = {
                "start": datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
                "end": datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date(),
            }
            auctions_data = Auction.query.filter(
                form_data["start"] <= Auction.date
            ).filter(
                Auction.date <= form_data["end"]
            ).all()
            if not auctions_data:
                auctions_data = 'not_found'
            return render_template('auction/show_sort_date.html', auctions_data=auctions_data)
        except:
            flash('Введите корректный диапазон дат', 'danger')
    return render_template('auction/show_sort_date.html')


@bp.route('/show/<int:auction_id>')
def show(auction_id):
    auction = Auction.query.get(auction_id)
    items = Item.query.filter_by(auction_id=auction_id).all()
    return render_template('auction/show.html', auction=auction, items=items)


@bp.route('/show_total')
def show_total():
    auctions = Auction.query.all()
    data_list = []
    for auction in auctions:
        auction_id = auction.id
        items = Item.query.filter_by(auction_id=auction_id).all()
        sum = 0
        for item in items:
            if item.sale_price:
                sum += item.sale_price
        data_list.append({"auction": Auction.query.get(auction_id), "total": sum})
        data_list = sorted(data_list, key=lambda x: x['total'])
        data_list.reverse()
    return render_template('auction/show_all_total.html', data_list=data_list)


@bp.route('/<int:auction_id>/add_item', methods=["GET", "POST"])
def add(auction_id):
    if request.method == "POST":
        item = Item(
            auction_id=auction_id,
            starting_price=request.form.get('starting_price'),
            short_desc=request.form.get('short_desc').strip(),
            seller_id=current_user.id,
        )

        count_items = len(Item.query.filter_by(auction_id=auction_id).all())
        f_lot_number = "N-{number}"
        if count_items < 9:
            lot_number = f_lot_number.format(number="00"+str((count_items+1)))
        elif count_items < 99:
            lot_number = f_lot_number.format(number="0"+str((count_items+1)))
        else:
            lot_number = f_lot_number.format(number=str((count_items+1)))
        item.lot_number = lot_number
        try:
            db.session.add(item)
            db.session.commit()
            flash('Предмет успешно добавлен', "success")
            return redirect(url_for('auction.show', auction_id=auction_id))
        except:
            flash('Во время добавления предмета произошла ошибка...', "danger")
            db.session.rollback()
    auction = Auction.query.get(auction_id)
    return render_template('auction/add.html', auction=auction)
