;
var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    },
    success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl(file_key) + '"/>'
                + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';

        if ($(".upload_pic_wrap .pic-each").size() > 0) {
            $(".upload_pic_wrap .pic-each").html(html);
        } else {
            $(".upload_pic_wrap").append('<span class="pic-each">' + html + '</span>');
        }
        food_set_ops.delete_img();
    }
};
var food_set_ops = {
    init: function () {
        this.ue = null;
        this.eventBind();
        this.initEditor();
        this.delete_img();
    },
    eventBind: function () {
        var that = this;

        $(".wrap_food_set .upload_pic_wrap input[name=pic]").change(function () {
            $(".wrap_food_set .upload_pic_wrap").submit();
        });

        $(".wrap_food_set select[name=cat_id]").select2({
            language: "zh-CN",
            width: '100%'
        });

        $(".wrap_food_set input[name=tags]").tagsInput({
            width: 'auto',
            height: 40,
            onAddTag: function (tag) {
            },
            onRemoveTag: function (tag) {
            }
        });

        $(".wrap_food_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var cat_id_target = $(".wrap_food_set select[name=cat_id]");
            var cat_id = cat_id_target.val();

            var name_target = $(".wrap_food_set input[name=name]");
            var name = name_target.val();

            var xunkao_id_target = $(".wrap_food_set input[name=xunkao_id]");
            var xunkao_id = xunkao_id_target.val();

            var danwei_target = $(".wrap_food_set input[name=danwei]");
            var danwei = danwei_target.val();

            var bumen_target = $(".wrap_food_set input[name=bumen]");
            var bumen = bumen_target.val();

            var weight_target = $(".wrap_food_set input[name=weight]");
            var weight = weight_target.val();

            var chepai_target = $(".wrap_food_set input[name=chepai]");
            var chepai = chepai_target.val();

            var mobile_target = $(".wrap_food_set input[name=mobile]");
            var mobile = mobile_target.val();

            var sfzh_target = $(".wrap_food_set input[name=sfzh]");
            var sfzh = sfzh_target.val();

            var bankcard_target = $(".wrap_food_set input[name=bankcard]");
            var bankcard = bankcard_target.val();

            var bankaddr_target = $(".wrap_food_set input[name=bankaddr]");
            var bankaddr = bankaddr_target.val();

            var address_target = $(".wrap_food_set input[name=address]");
            var address = address_target.val();


            if (parseInt(cat_id) < 1) {
                common_ops.tip("请选择岗位分类~~", cat_id_target);
                return;
            }

            if (name.length < 1) {
                common_ops.alert("请输入符合规范的姓名~~");
                return;
            }
            if (sfzh.length < 1) {
                sfzh = 0;
            }
            if (weight.length < 1) {
                weight = "C";
            }

            btn_target.addClass("disabled");

            var data = {
                cat_id: cat_id,
                name: name,
                xunkao_id: xunkao_id,
                danwei: danwei,
                bumen: bumen,
                weight: weight,
                chepai: chepai,
                mobile: mobile,
                sfzh: sfzh,
                bankcard: bankcard,
                bankaddr: bankaddr,
                address: address,
                id: $(".wrap_food_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/people/set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/people/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });


    },
    initEditor: function () {
        var that = this;
        that.ue = UE.getEditor('editor', {
            toolbars: [
                ['undo', 'redo', '|',
                    'bold', 'italic', 'underline', 'strikethrough', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|', 'rowspacingtop', 'rowspacingbottom', 'lineheight'],
                ['customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
                    'directionalityltr', 'directionalityrtl', 'indent', '|',
                    'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
                    'link', 'unlink'],
                ['imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
                    'insertimage', 'insertvideo', '|',
                    'horizontal', 'spechars', '|', 'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols']

            ],
            enableAutoSave: true,
            saveInterval: 60000,
            elementPathEnabled: false,
            zIndex: 4,
            serverUrl: common_ops.buildUrl('/upload/ueditor')
        });
    },
    delete_img: function () {
        $(".wrap_food_set .del_image").unbind().click(function () {
            $(this).parent().remove();
        });
    }
};

$(document).ready(function () {
    food_set_ops.init();
});