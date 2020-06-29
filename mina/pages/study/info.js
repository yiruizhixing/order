//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');
var utils = require('../../utils/util.js');

Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        buyNumber: 1,
        buyNumMin: 1,
        buyNumMax:1,
        canSubmit: false, //  选中时候是否允许加入购物车
        shopCarInfo: {},
        shopType: "addShopCar",//购物类型，加入购物车或立即购买，默认为加入购物车,
        id: 0,
        shopCarNum: 4,
        commentCount:2
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            id:e.id               //从页面传入的参数中获取商品id
        });

    },

    //每次进入页面都刷新显示详情
    onShow:function(){
        this.getInfo();         //显示详情
    },
    goShopCar: function () {
        wx.reLaunch({
            url: "/pages/cart/index"
        });
    },
    toAddShopCar: function () {
        this.setData({
            shopType: "addShopCar"
        });
        this.bindGuiGeTap();
    },
    tobuy: function () {
        this.setData({
            shopType: "tobuy"
        });
        this.bindGuiGeTap();
    },
    //加入购物车
    addShopCar: function () {
        var that = this;
        var data ={
            "id":this.data.info.id,
            "number":this.data.buyNumber
        };
        wx.request({           //向服务器发送分 存入数据库
            url: app.buildUrl("/cart/set"),
            header: app.getRequestHeader(),        //头部信息，记录用户信息
            method: 'POST',
            data: data,
            success: function (res) {

            }
        });

    },
    buyNow: function () {
        wx.navigateTo({
            url: "/pages/order/index"
        });
    },
    /**
     * 规格选择弹出框
     */
    bindGuiGeTap: function () {
        this.setData({
            hideShopPopup: false
        })
    },
    /**
     * 规格选择弹出框隐藏
     */
    closePopupTap: function () {
        this.setData({
            hideShopPopup: true
        })
    },
    numJianTap: function () {
        if( this.data.buyNumber <= this.data.buyNumMin){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum--;
        this.setData({
            buyNumber: currentNum
        });
    },
    numJiaTap: function () {
        if( this.data.buyNumber >= this.data.buyNumMax ){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum++;
        this.setData({
            buyNumber: currentNum
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    //获取商品详情 函数
    getInfo:function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/food/info"),
            header: app.getRequestHeader(),
            data:{
                id:that.data.id
            },
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {               //返回不成功
                    app.alert({"content": resp.msg});
                    return;
                }
                //var goods = resp.data.list;
                that.setData({
                    info:resp.data.info,
                    buyNumMax:resp.data.info.stock,  //最大购买数量为库库值
                });
                WxParse.wxParse('article','html',that.data.info.summary,that,5);    //发送给wx富文本解析插件
            }
        });

    },

    // 页面分享设置
    onShareAppMessage:function () {
        var that = this;
        var shareObj ={
            title:that.data.info.name,
            path:'page/food/info?id=' + that.data.info.id,
            // 分享转发成功与失败的回调已于2018年取消
            // success:function (res) {  //转发成功
            //     console.info("转发成功");
            //     wx.request({           //向服务器发送分享记录 存入数据库
            //         url: app.buildUrl("/member/share"),
            //         header: app.getRequestHeader(),        //头部信息，记录用户信息
            //         method:'POST',
            //         data: {
            //             url:utils.getCurrentPageUrlWithArgs()
            //         },
            //         success: function (res) {
            //
            //         }
            //     });
            // },
            // fail:function (res) {
            //     //转发失败
            //     console.info("失败");
            // }
        };
        //console.info("转发");
        // 返回shareObj
　　    return shareObj;
    }
});
