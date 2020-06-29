//获取应用实例
var commonCityData = require('../../../utils/city.js');
var app = getApp();
Page({
  data: {
    provinces: [],
    citys: [],
    districts: [],
    selProvince: '请选择',
    selCity: '请选择',
    selDistrict: '请选择',
    selProvinceIndex: 0,
    selCityIndex: 0,
    selDistrictIndex: 0
  },
  onLoad: function (e) {
    var that = this;
    
  },

  bindCancel: function () {
    wx.navigateBack({});
  },
  //绑定信息提交
  bindSave: function (e) {
    //console.info(e);
    if (e.detail.value.name.length == 0) {
      wx.showToast({
        title: '姓名不能为空',
        icon: 'loading',
        duration: 1500
      })
      setTimeout(function () {
        wx.hideToast()
      }, 2000)
    }else {
      wx.request({
        url: app.buildUrl("/member/bind"),
        header: app.getRequestHeader(),
        data: {
          name:e.detail.value.name
        },
        success: function (res) {
            var resp = res.data;
            if (resp.code != 200) { //返回不成功
                app.alert({
                    "content": resp.msg
                });
                return;
            }
            wx.showModal({         //返回成功提示框
              title: '提示',
              content: resp.msg,
              showCancel:false,
              success (res) {
                if (res.confirm) {   //点击确认
                  wx.navigateBack({  //返回前一页 首页
                    delta:1
                  })
                } else if (res.cancel) {
                  //console.log('用户点击取消')
                }
              }
            })
            

        }
    });
    }


  },



  deleteAddress: function (e) {

  },
  

});
