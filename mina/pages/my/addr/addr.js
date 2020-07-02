//获取应用实例
//var commonCityData = require('../../../utils/city.js');
var app = getApp();
Page({
  data: {
    provinces: [],
    citys: [],
    districts: [],
    // selProvince: '请选择',
    // selCity: '请选择',
    // selDistrict: '请选择',
    // selProvinceIndex: 0,
    // selCityIndex: 0,
    // selDistrictIndex: 0
  },
  onLoad: function (e) {
    var that = this;
    
  },
  onShow() {
    this.getInfo(); //获取详情
},
  
  bindCancel: function () {
    wx.navigateBack({});
  },
  // submit 保存提交
  bindSave: function (e) {
    var that = this;
    wx.request({
      url: app.buildUrl("/member/infoedt"),
      header: app.getRequestHeader(),
      method: 'POST',
      data: {
        people_id:that.data.info.people_id,
        chepai:e.detail.value.chepai,
        sfzh:e.detail.value.sfzh,
        mobile:e.detail.value.mobile,
        bankcard:e.detail.value.bankcard,
        bankaddr:e.detail.value.bankaddr,
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


  },
  deleteAddress: function (e) {

  },
      //获取会员详情 函数
      getInfo: function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/member/infoedt"),
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
                that.setData({
                    info:resp.data.info, 
                });

            }
        });

    },
});
