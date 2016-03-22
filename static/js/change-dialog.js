
(function() {

    var factory = function (exports) {

		var pluginName   = "change-dialog";

		exports.fn.changeDialog = function(raw_url, init) {

            var _this       = this;
            var cm          = this.cm;
            var lang        = this.lang;
            var editor      = this.editor;
            var settings    = this.settings;
            var cursor      = cm.getCursor();
            var selection   = cm.getSelection();
            var classPrefix = this.classPrefix;
			var dialogName  = classPrefix + pluginName, dialog;
			var raw_url = raw_url;

			cm.focus();

            var loading = function(show) {
                var _loading = dialog.find("." + classPrefix + "dialog-mask");
                _loading[(show) ? "show" : "hide"]();
            };

            if (editor.find("." + dialogName).length < 1)
            {
                var guid   = (new Date).getTime();

                var dialogContent = ("<div class=\"" + classPrefix + "form\">" ) +
                                        "<label>标题</label>" +
                                        "<input type=\"text\" style=\"height: 33px\" data-title />" + (function(){
                                            return "";
                                        })() +
                                        "<br/>" +
                                        "<label>分类</label>" +
                                        "<input type=\"text\" style=\"height: 33px\" value=\"" + selection + "\" data-cat />" +
                                        "<br/>" +
                                        "<label>标签</label>" +
                                        "<input type=\"text\" style=\"height: 33px\" value=\"\" data-tag />" +
                                        "<br/>" +
                                        "<label></label>" +
                                        "<input id=\"private\" type=\"checkbox\" value=\"1\" data-private /> 私密" +
                                        "<br/>" +
                                    ("</div>");
				// dialog定义开始
                dialog = this.createDialog({
                    title      : '发布',
                    width      : 380,
                    height     : 300,
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
                        enter : ['保存', function() {
                            var title  = this.find("[data-title]").val();
                            var cat  = this.find("[data-cat]").val();
                            var tag = this.find("[data-tag]").val();
                            var private = document.getElementById("private").checked;

                            if (title === ""){
                                alert('标题不能为空');
                                return false;
                            }
                            var dia = this;
		                    function change_success(){
			                    dia.hide().lockScreen(false).hideMask();
		                    }
							$.ajax( {  
							    url: '/save_head',
							    data:{
							    	raw_url: raw_url,
							    	title: title,
							    	cat: cat,
							    	tag: tag,
							    	private: private?'on': '',
							    	content: cm.getValue()
							    },  
							    type: 'post',  
							    success: function(data) {  
							        if(data.code ==0 ){
							        	$.bootstrapGrowl("修改成功！", { type: 'success',align: 'center',width: 'auto',allow_dismiss: false ,offset: {from: 'top', amount: 60}});
							            change_success();
							        }else if(data.code ==-2){
							        	href = '/auth/login?pop=1';
							            var win = window.open(href, 'login_window', 'height=450,width=780,resizable=yes,scrollbars=yes');
							            alert('请先登录');
							        }
							        else{  
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
                dialog.attr("id", classPrefix + "change-dialog-" + guid);
            }

			dialog = editor.find("." + dialogName);
			dialog.find("[data-title]").val(init.title);
			dialog.find("[data-cat]").val(init.cat);
			dialog.find("[data-tag]").val(init.tag);
			document.getElementById("private").checked = init.private;

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
