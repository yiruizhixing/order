;
var exam_kaodianset_ops ={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        //1.全部到右边
    // $('#btn-sel-all').click(function () {
    //   //找到左边select下拉菜单的所有option项,把这些option项都添加到右边的select下拉菜单中去.
    //   $('#src-kaodian>option').appendTo($('#tar-kaodian'));
    // });

    //2.全部到左边
    // $('#btn-back-all').click(function () {
    //   //找到右边select下拉菜单中的所有option项,把这些option项都添加到左边的select下拉菜单中去.
    //   $('#tar-kaodian>option').appendTo($('#src-kaodian'));
    // });

    //3.选中的到右边.
    $('#btn-sel').click(function () {
      //找到左边select下拉菜单中,被选中的option项, 把这些option项添加到右边的select下拉菜单中.
      $('#src-kaodian>option:selected').appendTo($('#tar-kaodian'));
    });

    //4.选中的到左边.
    $('#btn-back').click(function () {
      //找到右边select下拉菜单中,被选中的option项,把这些option项添加到左边的select下拉菜单中.
      $('#tar-kaodian>option:selected').appendTo($('#src-kaodian'));
    });

    /** 保存按钮 **/
    $('#btn-kaodian-save').click(function () {
        var btn_target = $(this);
        if( btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交");
                return;
        }
        btn_target.addClass("disabled");

        var tar_kaodian = $("#tar-kaodian>option");
        //console.log(tar_kaodian);
        //声明一个盒子
        var array = [];
        $(tar_kaodian).each(function(){
            var json = {kaodianid: 0,kaodianname:""};
            json.kaodianid = $(this).val();
            json.kaodianname = $(this).text();
            array.push(json);
        });
        console.log(array);
        //alert("aaaa");
        var jsongString = { data: JSON.stringify(array) };
        $.ajax({
                url:common_ops.buildUrl("/examset/kaodian"),
                type:'POST',
                data:jsongString,
                dataType:'json',
                success:function ( res ) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function () {
                            /** 完成后，统一跳转到 /examset/kaodian **/
                            window.location.href = common_ops.buildUrl("/examset/kaodian");
                        }
                    }
                    common_ops.alert(res.msg,callback );


                }
        });


    })

    }

};

$(document).ready( function () {
    exam_kaodianset_ops.init();

});