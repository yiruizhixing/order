//app.js
App({
  //生命周期函数
    onLaunch: function () {
    },
    globalData: {
        userInfo: null,
        version: "1.0",
        shopName: "巡考小程序",
        //domain:"http://192.168.244.6:8999/api"
        domain:"https://rsks.gongkao.org.cn/api"
    },
    tip:function( params ){
        var that = this;
        var title = params.hasOwnProperty('title')?params['title']:'提示信息';
        var content = params.hasOwnProperty('content')?params['content']:'';
        wx.showModal({
            title: title,
            content: content,
            success: function(res) {

                if ( res.confirm ) {//点击确定
                    if( params.hasOwnProperty('cb_confirm') && typeof( params.cb_confirm ) == "function" ){
                        params.cb_confirm();
                    }
                }else{//点击否
                    if( params.hasOwnProperty('cb_cancel') && typeof( params.cb_cancel ) == "function" ){
                        params.cb_cancel();
                    }
                }
            }
        })
    },
    alert:function( params ){
        var title = params.hasOwnProperty('title')?params['title']:'提示信息';
        var content = params.hasOwnProperty('content')?params['content']:'';
        wx.showModal({
            title: title,
            content: content,
            showCancel:false,
            success: function(res) {
                if (res.confirm) {//用户点击确定
                    if( params.hasOwnProperty('cb_confirm') && typeof( params.cb_confirm ) == "function" ){
                        params.cb_confirm();
                    }
                }else{
                    if( params.hasOwnProperty('cb_cancel') && typeof( params.cb_cancel ) == "function" ){
                        params.cb_cancel();
                    }
                }
            }
        })
    },
    console:function( msg ){
        console.log( msg);
    },
    getRequestHeader:function(){    //生成网络请求的头部信息
        return {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': this.getCache("token")
        }
    },
    buildUrl:function(path,params){
      var url =this.globalData.domain + path;
      var _paramUrl = "";
      if (params) {
        _paramUrl = Object.keys(params).map(function (k) {
          return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=")
        }).join("&");
        _paramUrl = "?" + _paramUrl
      }
      return url + _paramUrl;
    },
    //调取用户本地存储登录缓存
    getCache:function(key){
      var value = undefined;
      try {
       value = wx.getStorageSync(key)
       if (value) {
          
        }
      } catch (e) {        
      }
      return value;
    },
    //用户本地存储登录缓存
    setCache:function(key,value){
      wx.setStorage({
        key: key,
        data: value
      });
    }
});