;
var food_set_ops = {
    init:function () {
        this.eventBind();
        this.initEditor();
    },
    eventBind:function () {

    },
    initEditor:function () {
        var that = this;
        that.ue = UE.getEditor('editor',{
            toolbar:[
                [ 'undo', 'redo', '|',
                     'bold', 'italic', 'underline', 'strikethrough', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall',  '|','rowspacingtop', 'rowspacingbottom', 'lineheight'],
                [ 'customstyle', 'paragraph', 'fontfamily', 'fontsize','|','directionalityltr', 'directionalityrtl', 'indent', '|',
                    'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
                    'link', 'unlink'],
                [ 'imagenone', 'imageleft', 'imageright', 'imagecenter', '|','insertimage', 'insertvideo', '|',
                    'horizontal', 'spechars','|','inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols' ]
            ],
            enableAutoSave:true,           //是自动保存
            saveInterval:60000,            //自动保存时间
            elementPathEnabled:false,     //下方显示保存路径 ：否
            zIndex:4,
            serverUrl:common_ops.buildUrl("/upload/ueditor")
        });


    }
};

$(document).ready(function () {
    food_set_ops.init();
});