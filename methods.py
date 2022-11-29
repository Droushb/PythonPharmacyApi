import json
from sqlite3 import Date
from flask import Flask, jsonify
from sqlalchemy import select
from main import User, Status, Drug, Order, OrderDetails
from models import session
import sqlalchemy

def serialize(self):
     return {
        "Id": self.idDrug,
        "Name": self.name,
        "Duration": self.duration,
        "Photo": self.photo,
        "Category": self.id_idCategory
     }

#drugs
def get_drugs():
    AllDrugs = session.execute(select(Drug))
    drugs = AllDrugs.scalars().all()
    result = ""
    for drug in drugs:
        status = session.query(Status).filter_by(idStatus = drug.idStatus).one()
        drugJSON = {
            "Id": drug.idDrug,
            "Name": drug.Name,
            "Price": drug.Price,
            "Status": status.Name
        }
        result+= json.dumps(drugJSON)
    return result


def get_drug_byid(id):
    drug = session.query(Drug).filter_by(idDrug = id).one()
    status = session.query(Status).filter_by(idStatus = drug.idStatus).one()
    drugJSON = {
        "Id": drug.idDrug,
        "Name": drug.Name,
        "Price": drug.Price,
        "Status": status.Name
    }
    return json.dumps(drugJSON)

def post_drug(id, Name, Price, idStatus):
    addeddrug = Drug(idDrug=id, Name=Name, Price=Price, idStatus=idStatus)
    session.add(addeddrug)
    session.commit()
    return 'Added a Drug with id %s' % id + get_drug_byid(id)

def update_drug(id, name, price, idStatus):
   updatedDrug = session.query(Drug).filter_by(idDrug = id).one()
   if name!='':
       updatedDrug.Name = name
   if price!='':
       updatedDrug.Price = price
   if idStatus!='':
       updatedDrug.idStatus = idStatus
   session.add(updatedDrug)
   session.commit()
   return 'Updated a Drug with id %s' % id + get_drug_byid(id)

def delete_drug(id):
    drugToDelete = session.query(Drug).filter_by(idDrug = id).one()
    session.delete(drugToDelete)
    session.commit()
    return 'Removed Drug with id %s' % id

#orders
def get_orders():
    AllOrders = session.execute(select(Order))
    orders = AllOrders.scalars().all()
    result = ""
    for order in orders:
        user = session.query(User).filter_by(idUser = order.idUser).one()
        status = session.query(Status).filter_by(idStatus = order.idStatus).one()
        orderJSON = {
            "Id": order.idOrder,
            "UserName": user.UserName,
            "Status": status.Name
        }
        result+= json.dumps(orderJSON)
    return result

def get_order_byid(id):
    order = session.query(Order).filter_by(idOrder = id).one()
    user = session.query(User).filter_by(idUser = order.idUser).one()
    status = session.query(Status).filter_by(idStatus = order.idStatus).one()
    orderDetails = session.query(OrderDetails).filter_by(idOrder = id)

    orderDetailsString = ""
    for i in orderDetails:
        drug = session.query(Drug).filter_by(idDrug = i.idDrug).one()
        orderdetailsJSON = {
            "Drug Name": drug.Name,
            "Quantity": i.quantity
        }
        orderDetailsString+= json.dumps(orderdetailsJSON)+" , "
    orderJSON = {
        "Id": order.idOrder,
        "UserName": user.UserName,
        "Status": status.Name
    }
    return json.dumps(orderJSON)+" , "+orderDetailsString

def post_order(id, idUser, idStatus, items):
    addedorder = Order(idOrder=id, idUser=idUser, idStatus=idStatus)
    session.add(addedorder)
    for item in items:
        addedorderdetails = OrderDetails(idOrder=id, idDrug=item['idDrug'], quantity=item['quantity'])
        session.add(addedorderdetails)
    session.commit()
    return 'Added a Order with id %s' % id + get_order_byid(id)

def delete_order(id):
    orderToDelete = session.query(Order).filter_by(idOrder = id).one()
    while session.query(OrderDetails).filter_by(idOrder = id).first() is not None:
        orderDetailsToDelete =  session.query(OrderDetails).filter_by(idOrder = id).first()
        session.delete(orderDetailsToDelete)
    session.delete(orderToDelete)
    session.commit()
    return 'Removed Order with id %s' % id

#status
def get_status():
    AllStatuses = session.execute(select(Status))
    statuses = AllStatuses.scalars().all()
    result = ""
    for status in statuses:
        orderJSON = {
            "Id": status.idStatus,
            "Name": status.Name,
        }
        result+= json.dumps(orderJSON)
    return result

#users
def get_user_byUserName(UserName):
    userOne = session.query(User).filter_by(UserName = UserName).one()
    userJSON = {
        "Id": userOne.idUser,
        "UserName": userOne.UserName,
        "First Name": userOne.FirstName,
        "Second Name": userOne.LastName,
        "Email": userOne.Email,
        "Password": userOne.Password,
        "Phone": userOne.Phone,
        "Role": userOne.Role
    }
    return json.dumps(userJSON)

def post_user(id, UserName, firstName, lastName, email, password, phone, role):
    addeduser = User(idUser=id, UserName=UserName, FirstName=firstName, LastName=lastName,
    Email=email, Password=password, Phone=phone, Role=role)
    session.add(addeduser)
    session.commit()
    return 'Added a User with id %s' % id + get_user_byUserName(UserName)

def update_user(userName, firstName, lastName, email, password, phone):
    updatedUser = session.query(User).filter_by(UserName = userName).first()
    if firstName!='':
        updatedUser.FirstName = firstName
    if lastName!='':
        updatedUser.LastName = lastName
    if email!='':
        updatedUser.Email = email
    if password!='':
        updatedUser.Password = password
    if phone!='':
        updatedUser.Phone = phone
    session.add(updatedUser)
    session.commit()
    return 'Updated a User with UserName %s' % userName + get_user_byUserName(userName)

def delete_user(UserName):
    userToDelete = session.query(User).filter_by(UserName = UserName).one()
    session.delete(userToDelete)
    session.commit()
    return 'Removed User with UserName %s' % UserName
