import binascii

import Cryptodome
import Cryptodome.Random
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5

from app import db
from app.models import User


def register_user(form):
    user = User(username=form.username.data, email=form.email.data, company=form.company.data)
    user.set_password(form.password.data)
    user.private_key, user.public_key = generate_user_keys()
    db.session.add(user)
    db.session.commit()


def generate_user_keys():
    random_gen = Cryptodome.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    return binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), \
           binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')


def sign_transaction(transaction, private_key):
    private_key = RSA.import_key(binascii.unhexlify(private_key))
    signer = PKCS1_v1_5.new(private_key)
    h = SHA.new(str(transaction).encode('utf8'))
    return binascii.hexlify(signer.sign(h)).decode('ascii')
