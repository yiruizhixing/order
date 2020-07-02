// pages/bm/bm.js
//获取应用实例
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    id: 0,
    bm_status:"",
    sh_status:"无"
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (e) {
    var that = this;
    that.setData({
      id: e.id //从页面传入的参数中获取报名id
    });
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    this.getInfo(); //获取详情
  },

  //获取报名内容详情 函数
  getInfo: function () {
    var that = this;
    wx.request({
      url: app.buildUrl("/bm/info"),
      header: app.getRequestHeader(),
      data: {
        id: that.data.id //报名项目id
      },
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
          info: resp.data.info,
          bm_status:resp.data.bm_status,
          sh_status:resp.data.sh_status
        });

      }
    });

  },
  //报名提交
  toBaoMing: function (e) {
    var that = this;
    var bianhao_temp = that.data.info.bianhao;
    if(bianhao_temp==''){                             //如果没有编号，则赋值一个临时编号
      bianhao_temp="000"
    }
    var data = {
      "id": that.data.id,                             //报名项目id
      "name": that.data.info.name,                    //人员姓名
      "people_id": that.data.info.people_id,          //人员id
      "bianhao": bianhao_temp,                        //人员编号
    };
    wx.request({ //向服务器发送 存入数据库
      url: app.buildUrl("/bm/post"),
      header: app.getRequestHeader(),                 //头部信息，记录用户信息
      method: 'POST',
      data: data,
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
        // wx.navigateBack({      //返回前一页
        //   delta:1
        // })
      }
    });
  },

})