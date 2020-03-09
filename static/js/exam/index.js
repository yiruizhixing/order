;
var exam_index_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;

        /** 恢复 **/
        $(".recover").click( function () {
            that.ops( "recover",$(this).attr("data") )
        } );
        /** 暂停**/
        $(".pause").click( function () {
            that.ops( "pause",$(this).attr("data") )
        } );
    },
    ops:function ( act,id ) {
        var callback = {
            'ok':function () {
                $.ajax({
            url:common_ops.buildUrl("/exam/ops"),
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
        common_ops.confirm( (act == "pause" ? "确定关闭吗？关闭后不可编辑":"确定启用吗？"),callback )

    }
};

$(document).ready( function () {
    exam_index_ops.init();
} );

