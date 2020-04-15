;
var kaowu_arrange_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var btn_target = $(this);
        var that = this;

        /** 人员删除 **/
        $(".remove").click( function () {
            that.ops( "remove",$(this).attr("data") )
        } );

        /** 人员新增-人员输入*/
        $("#id_select2_j_txtName").select2({
            //tags: true,   //是否支持自定义标签
            //placeholder: '请选择',
                ajax: {
                    url: "",
                    dataType: 'json',
                    delay: 250,
                    data: function(params) {
                        return {
                            search: params.term
                        };
                    },
                    processResults: function(data) {
                        return {
                            results: data
                        };
                    },
                    cache: true
                },
                minimumInputLength: 1     //最少输入的查询字符长度

        });

        /** 考区人员新增按钮*/
        $("#kaoqu_btnAdd").click(function () {
            $('#j_formAdd').show();
            $('#j_mask').show();
        });
        /** 考区人员新增窗口的关闭操作*/
        $('#j_hideFormAdd').click(function () {
            $('#j_formAdd').hide();
            $('#j_mask').hide();
        });
       /** 考区人员新增窗口的保存操作*/
       $('#j_btnAdd').click(function () {
            //3.1 获取到用户输入的名称.

            var job_target = $(".form-item select[name=j_txtCatname]");  //获取用户输入的岗位名称
            var job = job_target.val();

            var txtName = $("#id_select2_j_txtName").select2("data")[0].text; //获取用户输入的姓名
            var txtNameid = $("#id_select2_j_txtName").select2("data")[0].id; //获取用户输入的id

            var txtMark = $('#j_txtMark').val(); //获取备注
           //alert('提示：' + $("#id_select2_j_txtName").select2('val'));
           //console.log(txtNameid);



           btn_target.addClass("disabled");

            var data = {
                job:job,
                beizhu2:txtName,
                beizhu1:txtMark,
                name_id:txtNameid
            };

            $.ajax({
                url:common_ops.buildUrl("/kaowu/kqarrange"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /exam/index **/
                            window.location.href = common_ops.buildUrl("/kaowu/kqarrange");
                        }
                    }
                    common_ops.alert(res.msg,callback );

                }

            });

           //3.4 把添加数据面板和遮罩层影藏起来.
            $('#j_hideFormAdd').click();
        });


    },

    ops:function ( act,id ) {
        var callback = {
            'ok':function () {
                $.ajax({
            url:common_ops.buildUrl("/kaowu/kq-ops"),
            type:'POST',
            data:{
                act:act,
                id:id
            },
            dataType:'json',
            success:function (res) {
                var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 操作完成后，刷新当前页面 **/
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(res.msg,callback );
            }
        });
            },
            'cancel':null
        };
        common_ops.confirm( (act == "remove" ? "确定删除吗？":"确定恢复吗？"),callback )

    }

};

$(document).ready( function () {
    kaowu_arrange_ops.init();

});