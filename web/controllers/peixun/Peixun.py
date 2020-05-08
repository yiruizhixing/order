# -*- coding: utf-8 -*-
from flask import Blueprint
from common.libs.Helper import ops_render


route_peixun = Blueprint( 'peixun_page',__name__ )

@route_peixun.route( "/index" )
def index():
    return ops_render( "peixun/index.html" )

