import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from ..forms import CreateTransactionForm
from ..services.transaction_object import Transaction
from ..services.transaction_services import fetch_user_transactions, post_transaction
from ..services.user_services import get_users_in_role
from ..constants import INITIATED, SUPPLIER, RETAILER
from ..utils import timestamp_to_string

transaction = Blueprint('transaction', __name__)


@login_required
@transaction.route('/transaction/list', methods=['GET'])
def all_transactions():
    tx = fetch_user_transactions(current_user)
    can_order = (current_user.user_role == RETAILER)
    return render_template('transaction/list.html', title='Transactions', transactions=tx, can_order=can_order)


@login_required
@transaction.route('/transaction/new', methods=['GET', 'POST'])
def create_transaction():
    message = ''
    form = CreateTransactionForm()
    form.supplier.choices = [(users.company, users.company) for users in get_users_in_role(SUPPLIER)]
    if form.validate_on_submit():
        new_tx = Transaction(block_type=INITIATED, actor_public_key=current_user.public_key,
                             actor_private_key=current_user.private_key, actor=current_user.company,
                             supplier=form.supplier.data, item=form.item.data, quantity=form.quantity.data)
        new_tx.signature = new_tx.sign_transaction()
        try:
            result = post_transaction(new_tx)
        except:
            result = False
        if result:
            flash('Order has been successfully created.')
            return redirect(url_for('transaction.all_transactions'))
        else:
            message = 'An error occurred.'
    return render_template('transaction/create.html', form=form, message=message)


@login_required
@transaction.route('/transaction/details', methods=['GET'])
def view_transaction():
    return ""




