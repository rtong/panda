var META_DICT = {};
var CAT_DICT = {};
var gi = gi || {};

var giHost = window.location.host;
var giProtocol = (document.location.protocol == "https:") ? "https://" : "http://";

function $g(keyid){ return document.getElementById(keyid); }
function $n(keyn){ return document.getElementsByName(keyn); }

gi.suggest = {
	getSearch: function(myEvent, suggVal){
	    myEvent=window.event || myEvent;
	    this.iKeyCode=myEvent.keyCode;
	    this.suggVal = suggVal;		    
	    this.getApi();    			
	},
	getApi: function(){		
		if(this.suggVal.length==0){load(); return; }	
		if(this.suggVal.length<3){	
			this.hideCity();    
	    } else if ((this.iKeyCode < 32 && this.iKeyCode != 8) || (this.iKeyCode >= 33 && this.iKeyCode <= 46) || (this.iKeyCode >= 112 && this.iKeyCode <= 123)){
	    	this.keyHandler();
	    } else {
	    	this.nowElm = -1;	    	
                this.suggVal = this.suggVal;
	    	gi.ajax.get({
				url: '/home/?',
				params: 'search='+this.suggVal,
				success: 'homeSuccess'
			});
	    }				
	},
        renderResult: function(cityJson){
		cityJson = eval(cityJson);
                console.log(cityJson);

		if(cityJson.length==0){ this.hidePlaces(); return false; }				
                $g('result').innerHTML = cityCode;
        },
	keyHandler: function(){		
	    switch(this.iKeyCode){
	       case 38: 
	          /*this.goUp();*/
	          break;
	       case 40: 
	          /*this.goDown();*/
	          break;
	       case 13:	       	  
	       	  this.hideCity();	  	       	        	  
	       	  break;
	       case 9:	       	 
	       	  this.hideCity();    
	          break;	       
	    }
 	},
 	hideCity: function(){		
	},
 	hidePlaces: function(){		
                $g('result').innerHTML = '';
	},
 	about: function(){		
		$g('aboutus').className = 'center';
	},
 	goUp: function(){
	    if(nodeCount>0 && this.nowElm>0){
	       --this.nowElm;	       
	       for(var i=0;i<nodeCount;i++){
	          if(i==this.nowElm){
	          }else{
	             this.getElm.childNodes[i].className="";
	          }
	       }
	    }
	},
	goDown: function(){
	    if(nodeCount>0 && this.nowElm<(nodeCount-1)){
	       ++this.nowElm;	      
	       for(var i=0;i<nodeCount;i++){
	          if(i==this.nowElm){
	          }else{
	          }
	       }
	    }
	},	
}

function homeSuccess(cityJson){ gi.suggest.renderResult(cityJson); }
function load(){
    data = $g('data').value;
    gi.suggest.renderResult(data);
}

gi.ajax = {
	getAjaxObject: function(){
		var goHttp = false;
		if(window.XMLHttpRequest){ goHttp = new XMLHttpRequest(); }
		else if(window.ActiveXObject){
			try{ goHttp = new ActiveXObject('Msxml2.XMLHTTP'); }
			catch(ef){ try{ goHttp = new ActiveXObject('Microsoft.XMLHTTP'); }
			catch(es){ this.getError('Please enable Javascript'); }}
		}
		return goHttp;		
	},
	getAjaxReady: function(getHttp, callSuccess){		
		return function(){
			if(getHttp.readyState == 4){
				if(getHttp.status == 200){ window[callSuccess](getHttp.responseText); giajst = 0; /*alert(getHttp.responseText);*/ }
				else{ this.getError('Sorry we are facing some issue in processing your request'); giajst = 0; }				
			}					
		}
	},
	post: function(giObj){		
		var getHttp = this.getAjaxObject();		
		getHttp.onreadystatechange = this.getAjaxReady(getHttp, giObj.success);
		getHttp.open('POST', giObj.url, true);
		getHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		getHttp.send(giObj.params);		
	},
	get: function(giObj){		
		var getHttp = this.getAjaxObject();		
		getHttp.onreadystatechange = this.getAjaxReady(getHttp, giObj.success);
		getHttp.open('GET', giObj.url+giObj.params, true);
		getHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		getHttp.send();		
	},
	getError : function(errMsg){
		$('gerb').className = 'db';	
		$('gerb').innerHTML = '<em>'+errMsg+'</em>';		
	},
	getSetting: function(settId){			
		if($(settId).className == 'dn'){ $(settId).className = 'db'; giOpenSett = settId;  }
		else{ $(settId).className = 'dn' }			
	},
	closeSetting: function(){			
		if(giOpenSett != ''){ $(giOpenSett).className = 'dn'; }		
	} 
};

