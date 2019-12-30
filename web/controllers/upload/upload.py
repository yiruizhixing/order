# 上传功能处理
from flask import Blueprint

route_upload = Blueprint('upload_page', __name__)


@route_upload.route("/ueditor", methods=["GET", "POST"])
def ueditor():
    req = request.values
    action = req['action'] if 'action' in req else ''
    if action == "config":
        root_path = app.root_path
        config_path = "{0}/web/static/plugins/ueditor/upload_config.json".format(root_path)
        with open(config_path) as fp:
            try:
                config_path = json.loads(re.sub(r'\/\*.*\*/','',fp.read()))
            except:
                config_data = {}
        return jsonify(config_data)
    if action == "uploadimage":
        return uploadImage()


    return "upload"

def uploadImage():
    resp = {'state':'SUCCESS','url':'','title':'','orginal':''}
    file_target = request.files
    app.logger.info(file_target)
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    if upfile is None:
        resp['state'] = "上传失败"
        return jsonify(resp)

    return jsonify(resp)