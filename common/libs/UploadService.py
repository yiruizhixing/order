# 上传相关功能封装

class UploadService():
    @staticmethod
    def uploadByFile(file):
        resp = {'code':200, 'msg':'', 'data':{}}
        return resp