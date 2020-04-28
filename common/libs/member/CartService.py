# 小程序购物 集中共用函数代码

from application import app, db
from common.models.member.MemberCart import MemberCart


class CartService():

    @staticmethod
    def setItems(member_id = 0,food_id = 0,number = 0):
        if member_id < 1 or food_id < 1 or  number < 1:
            return False
        cart_info = MemberCart.query.filter_by( food_id = food_id,member_id = member_id).first()
        if cart_info:
            model_cart = cart_info
        else:
            model_cart = MemberCart()
            model_cart.member_id = member_id

