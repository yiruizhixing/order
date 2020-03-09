;
var kaowu_arrange_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        /** 考区人员新增按钮*/
        $("#kaoqu_btnAdd").click(function () {
            $('#j_formAdd').show();
            $('#j_mask').show();
        })
        /** 考区人员新增窗口的关闭操作*/
        $('#j_hideFormAdd').click(function () {
            $('#j_formAdd').hide();
            $('#j_mask').hide();
        });
       /** 考区人员新增窗口的保存操作*/
       $('#j_btnAdd').click(function () {
            //3.1 获取到用户输入的所属学院和课程名称.
            var txtCatname = $('#j_txtCatname').val(); //获取用户输入的岗位名称
            var txtName = $('#j_txtName').val(); //获取用户输入的姓名
            var txtMark = $('#j_txtMark').val(); //获取备注
            //3.2 把用户输入的内容 ,创建出一个tr.
            var $trNew =$( '<tr>' +
                            '<td>'+txtCatname+'</td>'+
                            '<td>'+txtName+'</td>' +
                            '<td>'+txtMark+'</td>' +
                            '<td><a href="javascript:void(0);" class="get">删除</a></td>' +
                         '</tr>' );

            //给新创建的这个$trNew里面的a标签添加一个事件.
            $trNew.find('.get').click(function () {
                //$(this).parent().parent().remove();
                $trNew.remove();
            });

            //3.3 把新创建的tr标签添加到tbody中.
            $('#j_tb').append($trNew);
            //3.4 把添加数据面板和遮罩层影藏起来.
            $('#j_hideFormAdd').click();
        });

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
    kaowu_arrange_ops.init();

});