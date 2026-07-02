from flask import Flask, render_template
from database.db import db
from flask_login import LoginManager
from database.models import Gpu
from database.products.gpu import gpus
from database.products.mother_boards import boards
# პროცესორები
from database.models import Cpu,MotherBoard,Ram,PowerSuplly,Storage
from database.models import User
# from database.products.gpu import cpus
from database.products.cpu_db import cpus
from database.products.Ram import rams
from database.products.powerSuply import powers
from database.products.storage import storages
from database.models import PreBuiltPc
from pre_built import prebuilt_pcs


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SECRET_KEY"] = "5559"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login = LoginManager(app)
login.login_view = "login_page"
db.init_app(app)
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import *
with app.app_context():
    db.create_all()
    if not Gpu.query.first():
        for i in gpus:
            db.session.add(Gpu(**i))
        db.session.commit() 

    if not Cpu.query.first():
        for u  in cpus:
            db.session.add(Cpu(**u))
        db.session.commit()    


    if not MotherBoard.query.first():
        for u  in boards:
            db.session.add(MotherBoard(**u))
        db.session.commit() 


    if not Ram.query.first():
        for u  in rams:
            db.session.add(Ram(**u))
        db.session.commit()    


    if not Storage.query.first():
        for u  in storages:
            db.session.add(Storage(**u))
        db.session.commit()

    if not PowerSuplly.query.first():
        for u  in powers:
            db.session.add(PowerSuplly(**u))
        db.session.commit()

    def get_id_by_name(model, name):
        item = model.query.filter_by(name=name).first()
        if not item:
            print(f" Missing in DB: {name} ({model.__name__})")
            return None
        return item.id if item else None
    

   

    if not PreBuiltPc.query.first():

        gpu_map = {g.name: g.id for g in Gpu.query.all()}
        cpu_map = {c.name: c.id for c in Cpu.query.all()}
        board_map = {b.name: b.id for b in MotherBoard.query.all()}
        ram_map = {r.name: r.id for r in Ram.query.all()}
        psu_map = {p.name: p.id for p in PowerSuplly.query.all()}
        storage_map = {s.name: s.id for s in Storage.query.all()}

        for pc in prebuilt_pcs:

            gpu_id = gpu_map.get(pc["gpu"])
            cpu_id = cpu_map.get(pc["cpu"])
            board_id = board_map.get(pc["board"])
            ram_id = ram_map.get(pc["ram"])
            psu_id = psu_map.get(pc["psu"])
            storage_id = storage_map.get(pc["storage"])

            if None in [gpu_id, cpu_id, board_id, ram_id, psu_id, storage_id]:
                print(f" Skipping: {pc['name']}")
                continue

            db.session.add(PreBuiltPc(
                name=pc["name"],
                description=pc["description"],
                image_url=pc["image_url"],

                gpu_id=gpu_id,
                cpu_id=cpu_id,
                board_id=board_id,
                ram_id=ram_id,
                psu_id=psu_id,
                storage_id=storage_id,

                total_price=pc["total_price"],
                total_score=pc["total_score"]
            ))

    db.session.commit()
 

        


if __name__ == '__main__':
    app.run(debug=True,host = "0.0.0.0")
 

        

