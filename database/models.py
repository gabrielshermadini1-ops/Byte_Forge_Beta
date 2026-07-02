from .db import db
from flask_login import UserMixin



class Gpu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String, nullable=False)
    used_stat = db.Column(db.String(50), nullable=False)
    power_watt = db.Column(db.Float, nullable=False)
    power_score = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300),nullable = False)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),nullable = False,unique = True)
    email = db.Column(db.String(120),nullable = False,unique = True)
    password = db.Column(db.String(230),nullable = False)
    is_admin = db.Column(db.Boolean,default = False)
   




class Cpu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String, nullable=False)
    used_stat = db.Column(db.String(50), nullable=False)
    power_watt = db.Column(db.Float, nullable=False)
    power_score = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300),nullable = False)
     

class MotherBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String, nullable=False)
    used_stat = db.Column(db.String(50), nullable=False)
    power_watt = db.Column(db.Float, nullable=False)
    power_score = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300),nullable = False)


class PowerSuplly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String, nullable=False)
    used_stat = db.Column(db.String(50), nullable=False)
    power_watt = db.Column(db.Float, nullable=False)
    power_score = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300),nullable = False)

class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String, nullable=False)
    used_stat = db.Column(db.String(50), nullable=False)
    power_watt = db.Column(db.Float, nullable=False)
    power_score = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300),nullable = False)



class Ram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String, nullable=False)
    used_stat = db.Column(db.String(50), nullable=False)
    power_watt = db.Column(db.Float, nullable=False)
    power_score = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300),nullable = False)


class UserCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    part_type = db.Column(db.String(20))  
    part_id = db.Column(db.Integer)       

    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(300))
     
class PreBuiltPc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    image_url = db.Column(db.String(300))

    gpu_id = db.Column(db.Integer, db.ForeignKey('gpu.id'), nullable=True)
    cpu_id = db.Column(db.Integer, db.ForeignKey('cpu.id'), nullable=True)
    board_id = db.Column(db.Integer, db.ForeignKey('mother_board.id'), nullable=True)
    ram_id = db.Column(db.Integer, db.ForeignKey('ram.id'), nullable=True)
    psu_id = db.Column(db.Integer, db.ForeignKey('power_suplly.id'), nullable=True)
    storage_id = db.Column(db.Integer, db.ForeignKey('storage.id'), nullable=True)


    total_price = db.Column(db.Float)
    total_score = db.Column(db.Float)