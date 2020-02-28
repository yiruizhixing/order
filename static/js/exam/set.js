;
var exam_set_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
         /** wrap_account_set .save, 注意save前有一个空格*/
        $(".wrap_account_set .save").click(function () {

            var btn_target = $(this);
            if( btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交");
                return;
            }
            /** 考试名称**/
            var exam_name_target = $(".wrap_account_set input[name=exam_name]");
            var exam_name = exam_name_target.val();
            /** 考试时间 **/
            var exam_date_target = $(".wrap_account_set input[name=exam_date]");
            var exam_date = exam_date_target.val();
            /** 考试类别 **/
            var exam_cat_target = $(".wrap_account_set select[name=exam_cat]");
            var exam_cat = exam_cat_target.val();


            /** 考试描述 **/
            var summary_target = $(".wrap_account_set input[name=summary]");
            var summary = summary_target.val();



            if( exam_name.length < 1){
                common_ops.tip("请输入符合规范的考试名",exam_name_target );
                return false;
            }

            if( exam_date.length < 1){
                common_ops.tip("请输入符合规范的考试时间",exam_date_target );
                return false;
            }



            btn_target.addClass("disabled");

            var data = {
                exam_name:exam_name,
                exam_date:exam_date,
                exam_cat:exam_cat,
                summary:summary,
                id:$(".wrap_account_set input[name=id]").val()
            };

            $.ajax({
                url:common_ops.buildUrl("/exam/set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /exam/index **/
                            window.location.href = common_ops.buildUrl("/exam/index");
                        }
                    }
                    common_ops.alert(res.msg,callback );

                }

            });

        });
    }

};

$(document).ready( function () {
    exam_set_ops.init();

});