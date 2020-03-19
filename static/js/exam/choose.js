;
var exam_choose_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var btn_target = $(this);
        var that = this;

        /** 选择点击 **/
        $(".choose").click( function () {
            that.ops( "choose",$(this).attr("data") )
            //alert("aaa")
        } );


    },

    ops:function ( act,id ) {
        var callback = {
            'ok':function () {
                $.ajax({
            url:common_ops.buildUrl("/exam/choose"),
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
                            /** 选择完成后，统一跳转到 /index **/
                            window.location.href = common_ops.buildUrl("/");
                        }
                    }
                    common_ops.alert(res.msg,callback );
            }
        });
            },
            'cancel':null
        };
        common_ops.confirm( (act == "choose" ? "确定选择吗？":"确定恢复吗？"),callback )

    }

};

$(document).ready( function () {
    exam_choose_ops.init();

});