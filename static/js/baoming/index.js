;
var baoming_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        /**  swithc控件初始化 报名开关 条件开关 **/
        //$("[name='switch']").bootstrapSwitch();
        $('#switch1').bootstrapSwitch();
        $('#switch3').bootstrapSwitch();
        $('#switch4').bootstrapSwitch();
        $('#switch2').bootstrapSwitch({
            onSwitchChange:function(event,state){
                 if(state==true){

                 }
                 else {}
            }
        });

        /** 基本设置 编辑按钮 **/
        $('#baseedt').click(function () {
            $('#basesave').removeClass("disabled");
            $("input").removeAttr('disabled');
            //$('#switch1').bootstrapSwitch('setActive', false);
            //$('#switch1').Attr('disabled','false');
            $("textarea").removeAttr('disabled');
            $(this).addClass("disabled");
            $('.switch-show').removeAttr('hidden');
            $('.switch-hidden').remove();
        });

        /** 基本设置 保存 **/
        $('#basesave').click(function () {
            var btn_target = $(this);
            if( btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交");
                return;
            }
            /** 关联考试名称**/
            var exam_name = $('#examName').text();
            //common_ops.alert(exam_name);
            /** 显示考试名称**/
            var show_name = $("input[name='showName']").val();
            /** 考试id**/
            var examid = $('#examid').text();
            /** 所需人数**/
            var neednum = $("input[name='neednum']").val();
            //console.log(neednum);

            /** 报名条件**/
            var xstart = $('#xstart').val();
            var xend = $('#xend').val();
            var mstart = $('#mstart').val();
            var mend = $('#mend').val();

            /** 备注说明**/
            var beizhu = $("textarea").val();
            //console.log(beizhu);

            var rule_status = $('.bootstrap-switch-id-switch1').is('.bootstrap-switch-on');   //如果该元素有这个类，则是开启状态
            var status = $('.bootstrap-switch-id-switch2').is('.bootstrap-switch-on');



            if (xstart.length < 1) {
                xstart = 0;
            }
            if (xend.length < 1) {
                xend = 0;
            }
            if (mstart.length < 1) {
                mstart = 0;
            }
            if (mend.length < 1) {
                mend = 0;
            }

            if( eval(xstart) > eval(xend)){
                common_ops.alert("x起始号需要小于等于结束号" + xstart + xend);
                return false;
            }
            if( eval(mstart) > eval(mend)){
                common_ops.alert("m起始号需要小于等于结束号"+ mstart + mend);
                return false;
            }


            btn_target.addClass("disabled");

            var data = {
                exam_name:exam_name,
                show_name:show_name,
                neednum:neednum,
                examid:examid,
                xstart:xstart,
                xend:xend,
                mstart:mstart,
                mend:mend,
                beizhu:beizhu,
                rule_status:rule_status,
                status:status
            };

            $.ajax({
                url:common_ops.buildUrl("/baoming/index"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 修改完成后，统一跳转到 /baoming/index **/
                            window.location.href = common_ops.buildUrl("/baoming/index");
                        }
                    }
                    common_ops.alert(res.msg,callback );

                }

            });

        });







        /**  科目时间选择控件初始化  **/
        $('.date').datetimepicker({
            dayOfWeekStart: 1,
            initTime: true,
            allowTimes:['08:00','08:30','09:00','09:30','13:00','14:00','15:00']
        });
        $.datetimepicker.setLocale('zh');   //设置 datetimepicker 为汉语

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
    baoming_ops.init();

});