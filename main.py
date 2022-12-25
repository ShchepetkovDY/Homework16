import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import init_database
from models import User, Offer, Order

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # связь базы данных с приложением


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        result = []
        for user in User.query.all():
            result.append(user.get_dict())
        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )

        db.session.add(new_user)
        db.session.commit()

        return "Пользователь добавлен", 201


@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user(uid):
    if request.method == "GET":
        return json.dumps(User.query.get(uid).get_dict()), 200

    if request.method == "PUT":
        user_data = json.loads(request.data)
        user_change = db.session.query(User).get(uid)
        user_change.first_name = user_data["first_name"]
        user_change.last_name = user_data["last_name"]
        user_change.age = user_data["age"]
        user_change.email = user_data["email"]
        user_change.role = user_data["role"]
        user_change.phone = user_data["phone"]

        db.session.add(user_change)
        db.session.commit()

        return "Пользователь обновлен", 204

    if request.method == "DELETE":
        user_delete = db.session.query(User).get(uid)

        db.session.delete(user_delete)
        db.session.commit()

        return "Пользователь удален", 204


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for order in Order.query.all():
            result.append(order.get_dict())
        return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = Order(
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )

        db.session.add(new_order)
        db.session.commit()

        return "Заказ создан", 201


@app.route("/orders/<int:uid>", methods=["GET", "PUT", "DELETE"])
def order(uid):
    if request.method == "GET":
        return json.dumps(Order.query.get(uid).get_dict()), 200

    if request.method == "PUT":
        order_data = json.loads(request.data)
        order_change = db.session.query(Order).get(uid)
        order_change.name = order_data("name")
        order_change.description = order_data("description")
        order_change.start_date = order_data("start_date")
        order_change.end_date = order_data("end_date")
        order_change.address = order_data("address")
        order_change.price = order_data("price")
        order_change.customer_id = order_data("customer_id")
        order_change.executor_id = order_data("executor_id")

        db.session.add(order_change)
        db.session.commit()

        return "Заказ обновлен", 204

    if request.method == "DELETE":
        order_delete = db.session.query(Order).get(uid)

        db.session.delete(order_delete)
        db.session.commit()

        return "Заказ удален", 204


@app.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "GET":
        result = []
        for offer in Offer.query.all():
            result.append(offer.get_dict())
        return json.dumps(result), 200

    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )

        db.session.add(new_offer)
        db.session.commit()

        return "Предложение добавлено", 201


@app.route("/offers/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offer(uid):
    if request.method == "GET":
        return json.dumps(Offer.query.get(uid).get_dict()), 200
    if request.method == "PUT":
        offer_data = json.loads(request.data)
        offer_change = db.session.query(Offer).get(uid)
        offer_change.order_id = offer_data("order_id")
        offer_change.executor_id = offer_data("executor_id")

        db.session.add(offer_change)
        db.session.commit()

        return "Предложение обновлено", 204

    if request.method == "DELETE":
        offer_delete = db.session.query(Offer).get(uid)

        db.session.delete(offer_delete)
        db.session.commit()

        return "Предложение удалено", 204


if __name__ == '__main__':
    init_database()
    app.run(debug=True)
