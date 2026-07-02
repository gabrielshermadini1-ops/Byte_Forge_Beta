from models import PreBuiltPc
from db import db
from main import app

with app.app_context():

    build1 = PreBuiltPc(
        name="Budget Gaming PC",
        description="Sharp Razer Build",
        image_url="https://upload.wikimedia.org/wikipedia/commons/2/20/Avant-Tower-Gaming-PC.png",
        gpu_id=1,
        cpu_id=1,
        board_id=1,
        ram_id=1,
        psu_id=1,
        storage_id=1,
        total_price=1000,
        total_score=40
    )

    build2 = PreBuiltPc(
        name="Setup For Kids",
        description="Junior Play",
        image_url="https://static.vecteezy.com/system/resources/thumbnails/054/720/484/small/gaming-pc-on-white-background-on-transparent-background-png.png",
        gpu_id=2,
        cpu_id=2,
        board_id=2,
        ram_id=2,
        psu_id=2,
        storage_id=2,
        total_price=550,
        total_score=25
    )

    db.session.add(build1)
    db.session.add(build2)
    db.session.commit()