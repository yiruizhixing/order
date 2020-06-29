//获取应用实例
var app = getApp();
Page({
    data: {
        bind_flag:false,        
        nickname:"",
        avatar_url:"",
    },
    onLoad() {
        //this.getInfo(); //获取详情
    },
    onShow() {
        this.getInfo(); //获取详情
        // let that = this;        
        // that.setData({
        //     user_info: {
        //         nickname: info.name,
        //         avatar_url: info.avatar
        //     },
        // })
    },
    //获取会员详情 函数
    getInfo: function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/member/my"),
            header: app.getRequestHeader(),
            data: {},
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) { //返回不成功
                    app.alert({
                        "content": resp.msg
                    });
                    return;
                }
                //var goods = resp.data.list;
                that.setData({
                    bind_flag:resp.data.bind_flag,
                    nickname: resp.data.info.name,
                    avatar_url: resp.data.info.avatar                    
                });

            }
        });

    },
    //跳转绑定页面
    memberBind: function () {
        var that = this;
        if(that.data.bind_flag == false)   //如果未绑定 则跳转
            //console.info("aaa");
            wx.navigateTo({
                url: "/pages/my/bind/bind" 
            });
    }
});