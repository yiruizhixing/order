//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        p: 1
    },
    onLoad: function () {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });



        this.getBannerAndCat();
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
	listenerSearchInput:function( e ){
	        this.setData({
	            searchInput: e.detail.value
	        });
	 },
	 toSearch:function( e ){
	        this.setData({
	            p:1,
	            goods:[],
	            loadingMoreHidden:true
	        });
	        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    },
    //获取banner图和菜品分类
    getBannerAndCat:function () {
        var that = this;
        wx.request({
            url:app.buildUrl("/food/index"),
            header:app.getRequestHeader(),
            success:function ( res ) {
                var resp = res.data;
                if(resp.code != 200){
                  app.alert({"content":resp.msg});
                  return;
                }
                that.setData({
                  banners:resp.data.banner_list,
                  categories:resp.data.cat_list
                });
                that.getFoodList();

            }
        });

    },
     //分类标签被点击后处理方法
    catClick:function(){
      this.setData({
        activeCategoryId:e.currentTarget.id
      });
      this.getFoodList();
    },
    //触底函数
    onReachBottom:function(){
      var that = this;
      //500ms 延时处理
      setTimeout(function(){
        that.getFoodList();
      },500)

    },
    //获取菜品列表
    getFoodList:function(){
      var that = this;
      //如果存在processing变量，则表法正在处理，不能再次发出请求
      if (that.data.processing){
        return;
      }
      //如果没有了，就返回
      if (!that.data.loadingMoreHidden){
        return;
      }

      that.setData({
        processing:true     //正在处理
      });

      wx.request({
        url: app.buildUrl("/food/search"),
        header: app.getRequestHeader(),
        data:{
          cat_id: that.data.activeCategoryId,
          mix_kw:that.data.searchInput,
          p:that.data.p

        },
        success: function (res) {
          var resp = res.data;
          if (resp.code != 200) {
            app.alert({ "content": resp.msg });
            return;
          }
          var goods = resp.data.list;          
          that.setData({
            goods:goods,
            p:that.data.p + 1,   //页码加1
            processing:false
            
          });
          //if 再没有页码了
          if(resp.data.has_more == 0){
            that.setData({
              loadingMoreHidden:false
            })
          }

        }
      });
    }
});
