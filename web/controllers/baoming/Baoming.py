# -*- coding: utf-8 -*-
from flask import Blueprint
from common.libs.Helper import ops_render


route_baoming = Blueprint( 'baoming_page',__name__ )

@route_baoming.route( "/index" )
def index():
    return ops_render( "baoming/index.html" )

