
function delete_post(raw_url, callback){
	var msg = "确定删除？"; 
	if (confirm(msg)==true){ 
	
		$.ajax({  
		    url: '/delete_post',
		    data:{
		    	raw_url: raw_url,
		    },  
		    type: 'post',  
		    success: function(data) {  
		        if(data.code ==0 ){  
		        	if(callback){
		        		callback();
		        	}else{
		        		window.location.href = '/';
		        	}
		        }else if(data.code ==-2){
		        	href = '/auth/login?pop=1';
		            var win = window.open(href, 'login_window', 'height=450,width=780,resizable=yes,scrollbars=yes');
		            win.focus();
		        }  
		     },  
		     error : function() {  
		          alert("服务器异常！请稍后重试");  
		     }
		});
	
	}else{ }
}
