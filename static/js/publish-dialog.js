
(function() {

    var factory = function (exports) {

		var pluginName   = "publish-dialog";

		exports.fn.publishDialog = function() {

            var _this       = this;
            var cm          = this.cm;
            var lang        = this.lang;
            var editor      = this.editor;
            var settings    = this.settings;
            var cursor      = cm.getCursor();
            var selection   = cm.getSelection();
            var imageLang   = lang.dialog.image;
            var classPrefix = this.classPrefix;
            var iframeName  = classPrefix + "image-iframe";
			var dialogName  = classPrefix + pluginName, dialog;

			cm.focus();

            var loading = function(show) {
                var _loading = dialog.find("." + classPrefix + "dialog-mask");
                _loading[(show) ? "show" : "hide"]();
            };

            if (editor.find("." + dialogName).length < 1)
            {
                var guid   = (new Date).getTime();
                var action = settings.imageUploadURL + (settings.imageUploadURL.indexOf("?") >= 0 ? "&" : "?") + "guid=" + guid;

                if (settings.crossDomainUpload)
                {
                    action += "&callback=" + settings.uploadCallbackURL + "&dialog_id=editormd-publish-dialog-" + guid;
                }

                var dialogContent = ( (settings.imageUpload) ? "<form action=\"" + action +"\" target=\"" + iframeName + "\" method=\"post\" enctype=\"multipart/form-data\" class=\"" + classPrefix + "form\">" : "<div class=\"" + classPrefix + "form\">" ) +
                                        ( (settings.imageUpload) ? "<iframe name=\"" + iframeName + "\" id=\"" + iframeName + "\" guid=\"" + guid + "\"></iframe>" : "" ) +
                                        "<label>标题</label>" +
                                        "<input type=\"text\" data-url />" + (function(){
                                            return (settings.imageUpload) ? "<div class=\"" + classPrefix + "file-input\">" +
                                                                                "<input type=\"file\" name=\"" + classPrefix + "image-file\" accept=\"image/*\" />" +
                                                                                "<input type=\"submit\" value=\"" + imageLang.uploadButton + "\" />" +
                                                                            "</div>" : "";
                                        })() +
                                        "<br/>" +
                                        "<label>分类</label>" +
                                        "<input type=\"text\" value=\"" + selection + "\" data-alt />" +
                                        "<br/>" +
                                        "<label>标签</label>" +
                                        "<input type=\"text\" value=\"\" data-link />" +
                                        "<br/>" +
                                        "<label>文件名</label>" +
                                        "<input type=\"text\" value=\"\" data-name />" +
                                        "<br/>" +
                                        "<label>管理密码</label>" +
                                        "<input type=\"password\" value=\"\" data-password />" +
                                        "<br/>" +
                                    ( (settings.imageUpload) ? "</form>" : "</div>");
				// dialog定义开始
                dialog = this.createDialog({
                    title      : '发布',
                    width      : 380,
                    height     : 330,
                    name       : dialogName,
                    content    : dialogContent,
                    mask       : settings.dialogShowMask,
                    drag       : settings.dialogDraggable,
                    lockScreen : settings.dialogLockScreen,
                    maskStyle  : {
                        opacity         : settings.dialogMaskOpacity,
                        backgroundColor : settings.dialogMaskBgColor
                    },
                    buttons : {
                        enter : ['确定发布', function() {
                            var url  = this.find("[data-url]").val();
                            var alt  = this.find("[data-alt]").val();
                            var link = this.find("[data-link]").val();
                            var name = this.find("[data-name]").val();
                            var password = this.find("[data-password]").val();

                            if (url === ""){
                                alert('标题不能为空');
                                return false;
                            }
                            if (name === ""){
                                alert('保存的文件名不能为空');
                                return false;
                            }
                            var dia = this;
		                    function publish_success(){
			                    dia.hide().lockScreen(false).hideMask();
			                    //cm.setValue('');
		                    }
							$.ajax( {  
							    url: '/publish',
							    data:{
							    	title: url,
							    	cat: alt,
							    	tag: link,
							    	name: name,
							    	password: password,
							    	content: cm.getValue()
							    },  
							    type: 'post',  
							    success: function(data) {  
							        if(data.code ==0 ){  
										var msg = "发布成功！\n\n是否去首页查看？"; 
										if (confirm(msg)==true){ 
										    window.location.href = '/';
										}else{ }
							            publish_success();
							        }else{  
							            alert(data.msg);  
							        }  
							     },  
							     error : function() {  
							          alert("服务器异常！请稍后重试");  
							     }
							});
                        }],

                        cancel : ['取消', function() {
                            this.hide().lockScreen(false).hideMask();
                            return false;
                        }]
                    }
                });
				// dialog定义结束
                dialog.attr("id", classPrefix + "publish-dialog-" + guid);
            }

			dialog = editor.find("." + dialogName);
			dialog.find("[type=\"text\"]").val("");
			dialog.find("[type=\"file\"]").val("");
			dialog.find("[data-link]").val("");

			this.dialogShowMask(dialog);
			this.dialogLockScreen();
			dialog.show();

		};

	};

	// CommonJS/Node.js
	if (typeof require === "function" && typeof exports === "object" && typeof module === "object")
    {
        module.exports = factory;
    }
	else if (typeof define === "function")  // AMD/CMD/Sea.js
    {
		if (define.amd) { // for Require.js

			define(["editormd"], function(editormd) {
                factory(editormd);
            });

		} else { // for Sea.js
			define(function(require) {
                var editormd = require("./../../editormd");
                factory(editormd);
            });
		}
	}
	else
	{
        factory(window.editormd);
	}

})();
