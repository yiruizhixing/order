;
var food_cat_set_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
         /** wrap_account_set .save, 注意save前有一个空格*/
        $(".wrap_cat_set .save").click(function () {

            var btn_target = $(this);
            if( btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交");
                return;
            }
            /**  考点名称 **/
            var name_target = $(".wrap_cat_set input[name=name]");
            var name = name_target.val();
            /**  考点地址 **/
            var address_target = $(".wrap_cat_set input[name=address]");
            var address = address_target.val();
            /**  考场数量 **/
            var kaochang_target = $(".wrap_cat_set input[name=kaochang]");
            var kaochang = kaochang_target.val();
            /**  联系人 **/
            var linkman_target = $(".wrap_cat_set input[name=linkman]");
            var linkman = linkman_target.val();
            /** 电话 **/
            var tel_target = $(".wrap_cat_set input[name=tel]");
            var tel = tel_target.val();

            if( name.length < 1){
                common_ops.tip("请输入符合规范的考点名称",name_target );
                return false;
            }
            if( kaochang.length < 1){
                kaochang = 1;
            }


            btn_target.addClass("disabled");

            var data = {
                name:name,
                address:address,
                kaochang:kaochang,
                linkman:linkman,
                tel:tel,
                id:$(".wrap_cat_set input[name=id]").val()
            };

            $.ajax({
                url:common_ops.buildUrl("/exam/kaodian-set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /exam/kaodian **/
                            window.location.href = common_ops.buildUrl("/exam/kaodian");
                        }
                    }
                    common_ops.alert(res.msg,callback );

                }

            });

        });
    }

};

$(document).ready( function () {
    food_cat_set_ops.init();

});
