;
var exam_set_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        /**  科目时间选择控件初始化  **/
        $('.date').datetimepicker({
            dayOfWeekStart: 1,
            initTime: true,
            allowTimes:['08:00','08:30','09:00','09:30','13:00','14:00','15:00']
        });
        $.datetimepicker.setLocale('zh');   //设置 datetimepicker 为汉语

        /** 基本设置 保存 **/
        $('#basesave').click(function () {
            //alert("点了");

            var btn_target = $(this);
            if( btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交");
                return;
            }
            /** 考试名称**/
            //var exam_name = $('#exam_name').text();
            //common_ops.alert(exam_name);
            /** 考试id**/
            var examid = $('#examid').text();

            /** 考试科数**/
            var keshu_target = $("input[name='inlineRadioOptions']:checked");
            var keshu = keshu_target.val();
            //console.log(keshu_target);
            /** 考试天数**/
            var days_target = $(".form-horizontal select[name=exam_days]");
            var days = days_target.val();

            /** 考试餐补次数**/
            var canbu_target = $(".form-horizontal select[name=exam_canbu]");
            var canbu = canbu_target.val();
            //common_ops.alert(canbu);


            if( keshu == undefined){
                common_ops.alert("请选择科目数");
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                keshu:keshu,
                canbu:canbu,
                days:days,
                id:examid
            };

            $.ajax({
                url:common_ops.buildUrl("/examset/index"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /examset/index **/
                            window.location.href = common_ops.buildUrl("/examset/index");
                        }
                    }
                    common_ops.alert(res.msg,callback );

                }

            });

        });

        /** 基本设置 编辑按钮 **/
        $('#baseedt').click(function () {
            $('#basesave').removeClass("disabled");
            $("select").removeAttr('disabled');
            $('input[name="inlineRadioOptions"]').removeAttr('disabled');
            $(this).addClass("disabled");
        });

        /** 科目设置 保存 **/
        $('#kemuSave').click(function () {

            var btn_target = $(this);
            if( btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交");
                return;
            }

            //common_ops.alert("点了呀");

            //var trs = $("table tr:not(:first)");  //选取table 中 除去第一个tr之外的tr
            var trs = $("table tr.kemu");           //选取table 中 class 为kemu的tr
            //console.log(trs);
            //声明一个盒子
            var array = [];
            //循环你所要选择的行
            $.each(trs, function (i, val) {
                var tr = val;
                var json = {kemuid: 0,changci:0, kemuName: "", startTime: 0, lastTime:0, kaochang: 0 };
                json.changci = $(tr).find("[name='changci']").text();
                json.kemuName = $(tr).find("[name='kemuName']").val();
                json.kaochang = $(tr).find("[name='kaochang']").val();
                json.startTime = $(tr).find("[name='startTime']").val();
                json.lastTime = $(tr).find("[name='lastTime']").val();
                json.kemuid = $(tr).find("[name='kemuid']").val();
                //common_ops.alert(json.kaochang);
                //console.log(json.lastTime);
                //全加入
                array.push(json);
            });
            var jsongString = { data: JSON.stringify(array) };
            $.ajax({
                url:common_ops.buildUrl("/examset/kemusave"),
                type:'POST',
                data:jsongString,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /examset/index **/
                            window.location.href = common_ops.buildUrl("/examset/index");
                        }
                    }
                    common_ops.alert(res.msg,callback );

                }

            });

        });

        /** 科目设置 编辑 **/
         $('#kemuedt').click(function () {
             $('#kemuSave').removeClass("disabled");
             $('#kemuDel').addClass("disabled");
             $('table input').removeAttr('disabled');
             $(this).addClass("disabled");
         });
        /** 科目设置 删除 **/
         $('#kemuDel').click(function () {
             var btn_target = $(this);
             if( btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交");
                return;
             }
             var trs = $("table tr.kemu");           //选取table 中 class 为kemu的tr

            //声明一个盒子
             var array = [];
            //循环你所要选择的行
             $.each(trs, function (i, val) {
                var tr = val;
                var json = {kemuid: 0 };
                json.kemuid = $(tr).find("[name='kemuid']").val();
                //全加入
                array.push(json);
             });
             var jsongString = { data: JSON.stringify(array) };
             $.ajax({
                url:common_ops.buildUrl("/examset/kemudel"),
                type:'POST',
                data:jsongString,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /examset/index **/
                            window.location.href = common_ops.buildUrl("/examset/index");
                        }
                    }
                    common_ops.alert(res.msg,callback );

                }

             });

         })

    }

};

$(document).ready( function () {
    exam_set_ops.init();

});