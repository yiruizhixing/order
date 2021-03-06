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
            /**  分类名称 **/
            var name_target = $(".wrap_cat_set input[name=name]");
            var name = name_target.val();
            /** 权重 **/
            var weight_target = $(".wrap_cat_set input[name=weight]");
            var weight = weight_target.val();

            if( name.length < 1){
                common_ops.tip("请输入符合规范的分类名称",name_target );
                return false;
            }
           /** 整型且不能小于1 **/
            if( parseInt(weight) < 1){
                common_ops.tip("请输入符合规范的权重，并且至少要大于1",weight_target );
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                name:name,
                weight:weight,
                id:$(".wrap_cat_set input[name=id]").val()
            };

            $.ajax({
                url:common_ops.buildUrl("/peixun/cat-set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /food/index **/
                            window.location.href = common_ops.buildUrl("/peixun/cat");
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
