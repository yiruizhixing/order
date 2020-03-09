# -*- coding: utf-8 -*-
from flask import Blueprint
from common.libs.Helper import ops_render

route_kaowu = Blueprint( 'kaowu_page',__name__ )

@route_kaowu.route( "/index" )
def index():
    return ops_render( "kaowu/index.html" )

@route_kaowu.route( "/arrange" )
def arrange():
    return ops_render( "kaowu/arrange.html" )

@route_kaowu.route( "/member" )
def memebr():
    return ops_render( "stat/member.html" )

@route_kaowu.route( "/share" )
def share():
    return ops_render( "stat/share.html" )
