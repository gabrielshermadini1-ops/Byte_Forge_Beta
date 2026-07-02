from flask import Flask,render_template,Blueprint,request,redirect,session
from database.models import Gpu,Cpu,User
from database.models import MotherBoard
from database.models import UserCart
from database.models import PowerSuplly
from database.models import Ram
from database.models import Storage
from database.models import PreBuiltPc

from main import app
from flask import flash
from database.db import db
from flask_login import login_user,login_required,current_user,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from flask import abort

@app.route("/")
def firstPage():
    if current_user.is_authenticated:
        return redirect("/home")
    return redirect("/login")




@app.route("/gpu-shop")
@login_required
def seed_gpus():
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    
    min_year = request.args.get("min_year",type = int)
    max_year = request.args.get("max_year",type = int)


    query = Gpu.query

    if min_price is not None:
        query = query.filter(Gpu.price >= min_price)
    if max_price is not None:
        query = query.filter(Gpu.price <= max_price)
    if min_year is not None:
        query = query.filter(Gpu.release_date >= str(int(min_year)))
    if max_year is not None:
        query = query.filter(Gpu.release_date <=str(int(max_year)))
    all_gpus = query.all()
    overall_max = db.session.query(db.func.max(Gpu.price)).scalar() or 0
    overall_max_year = db.session.query(db.func.max(Gpu.release_date)).scalar() or "2026"
    overall_min_year = db.session.query(db.func.min(Gpu.release_date)).scalar() or "2014"

    return render_template("gpu.html", gpus=all_gpus, min_price=min_price, max_price=max_price,min_year = min_year,max_year=max_year, overall_max=overall_max,overall_max_year = overall_max_year,overall_min_year = overall_min_year)

@app.route("/cpu-shop")
@login_required
def seed_cpus():
    min_price_cpu = request.args.get("min_price_cpu", type=float)
    max_price_cpu = request.args.get("max_price_cpu", type=float)

    min_year_cpu = request.args.get("min_year_cpu", type=int)
    max_year_cpu = request.args.get("max_year_cpu", type=int)

    query_cpu = Cpu.query

    if min_price_cpu is not None:
        query_cpu = query_cpu.filter(Cpu.price >= min_price_cpu)

    if max_price_cpu is not None:
        query_cpu = query_cpu.filter(Cpu.price <= max_price_cpu)

    if min_year_cpu is not None:
        query_cpu = query_cpu.filter(Cpu.release_date >= str(min_year_cpu))

    if max_year_cpu is not None:
        query_cpu = query_cpu.filter(Cpu.release_date <= str(max_year_cpu))

    all_cpus = query_cpu.all()
    overall_max = db.session.query(db.func.max(Cpu.price)).scalar() or 0
    overall_max_year = db.session.query(db.func.max(Cpu.release_date)).scalar() or "2026"
    overall_min_year = db.session.query(db.func.min(Cpu.release_date)).scalar() or "2014"
    return render_template ("cpu.html",cpus = all_cpus,min_price_cpu = min_price_cpu, max_price_cpu =max_price_cpu,min_year_cpu = min_year_cpu,max_year_cpu = max_year_cpu, overall_max = overall_max,overall_max_year = overall_max_year,overall_min_year = overall_min_year)
@app.route("/board-shop")
@login_required
def seed_boards():
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    
    min_year = request.args.get("min_year",type = int)
    max_year = request.args.get("max_year",type = int)


    query = MotherBoard.query

    if min_price is not None:
        query = query.filter(MotherBoard.price >= min_price)
    if max_price is not None:
        query = query.filter(MotherBoard.price <= max_price)
    if min_year is not None:
        query = query.filter(MotherBoard.release_date >= str(int(min_year)))
    if max_year is not None:
        query = query.filter(MotherBoard.release_date <=str(int(max_year)))
    all_boards = query.all()
    overall_max = db.session.query(db.func.max(MotherBoard.price)).scalar() or 0
    overall_max_year = db.session.query(db.func.max(MotherBoard.release_date)).scalar() or "2026"
    overall_min_year = db.session.query(db.func.min(MotherBoard.release_date)).scalar() or "2014"

    return render_template("motherbaord.html", boards= all_boards , min_price=min_price, max_price=max_price,min_year = min_year,max_year=max_year, overall_max=overall_max,overall_max_year = overall_max_year,overall_min_year = overall_min_year)

@app.route("/pc-build")
@login_required
def pc_build():
    builds = session.get('builds', {'build_1': {}, 'build_2': {}})

    def resolve(build_dict):
        gpu     = Gpu.query.get(build_dict.get('gpu'))         if build_dict.get('gpu')     else None
        cpu     = Cpu.query.get(build_dict.get('cpu'))         if build_dict.get('cpu')     else None
        board   = MotherBoard.query.get(build_dict.get('board')) if build_dict.get('board') else None
        ram     = Ram.query.get(build_dict.get('ram'))         if build_dict.get('ram')     else None
        psu     = PowerSuplly.query.get(build_dict.get('psu')) if build_dict.get('psu')     else None
        storage = Storage.query.get(build_dict.get('storage')) if build_dict.get('storage') else None

        parts = [gpu, cpu, board, ram, psu, storage]
        return {
            'gpu': gpu, 'cpu': cpu, 'board': board,
            'ram': ram, 'psu': psu, 'storage': storage,
            'total_score': round( sum(p.power_score for p in parts if p)),
            'total_price': round(sum(p.price for p in parts if p)),
        }

    build_1 = resolve(builds['build_1'])
    build_2 = resolve(builds['build_2'])
    return render_template("build.html", build_1=build_1, build_2=build_2)

@app.route("/register",methods = ["GET","POST"])
def register_page():
    if request.method == "POST":
        user_name = request.form.get("usernameInput")
        user_pass = request.form.get("exampleInputPassword1")
        user_em = request.form.get("exampleInputEmail1")
        

        existed_user = User.query.filter(
            (User.username == user_name) | (User.email == user_em)
        ).first()

        if existed_user:
            flash("Username or Email already taken!","danger")
            return redirect("/register")
        

        hashed_pass = generate_password_hash(user_pass)

        new_user = User(username = user_name,email = user_em,password = hashed_pass)
         
        if user_name == "admina":
            new_user.is_admin = True 


        db.session.add(new_user)
        db.session.commit()
        
        return redirect ("/")
    
    return render_template ("register.html")


@app.route("/use-part/<string:part_type>/<int:part_id>/<int:slot>")
@login_required
def use_part(part_type, part_id, slot):

    builds = session.get('builds', {'build_1': {}, 'build_2': {}})

    build_key = f'build_{slot}'
    build = builds.get(build_key, {})

    build[part_type] = part_id
    builds[build_key] = build

    session['builds'] = builds
    session.modified = True

    return redirect(request.referrer) 


@app.route("/login",methods = ["GET","POST"])
def login_page():
    if request.method == "POST":
        usernameInput = request.form.get("usernameInput")
        userpassInput = request.form.get("exampleInputPassword1")
        

        user = User.query.filter_by(username = usernameInput).first()

        if user and check_password_hash(user.password,userpassInput):
            login_user (user)
            return render_template("home_page.html")   
        else: 
            flash("Invalid username or password","danger")
            return redirect("/login")

    return render_template("login.html")   

@app.route("/remove-part/<string:part_type>/<int:slot>")
@login_required
def remove_part(part_type, slot):
    if 'builds' in session:
        session['builds'][f'build_{slot}'].pop(part_type, None)
        session.modified = True
    return redirect("/pc-build")

@app.route("/clear-build/<int:slot>")
@login_required
def clear_build(slot):
    if 'builds' in session:
        session['builds'][f'build_{slot}'] = {}
        session.modified=True

    return redirect("/pc-build")    

@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect("/login")    


@app.route("/cart")
@login_required
def cart():
    cart_items = UserCart.query.filter_by(user_id=current_user.id).all()

    products = []

    for item in cart_items:
        product = None

        if item.part_type == "gpu":
            product = Gpu.query.get(item.part_id)
        elif item.part_type == "cpu":
            product = Cpu.query.get(item.part_id)
        elif item.part_type == "board":
            product = MotherBoard.query.get(item.part_id)

        elif item.part_type == "ram":
            product = Ram.query.get(item.part_id)   

        elif item.part_type == "psu":
            product = PowerSuplly.query.get(item.part_id) 

        elif item.part_type == "storage":
            product = Storage.query.get(item.part_id)    



        if product:
            products.append({
                "name": product.name,
                "price": product.price,
                "image_url": product.image_url,
                "type": item.part_type,
                "cart_id":item.id
            })
    total_price = sum(p["price"] for p in products)
    return render_template("cart.html", products=products,total = total_price)


@app.route("/add-to-cart/<string:part_type>/<int:part_id>")
@login_required
def add_to_cart(part_type, part_id):

    if part_type == "gpu":
        product = Gpu.query.get(part_id)
    elif part_type == "cpu":
        product = Cpu.query.get(part_id)
    elif part_type == "board":
        product = MotherBoard.query.get(part_id)
    elif part_type == "ram":
        product = Ram.query.get(part_id)
    elif part_type == "psu":
        product = PowerSuplly.query.get(part_id)
    elif part_type == "storage":
        product = Storage.query.get(part_id)
    else:
        return redirect(request.referrer)

    item = UserCart(
        user_id=current_user.id,
        part_type=part_type,
        part_id=part_id,
        name=product.name,
        price=product.price,
        image_url=product.image_url
    )

    db.session.add(item)
    db.session.commit()

    return redirect("/cart")


@app.route("/add-build-to-cart/<int:slot>")
@login_required
def add_build_to_cart(slot):

    builds = session.get('builds') or {}

    build = builds.get(f'build_{slot}')

    if not build:
        print("EMPTY BUILD!")
        return redirect("/pc-build")

    mapping = {
        "gpu": Gpu,
        "cpu": Cpu,
        "board": MotherBoard,
        "ram" :Ram,
        "psu":PowerSuplly,
        "storage":Storage
    }

    print("BUILD FROM SESSION:", build)

    for part_type, model in mapping.items():
        part_id = build.get(part_type)

        print(part_type, part_id)

        if not part_id:
            continue

        product = model.query.get(part_id)

        print("FOUND PRODUCT:", product)

        if not product:
            continue

        db.session.add(UserCart(
            user_id=current_user.id,
            part_type=part_type,
            part_id=part_id,
            name=product.name,
            price=product.price,
            image_url=product.image_url
        ))

    db.session.commit()

    print("BUILD ADDED SUCCESSFULLY")

    return redirect("/cart")



@app.route("/remove-from-cart/<int:item_id>")
@login_required

def remove_Product_From_Cart(item_id):
    item  = UserCart.query.get(item_id)
    if item and item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()

    return redirect("/cart")    



@app.route("/home")
@login_required
def home():
    return render_template("home_page.html")




def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)

        return f(*args, **kwargs)
    return decorated     


@app.route("/admin")
@login_required
@admin_required
def admin_panel():
    gpus = Gpu.query.all()
    cpus = Cpu.query.all()
    boards = MotherBoard.query.all()
    rams = Ram.query.all()
    psus = PowerSuplly.query.all()
    storages = Storage.query.all()
    all_users = User.query.all()
    return render_template("admin.html",gpus = gpus, cpus = cpus, boards = boards,rams = rams,psus = psus,storages=storages,users = all_users)



@app.route("/admin/add/<string:part_type>",methods = ["GET","POST"])
@login_required
@admin_required
def admin_add(part_type):
    if request.method == "POST":
        data = {
            "name":request.form.get("name"),
            "price":float(request.form.get("price")),
            "brand": request.form.get("brand"),
            "release_date":request.form.get("release_date"),
            "used_stat":request.form.get("used_stat"),
            "power_watt":float(request.form.get("power_watt")),
            "power_score":float(request.form.get("power_score")),
            "image_url": request.form.get("image_url"),
        }
        models = {"gpu":Gpu, "cpu":Cpu,"board":MotherBoard,"ram":Ram,"psu":PowerSuplly,"storage":Storage}
        db.session.add(models[part_type](**data))
        db.session.commit()
        return redirect("/admin")
    return render_template("admin_form.html",part_type = part_type, product = None)


@app.route("/admin/edit/<string:part_type>/<int:part_id>",methods = ["GET","POST"])
@login_required
@admin_required
def admin_edit(part_type,part_id):
     model = {"gpu":Gpu, "cpu":Cpu,"board":MotherBoard,"ram":Ram,"psu":PowerSuplly,"storage":Storage}[part_type]
     product = model.query.get_or_404(part_id)
     if request.method == "POST":
        product.name         = request.form.get("name")
        product.price        = float(request.form.get("price"))
        product.brand        = request.form.get("brand")
        product.release_date = request.form.get("release_date")
        product.used_stat    = request.form.get("used_stat")
        product.power_watt   = float(request.form.get("power_watt"))
        product.power_score  = float(request.form.get("power_score"))
        product.image_url    = request.form.get("image_url")
        db.session.commit()
        return redirect("/admin")
     return render_template("admin_form.html",part_type = part_type,product = product)












@app.route("/admin/delete/<string:part_type>/<int:part_id>")
@login_required
@admin_required
def admin_delete(part_type,part_id):
    model = {"gpu":Gpu, "cpu":Cpu,"board":MotherBoard,"ram":Ram,"psu":PowerSuplly,"storage":Storage}[part_type]
    product = model.query.get_or_404(part_id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/admin")



@app.route("/ram-shop")
@login_required
def seed_rams():
    min_price = request.args.get("min_price",type=float)
    max_price = request.args.get("max_price",type=float)
    min_year = request.args.get("min_year",type=int)
    max_year = request.args.get("max_year",type=int)
    
    
    query = Ram.query


    if min_price is not None:
        query = query.filter(Ram.price >= min_price)
    if max_price is not None:
        query = query.filter(Ram.price <= max_price)
    if min_year is not None:
        query = query.filter(Ram.release_date >= str(min_year))
    if max_year is not None:
        query = query.filter(Ram.release_date <= str(max_year))

    all_rams = query.all()
    overall_max = db.session.query(db.func.max(Ram.price)).scalar() or 0
    overall_max_year = db.session.query(db.func.max(Ram.release_date)).scalar() or "2026"
    overall_min_year = db.session.query(db.func.min(Ram.release_date)).scalar() or "2014"
    return render_template("ram.html", rams=all_rams, min_price=min_price, max_price=max_price,
                           min_year=min_year, max_year=max_year, overall_max=overall_max,
                           overall_max_year=overall_max_year, overall_min_year=overall_min_year)    
@app.route("/pcu-shop")
@login_required
def seed_pcu():
    min_price = request.args.get("min_price",type=float)
    max_price = request.args.get("max_price",type=float)
    min_year = request.args.get("min_year",type=float)
    max_year = request.args.get("max_year",type=float)

    query = PowerSuplly.query

    if min_price is not None:
        query = query.filter(PowerSuplly.price >= min_price)
    if max_price is not None:
        query = query.filter(PowerSuplly.price <= max_price)
    if min_year is not None:
        query = query.filter(PowerSuplly.release_date >= str(min_year))
    if max_year is not None:
        query = query.filter(PowerSuplly.release_date <= str(max_year))

    all_psu = query.all()
    overall_max = db.session.query(db.func.max(PowerSuplly.price)).scalar() or 0
    overall_max_year = db.session.query(db.func.max(PowerSuplly.release_date)).scalar() or "2026"
    overall_min_year = db.session.query(db.func.min(PowerSuplly.release_date)).scalar() or "2014"
    return render_template("pcu.html", pcus=all_psu, min_price=min_price, max_price=max_price,
                           min_year=min_year, max_year=max_year, overall_max=overall_max,
                           overall_max_year=overall_max_year, overall_min_year=overall_min_year)    
@app.route("/storage-shop")
@login_required
def seed_storage():
    min_price = request.args.get("min_price",type=float)
    max_price = request.args.get("max_price",type=float)
    min_year = request.args.get("min_year",type=float)
    max_year = request.args.get("max_year",type=float)

    query = Storage.query

    if min_price is not None:
        query = query.filter(Storage.price >= min_price)
    if max_price is not None:
        query = query.filter(Storage.price <= max_price)
    if min_year is not None:
        query = query.filter(Storage.release_date >= str(min_year))
    if max_year is not None:
        query = query.filter(Storage.release_date <= str(max_year))

    all_storages = query.all()
    overall_max = db.session.query(db.func.max(Storage.price)).scalar() or 0
    overall_max_year = db.session.query(db.func.max(Storage.release_date)).scalar() or "2026"
    overall_min_year = db.session.query(db.func.min(Storage.release_date)).scalar() or "2014"
    return render_template("storage.html", storages=all_storages, min_price=min_price, max_price=max_price,
                           min_year=min_year, max_year=max_year, overall_max=overall_max,
                           overall_max_year=overall_max_year, overall_min_year=overall_min_year)    




@app.route("/about-page")
@login_required
def seed_about():
    return render_template("about.html")





@app.route("/admin/give_admin/<int:user_id>")
@login_required
@admin_required
def give_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    return redirect("/admin")


@app.route("/admin/delete_user/<int:user_id>")
@login_required
@admin_required
def del_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You Cant Delete your own Account!","warning")
        return redirect("/admin")
    UserCart.query.filter_by(user_id = user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return redirect("/admin")



@app.route("/all_products")
@login_required

def see_all():
    gpus = Gpu.query.all()
    cpus = Cpu.query.all()
    boards = MotherBoard.query.all()
    rams = Ram.query.all()
    psus = PowerSuplly.query.all()
    storage = Storage.query.all()
    return render_template("allProducts.html",gpus = gpus, cpus = cpus, boards = boards, rams = rams, psus = psus, storage = storage)


@app.route("/prebuilt-shop")
@login_required
def prebuilt_shop():
    builds = PreBuiltPc.query.all()
    return render_template("prebuilt.html",builds = builds)

@app.route("/add-prebuilt-to-cart/<int:build_id>")
@login_required
def add_prebuilt_to_cart(build_id):
    build = PreBuiltPc.query.get_or_404(build_id)
    mapping = {
        "gpu":(Gpu, build.gpu_id),
        "cpu":(Cpu, build.cpu_id),
        "board":(MotherBoard, build.board_id),
        "ram":(Ram, build.ram_id),
        "psu":(PowerSuplly, build.psu_id),
        "storage":(Storage, build.storage_id),
    }

    for part_type,(model,part_id) in mapping.items():
        if not part_id:
            continue
        product = model.query.get(part_id)
        if product:
            db.session.add(UserCart(
                user_id = current_user.id,
                part_type = part_type,
                part_id = part_id,
                name = product.name,
                price = product.price,
                image_url = product.image_url 
                ))
    db.session.commit()
    return redirect("/cart")    
