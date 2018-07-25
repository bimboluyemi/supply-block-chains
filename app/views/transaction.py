from flask import Blueprint, render_template

transaction = Blueprint('transaction', __name__)


@transaction.route('/transaction/list')
def all_transactions():
    return render_template('transaction/list.html')


@transaction.route('/transaction/new', methods=['GET', 'POST'])
def create_transaction():
    return render_template('transaction/create.html')
