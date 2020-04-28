;
var kaowu_kdarrange_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var btn_target = $(this);
        var that = this;
         /** 人员新增-人员输入  select2 *******************************************************************/
         //***初始化 及 输入第一个字后动态获取相关人员数据***
         $('.txt').select2({
             //tags: true,   //是否支持自定义标签
             //placeholder: '请选择',
             ajax: {
                 url: "/kaowu/kqarrange",
                 dataType: 'json',
                 delay: 250,
                 data: function (params) {
                     return {
                         search: params.term
                     };
                 },
                 processResults: function (data) {
                     return {
                         results: data
                     };
                 },
                 cache: true
             },
             minimumInputLength: 1     //最少输入的查询字符长度
         });

        //手工输入添加人员
        $('.txt').on('select2:select', function (e) {
            //alert("很好呀")
           // console.log($(this).find(':selected:last'.select2("data")));
            var txtName = $(this).find(':selected:last')[0].text;               //获取用户输入的人员姓名
            var txtNameid = $(this).find(':selected:last')[0].value;            //获取用户输入的人员id
            var kdid = $(this).parent().parent().attr('class');                        //获取其父类的类名，获取考点id
            //var kdname = $(this).parent().parent().attr('class');             //获取其父类的类名，考点name
            var kdgw = $(this).find('~ a')[0].text;                            //~获取其同级的所有 <a> 元素，工作岗位
            var gwid = $(this).attr('name');                                   //岗位id
            var kdname = $(this).parents('.tab-pane').children('a')[0].text;   //~获取其祖先元素tab-pane类下的 <a> 元素，考点name
            console.log(kdid);

            var data = {
                job:kdgw,               //岗位名称
                job_id:gwid,            //岗位id
                name:txtName,           //人员姓名
                name_id:txtNameid,      //人员id
                kaodian:kdname,         //考点名称
                kdid:kdid               //考点id
            };
            $.ajax({
                url:common_ops.buildUrl("/kaowu/kdarrange"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    //btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到  **/
                            window.location.href = common_ops.buildUrl("/kaowu/kdarrange");
                        }
                    }
                    /** 修改失败 则提示  **/
                    else{common_ops.alert(res.msg,callback )}
                }
            });
        });
        //手工删除人员
        $('.txt').on('select2:unselect', function (e) {
            //alert("删除")
            console.log(e);
            console.log(e.params.data.text);   //被删除人员姓名
            console.log(e.params.data.id);   //被删除人员姓名id
            console.log(e.currentTarget.attributes.name.nodeValue);
            console.log(kdname);
            var kdname = $(this).parents('.tab-pane').children('a')[0].text;     //~获取其祖先元素tab-pane类下的 <a> 元素，考点name
            var gwid = e.currentTarget.attributes.name.nodeValue;                //工作岗位
            var txtName = e.params.data.text;                                    //人员姓名
            var txtNameid = e.params.data.id;                                    //人员id

            var data = {
                //job:kdgw,               //岗位名称
                job_id:gwid,            //岗位id
                name:txtName,           //人员姓名
                name_id:txtNameid,      //人员id
                kaodian:kdname,         //考点名称
            };
            $.ajax({
                url:common_ops.buildUrl("/kaowu/kd-ops"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    //btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到  **/
                            window.location.href = common_ops.buildUrl("/kaowu/kdarrange");
                        }
                    }
                    /** 修改失败 则提示  **/
                    else{common_ops.alert(res.msg,callback )}
                }
            });

        });

        /** 人员编辑按钮 **/
        $('.edt-btn').click(function(){
            $(this).parents('tbody').find('.txt').prop("disabled", false);
        });
        /** 人员编辑ok按钮 **/
        $('.ok-btn').click(function(){
            $(this).parents('tbody').find('.txt').prop("disabled", true);
        });
        /** select2  end **************************************************************************/

       /** 考点其他人员安排 start **/
        /** 人员删除 **/
        $(".remove").click( function () {
            that.ops( "remove",$(this).attr("data") )
        } );

        /** 人员新增-人员输入*/
        $("#id_select2_j_txtName").select2({
            //tags: true,   //是否支持自定义标签
            width:400,
            //placeholder: '请选择',
                ajax: {
                    url: "/kaowu/kqarrange",
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
                minimumInputLength: 1

        });

        /** 考区人员新增按钮*/
        $(".kd-other-add").click(function () {
            $('#j_formAdd').show();
            var kdid = $(this).attr("name");    //获取被点击按钮的name值，即为考点id
            var kdname = $(this).parents('.tab-pane').children('a')[0].text;   //~获取其祖先元素tab-pane类下的 <a> 元素，考点name
            //console.log(kdname);
            // 设置标签定义属性
            $("#j_formAdd >input").attr("name", kdid);
            $("#j_formAdd >a").attr("value", kdname);
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
            var job_target = $(".form-item select[name=j_txtCatname]");
            var job_id = job_target.val();                               // 获取岗位id
            var job = job_target.find("option:selected").text();         // 获取岗位名称

            var txtName = $("#id_select2_j_txtName").select2("data")[0].text; //获取用户输入的姓名
            var txtNameid = $("#id_select2_j_txtName").select2("data")[0].id; //获取用户输入的姓名id
            var txtMark = $('#j_txtMark').val();                              //获取备注

           var kdid = $('#j_formAdd>input').attr("name");                     //获取考点id
           var kdname = $('#j_formAdd>a').attr("value");                     //获取考点name
           console.log(kdname);

           btn_target.addClass("disabled");

            var data = {
                job:job,
                job_id:job_id,
                name:txtName,
                name_id:txtNameid,
                beizhu1:txtMark,
                kdid:kdid,
                kaodian:kdname        //考点名称
            };
            $.ajax({
                url:common_ops.buildUrl("/kaowu/kdarrange"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /exam/index **/
                            window.location.href = common_ops.buildUrl("/kaowu/kdarrange");
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
                    url: common_ops.buildUrl("/kaowu/kq-ops"),
                    type: 'POST',
                    data: {
                        act: act,
                        id: id
                    },
                    dataType: 'json',
                    success: function (res) {
                        var callback = null;
                        if (res.code == 200) {
                            callback = function () {
                                /** 操作完成后，刷新当前页面 **/
                                window.location.href = window.location.href;
                            }
                        }
                        common_ops.alert(res.msg, callback);
                    }
                });
            },
            'cancel':null
        };
        common_ops.confirm( (act == "remove" ? "确定删除吗？":"确定恢复吗？"),callback )

    }
};

$(document).ready( function () {
    kaowu_kdarrange_ops.init();
});