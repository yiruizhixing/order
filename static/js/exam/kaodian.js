;
var food_cat_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        var that = this;
        /** 状态选择 **/
        $(".wrap_search select[name=status]").change( function () {
            $(".wrap_search").submit();
        } );

        /** 删除 **/
        $(".remove").click( function () {
            that.ops( "remove",$(this).attr("data") )
        } );
        /** 恢复 **/
        $(".recover").click( function () {
            that.ops( "recover",$(this).attr("data") )
        } );
    },
    ops:function ( act,id ) {
        var callback = {
            'ok':function () {
                $.ajax({
            url:common_ops.buildUrl("/exam/kaodian-ops"),
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
    food_cat_ops.init();
} );

