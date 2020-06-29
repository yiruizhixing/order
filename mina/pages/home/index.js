// pages/home/index.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    indicatorDots: true,
    autoplay: true,
    loadingHidden: false, // loading
    categories: [{ "id": 1, "name": "考试1" },{ "id": 2, "name": "考试222" }],
    activeCategoryId: 0,
    goods: [],
    news:[],
    bm_list:[],
    processing:false

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    this.getNewsList();    //加载新闻列表 考务通知
    //console.info("aaa")
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
    
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  

  //分类标签被点击后处理方法
  catClick: function (e) {
    this.setData({
      activeCategoryId: e.currentTarget.id,
      p: 1,
      goods: [],
      loadingMoreHidden: true

    });
    //app.alert({ "content": "点了" });
  },

  //获取news列表 and 报名列表
  getNewsList: function () {
    var that = this;
    //如果存在processing变量，则表示正在处理，不能再次发出请求
    if (that.data.processing) {
      return;
    }
    that.setData({
      processing: true                        //正在处理
    });
    wx.request({
      url: app.buildUrl("/home/news"),
      header: app.getRequestHeader(),
      success: function (res) {
        var resp = res.data;
        if (resp.code != 200) {               //返回不成功
          app.alert({ "content": resp.msg });
          return;
        }
        that.setData({
          news:resp.data.news_list,
          bm_list:resp.data.bm_list
        });
        //console.info(goods); 

      }
    });
  },
  toNewsDetailsTap: function (e) {
    wx.navigateTo({
      url: "/pages/news/info?id=" + e.currentTarget.dataset.id
    });   
  },



})