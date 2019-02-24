/*** Seguirnos *****/
	var_seguirnos="";
	if($('#seguirnos').is(':checked')){
		$("#seguir-si").css("color", "black");
    $("#seguir-no").css("color", "rgba(0,0,0, 0.26)");
	}else{
		$("#seguir-no").css("color", "black");
   	$("#seguir-si").css("color", "rgba(0,0,0, 0.26)");
   	
	}
	
	$("#seguirnos").change(function() {
    if(this.checked) {
      $("#seguir-si").css("color", "black");
      $("#seguir-no").css("color", "rgba(0,0,0, 0.26)");

    }else{
    	$("#seguir-no").css("color", "black");
    	$("#seguir-si").css("color", "rgba(0,0,0, 0.26)");
    	
    }
	});
	
/*** Fin Seguirnos *****/
/*** Hastag *****/
	var_hastag="";
	if($('#hastag').is(':checked')){
		$("#hastag-si").css("color", "black");
    $("#hastag-no").css("color", "rgba(0,0,0, 0.26)");
    $("#hastag-td").css("display", "block");
    
    if ($('#hastag-div').hasClass("is-empty")){
    	$("#hastag-div").addClass("has-error");
   	}else{
   		$("#hastag-div").removeClass("has-error");
   	}

   	

	}else{
		$("#hastag-no").css("color", "black");
   	$("#hastag-si").css("color", "rgba(0,0,0, 0.26)");
   	$("#hastag-td").css("display", "none");
   	var_hastag="";
	}
	
	$("#hastag").change(function() {
    if(this.checked) {
      $("#hastag-si").css("color", "black");
      $("#hastag-no").css("color", "rgba(0,0,0, 0.26)");
      $("#hastag-td").css("display", "block");

	    if ($('#hastag-div').hasClass("is-empty")){
	    	$("#hastag-div").addClass("has-error");
	   	}else{
	   		$("#hastag-div").removeClass("has-error");
	   	}	   	

    }else{
    	$("#hastag-no").css("color", "black");
    	$("#hastag-si").css("color", "rgba(0,0,0, 0.26)");
    	$("#hastag-td").css("display", "none");
    	var_hastag="";
    }
  });
/*** Fin Hastag *****/

/*** Seguir otros *****/
	var_seguir_otros="";
	if($('#seguir-otro').is(':checked')){
		$("#seguir-otro-div-td-2").css("display", "block");
		$("#seguir-otro-si").css("color", "black");
    $("#seguir-otro-no").css("color", "rgba(0,0,0, 0.26)");
    $("#seguir-otro-td").css("display", "block");

    if($('#etiqueta').is(':checked')){
    	$("#seguir-otro-div-td").css("display", "block");
    }else{
    	$("#seguir-otro-div-td").css("display", "none");
    }  

    if ($('#seguir-otro-div-id').hasClass("is-empty")){
    	$("#seguir-otro-div-id").addClass("has-error");
   	}else{
   		$("#seguir-otro-div-id").removeClass("has-error");
   	}

   	

	}else{
		$("#seguir-otro-div-td-2").css("display", "none");
		$("#seguir-otro-no").css("color", "black");
   	$("#seguir-otro-si").css("color", "rgba(0,0,0, 0.26)");
   	$("#seguir-otro-td").css("display", "none");
   	$("#seguir-otro-div-td").css("display", "none");
   	var_seguir_otros="";
	}

	
	
	$("#seguir-otro").change(function() {
    if(this.checked) {
      $("#seguir-otro-si").css("color", "black");
      $("#seguir-otro-no").css("color", "rgba(0,0,0, 0.26)");
      $("#seguir-otro-td").css("display", "block");
      $("#seguir-otro-div-td-2").css("display", "block");
      
      if($('#etiqueta').is(':checked')){
	    	$("#seguir-otro-div-td").css("display", "block");
	    }else{
	    	$("#seguir-otro-div-td").css("display", "none");
	    }

      if ($('#seguir-otro-div-id').hasClass("is-empty")){
       	$("#seguir-otro-div-id").addClass("has-error");
      }else{
      	$("#seguir-otro-div-id").removeClass("has-error");
      }


    }else{
    	$("#seguir-otro-no").css("color", "black");
    	$("#seguir-otro-si").css("color", "rgba(0,0,0, 0.26)");
    	$("#seguir-otro-td").css("display", "none");
    	$("#seguir-otro-div-td-2").css("display", "none");
    	$("#seguir-otro-div-td").css("display", "none");
    	
    	var_seguir_otros="";

    }

    
	});
/*** Fin Seguir otros *****/

/*** Etiquetar amigos *****/
	var_cant_etiqueta="";
	if($('#etiqueta').is(':checked')){
		$("#etiqueta-si").css("color", "black");
    $("#etiqueta-no").css("color", "rgba(0,0,0, 0.26)");
    $("#etiqueta-td").css("display", "block");
    $("#amigos-seguir-div").css("display", "block");
    $("#amigos-seguir-td").css("display", "block");    
    $("#like-otro-div-td").css("display", "block");

    if ($("#seguir-otro").is(':checked')){
    	$("#seguir-otro-div-td").css("display", "block");
    }else{
    	$("#seguir-otro-div-td").css("display", "none");
    }
    
    
	}else{
		$("#etiqueta-no").css("color", "black");
   	$("#etiqueta-si").css("color", "rgba(0,0,0, 0.26)");
   	$("#etiqueta-td").css("display", "none");
   	$("#amigos-seguir-div").css("display", "none");
   	$("#amigos-seguir-td").css("display", "none");
   	$("#error-cantidad-etiqueta").css("display", "none");
   	$("#like-otro-div-td").css("display", "none");
   	$("#seguir-otro-div-td").css("display", "none");
   	var_cant_etiqueta="";

	}

	
	
	$("#etiqueta").change(function() {
    if(this.checked) {
      $("#etiqueta-si").css("color", "black");
      $("#etiqueta-no").css("color", "rgba(0,0,0, 0.26)");
      $("#etiqueta-td").css("display", "block");
      $("#amigos-seguir-div").css("display", "block");
      $("#amigos-seguir-td").css("display", "block");
      $("#like-otro-div-td").css("display", "block");
      
      if ($("#seguir-otro").is(':checked')){
	    	$("#seguir-otro-div-td").css("display", "block");
	    }else{
	    	$("#seguir-otro-div-td").css("display", "none");
	    } 
    }else{
    	$("#etiqueta-no").css("color", "black");
    	$("#etiqueta-si").css("color", "rgba(0,0,0, 0.26)");
    	$("#etiqueta-td").css("display", "none");
    	$("#amigos-seguir-div").css("display", "none");
    	$("#amigos-seguir-td").css("display", "none");
    	$("#error-cantidad-etiqueta").css("display", "none");
    	$("#like-otro-div-td").css("display", "none");
    	$("#seguir-otro-div-td").css("display", "none");
    	var_cant_etiqueta="";
    }

    
	});
/*** Fin Etiquetar amigos *****/

/*** Like ****/
	var_like="";
	if($('#like').is(':checked')){
		
		$("#like-si").css("color", "black");
    $("#like-no").css("color", "rgba(0,0,0, 0.26)");


	}else{
		
		$("#like-no").css("color", "black");
   	$("#like-si").css("color", "rgba(0,0,0, 0.26)");
	}	
	
	$("#like").change(function() {
    if(this.checked) {
      $("#like-si").css("color", "black");
      $("#like-no").css("color", "rgba(0,0,0, 0.26)");

    }else{
    	$("#like-no").css("color", "black");
    	$("#like-si").css("color", "rgba(0,0,0, 0.26)");
    }

    
	});
/*** Fin Like ****/

/*** Amigos Segirme *****/
	var_amigos_seguirme="";
	if($('#amigos-seguir').is(':checked')){
		$("#amigos-seguir-si").css("color", "black");
    $("#amigos-seguir-no").css("color", "rgba(0,0,0, 0.26)");    
    
	}else{
		$("#amigos-seguir-no").css("color", "black");
   	$("#amigos-seguir-si").css("color", "rgba(0,0,0, 0.26)");
	}
	
	$("#amigos-seguir").change(function() {
    if(this.checked) {
      $("#amigos-seguir-si").css("color", "black");
      $("#amigos-seguir-no").css("color", "rgba(0,0,0, 0.26)");

    }else{
    	$("#amigos-seguir-no").css("color", "black");
    	$("#amigos-seguir-si").css("color", "rgba(0,0,0, 0.26)");
    }
	});
/* Fin Amigos Segirme*/

/*** Amigos Segir Otros Usuarios *****/
	var_amigos_seguir_otros="";
	if($('#amigos-seguir-otro').is(':checked')){
		
		$("#amigos-seguir-otro-si").css("color", "black");
    $("#amigos-seguir-otro-no").css("color", "rgba(0,0,0, 0.26)");
  
    

	}else{
		
		$("#amigos-seguir-otro-no").css("color", "black");
   	$("#amigos-seguir-otro-si").css("color", "rgba(0,0,0, 0.26)");
	
	}
	
	$("#amigos-seguir-otro").change(function() {
    if(this.checked) {
    	
      $("#amigos-seguir-otro-si").css("color", "black");
      $("#amigos-seguir-otro-no").css("color", "rgba(0,0,0, 0.26)");
    
      
    }else{

    	$("#amigos-seguir-otro-no").css("color", "black");
    	$("#amigos-seguir-otro-si").css("color", "rgba(0,0,0, 0.26)");
    }
	});
/*** Fin Amigos Segir Ottros Usuarios *****/

/*** Amigos Like Otros Usuarios *****/
	var_amigos_like_otros="";
	if($('#amigos-like-otro').is(':checked')){
		
		$("#amigos-like-otro-si").css("color", "black");
    $("#amigos-like-otro-no").css("color", "rgba(0,0,0, 0.26)");
  
    

	}else{
		
		$("#amigos-like-otro-no").css("color", "black");
   	$("#amigos-like-otro-si").css("color", "rgba(0,0,0, 0.26)");
	
	}
	
	$("#amigos-like-otro").change(function() {
    if(this.checked) {
    	
      $("#amigos-like-otro-si").css("color", "black");
      $("#amigos-like-otro-no").css("color", "rgba(0,0,0, 0.26)");
    
      
    }else{

    	$("#amigos-like-otro-no").css("color", "black");
    	$("#amigos-like-otro-si").css("color", "rgba(0,0,0, 0.26)");
    }
	});
/*** Fin Amigos Like Ottros Usuarios *****/

/**** validar el numero de amigos a etiquetar *****/
	$("#cantidad-etiqueta").change(function(){
		if ($("#cantidad-etiqueta").val()<= 0){
			$("#error-cantidad-etiqueta").css("display", "block");
		}else{
			$("#error-cantidad-etiqueta").css("display", "none");
		}
	});
/****FIN validar el numero de amigos a etiquetar****/
 
/* Vista Compartir */
$("#previa-id").click(function(){
	/* Var Seguirnos */
  	if($('#seguirnos').is(':checked')){		
      var_seguirnos="- Debes seguirnos\n";
      ajax_seguirnos = 1;
  	}else{
  		
     	var_seguirnos="";
      ajax_seguirnos =0;
  	}
	/* Fin Var Seguirnos */
	
	/* Var Like */
  	if($('#like').is(':checked')){
      var_like= "- Debes darle like a esta foto\n";
      ajax_like = 1;
  	}else{
     	var_like="";
      ajax_like = 0;
  	}	
	/* Fin Var Like */

	/* Var Hastag */
  	if($("#hastag-text").val()!="" && $('#hastag').is(':checked')){
  		harr=$("#hastag-text").val().split(" ")
  		if (harr.length > 1 && harr[1]!=""){
  			var_hastag="- Debes usar los hastags: "+$("#hastag-text").val()+"\n";	
        ajax_hastag = $("#hastag-text").val();
  		}else{
  			var_hastag="- Debes usar el hastag: "+$("#hastag-text").val()+"\n";
        ajax_hastag = $("#hastag-text").val();
  		}
   		
   	
   	}else if (!$('#hastag').is(':checked')){
   		var_hastag="";
      ajax_hastag = "";
   	}else if($("#hastag-text").val()=="" && $('#hastag').is(':checked')){
      $("#condiciones").click()
      demo.showNotificationError('top','center','No debes dejar el espacio del Hastag vacio');
    }

 	/* Fin Var Hastag */

 	/* Var Seguir a otros usuarios */
    if($("#segir-otro-text").val() != "" && $('#seguir-otro').is(':checked')){
   	
   		var_seguir_otros="- Debes seguir estas cuentas: "+$("#segir-otro-text").val()+"\n";
      ajax_seguir_otros = $("#segir-otro-text").val();
   	}else if (!$('#seguir-otro').is(':checked')){
   		var_seguir_otros="";
      ajax_seguir_otros = "";
   	}else if($("#segir-otro-text").val() == "" && $('#seguir-otro').is(':checked')){
      $("#condiciones").click()
      demo.showNotificationError('top','center','No debes dejar el espacio de las cuentas a seguir vacio');
    }
 	/* Fin Var Seguir a otros usuarios */

 	/* Var Catidad de usuarios a etiquetar */
  
   	if ($("#cantidad-etiqueta").val() > 0 && $('#etiqueta').is(':checked')){
    	if ($("#cantidad-etiqueta").val() == 1){
    	
    		var_cant_etiqueta="- Etiquetar a "+$("#cantidad-etiqueta").val() + " amigo\n";
        ajax_cant_etiqueta = $("#cantidad-etiqueta").val();
    	}else{
    	
    		var_cant_etiqueta= "- Etiquetar a "+$("#cantidad-etiqueta").val() + " amigos\n";
        ajax_cant_etiqueta = $("#cantidad-etiqueta").val();
    	}
    	
    }else if(!$('#etiqueta').is(':checked')){
    	var_cant_etiqueta=""
      ajax_cant_etiqueta = 0;
    }else if($("#cantidad-etiqueta").val() == "" && $('#etiqueta').is(':checked')){
      demo.showNotificationError('top','center','Debes decidir que cantidad de amigos se etiquetaran');
    }
  /* Fin Var Catidad de usuarios a etiquetar */

  /* Amigos Seguirme */
    if($('#amigos-seguir').is(':checked') && $('#etiqueta').is(':checked')){
    	
      var_amigos_seguirme="- Tus amigos etiquetados deben seguir a nuestra cuenta\n";
      ajax_amigos_seguirme = 1;
    }else{
    	var_amigos_seguirme="";
      ajax_amigos_seguirme = 0;
    }
  /* Fin amigos Seguirme */

  /* Amigos seguir a otros usuarios*/
    if($('#amigos-seguir-otro').is(':checked') && $('#seguir-otro').is(':checked') && $('#etiqueta').is(':checked') ){
  	  var_amigos_seguir_otros="- Tus amigos etiquetados deben seguir a las cuentas nombradas\n";
      ajax_amigos_seguir_otros = 1;
  	}else{
  		var_amigos_seguir_otros="";
      ajax_amigos_seguir_otros = 0;
  	}
	/* Fin amigos seguir otros usuarios*/



  /* Amigos Like a este post*/
    if($('#amigos-like-otro').is(':checked') && $('#etiqueta').is(':checked')){

      var_amigos_like_otros="- Tus amigos etiquetados deben hacer like a esta publicación\n"; 
      ajax_amigos_like_otros = 1; 	

  	}else{
  		var_amigos_like_otros="";
      ajax_amigos_like_otros = 0;   
  	}
	/* Fin amigos seguir otros usuarios*/
  /* Ganadores */
    if($('#ganadores-text').val() > 0 ){
      if($('#ganadores-text').val() == 1 ){
        var_ganadores = "- Se elegirá un solo ganador\n";
      }else{
        var_ganadores = "- Se elegirán "+ $('#ganadores-text').val() +" ganadores\n";
      }
      
      ajax_ganadores = $('#ganadores-text').val();
    }else{
      demo.showNotificationError('top','center','Debes indicar la cantidad de Ganadores para el concurso');
    }
  /* Fin Ganadores */
	$("#comentario").val( var_seguirnos+ var_like+var_hastag+var_seguir_otros+var_cant_etiqueta+var_amigos_like_otros+var_amigos_seguirme+var_amigos_seguir_otros);
  });

$("#share-id").click(function(){
  
  /* Var Seguirnos */
    if($('#seguirnos').is(':checked')){   
      var_seguirnos="- Debes seguirnos\n";
      ajax_seguirnos = 1;
    }else{
      
      var_seguirnos="";
      ajax_seguirnos =0;
    }
  /* Fin Var Seguirnos */
  
  /* Var Like */
    if($('#like').is(':checked')){
      var_like= "- Debes darle like a esta foto\n";
      ajax_like = 1;
    }else{
      var_like="";
      ajax_like = 0;
    } 
  /* Fin Var Like */

  /* Var Hastag */
    if($("#hastag-text").val()!="" && $('#hastag').is(':checked')){
      harr=$("#hastag-text").val().split(" ")
      if (harr.length > 1 && harr[1]!=""){
        var_hastag="- Debes usar los hastags: "+$("#hastag-text").val()+"\n"; 
        ajax_hastag = $("#hastag-text").val();
      }else{
        var_hastag="- Debes usar el hastag: "+$("#hastag-text").val()+"\n";
        ajax_hastag = $("#hastag-text").val();
      }
      
    
    }else if (!$('#hastag').is(':checked')){
      var_hastag="";
      ajax_hastag = "";
    }else if($("#hastag-text").val()=="" && $('#hastag').is(':checked')){
      $("#condiciones").click()
      demo.showNotificationError('top','center','No debes dejar el espacio del Hastag vacio');
    }

  /* Fin Var Hastag */

  /* Var Seguir a otros usuarios */
    if($("#segir-otro-text").val() != "" && $('#seguir-otro').is(':checked')){
    
      var_seguir_otros="- Debes seguir estas cuentas: "+$("#segir-otro-text").val()+"\n";
      ajax_seguir_otros = $("#segir-otro-text").val();
    }else if (!$('#seguir-otro').is(':checked')){
      var_seguir_otros="";
      ajax_seguir_otros = "";
    }else if($("#segir-otro-text").val() == "" && $('#seguir-otro').is(':checked')){
      $("#condiciones").click()
      demo.showNotificationError('top','center','No debes dejar el espacio de las cuentas a seguir vacio');
    }
  /* Fin Var Seguir a otros usuarios */

  /* Var Catidad de usuarios a etiquetar */
  
    if ($("#cantidad-etiqueta").val() > 0 && $('#etiqueta').is(':checked')){
      if ($("#cantidad-etiqueta").val() == 1){
      
        var_cant_etiqueta="- Etiquetar a "+$("#cantidad-etiqueta").val() + " amigo\n";
        ajax_cant_etiqueta = $("#cantidad-etiqueta").val();
      }else{
      
        var_cant_etiqueta= "- Etiquetar a "+$("#cantidad-etiqueta").val() + " amigos\n";
        ajax_cant_etiqueta = $("#cantidad-etiqueta").val();
      }
      
    }else if(!$('#etiqueta').is(':checked')){
      var_cant_etiqueta=""
      ajax_cant_etiqueta = 0;
    }else if($("#cantidad-etiqueta").val() == "" && $('#etiqueta').is(':checked')){
      demo.showNotificationError('top','center','Debes decidir que cantidad de amigos se etiquetaran');
    }
  /* Fin Var Catidad de usuarios a etiquetar */

  /* Amigos Seguirme */
    if($('#amigos-seguir').is(':checked') && $('#etiqueta').is(':checked')){
      
      var_amigos_seguirme="- Tus amigos etiquetados deben seguir a nuestra cuenta\n";
      ajax_amigos_seguirme = 1;
    }else{
      var_amigos_seguirme="";
      ajax_amigos_seguirme = 0;
    }
  /* Fin amigos Seguirme */

  /* Amigos seguir a otros usuarios*/
    if($('#amigos-seguir-otro').is(':checked') && $('#seguir-otro').is(':checked') && $('#etiqueta').is(':checked') ){
      var_amigos_seguir_otros="- Tus amigos etiquetados deben seguir a las cuentas nombradas\n";
      ajax_amigos_seguir_otros = 1;
    }else{
      var_amigos_seguir_otros="";
      ajax_amigos_seguir_otros = 0;
    }
  /* Fin amigos seguir otros usuarios*/



  /* Amigos Like a este post*/
    if($('#amigos-like-otro').is(':checked') && $('#etiqueta').is(':checked')){

      var_amigos_like_otros="- Tus amigos etiquetados deben hacer like a esta publicación\n"; 
      ajax_amigos_like_otros = 1;   

    }else{
      var_amigos_like_otros="";
      ajax_amigos_like_otros = 0;   
    }
  /* Fin amigos seguir otros usuarios*/
  /* Ganadores */
    if($('#ganadores-text').val() > 0 ){
      if($('#ganadores-text').val() == 1 ){
        var_ganadores = "- Se elegirá un solo ganador\n";
      }else{
        var_ganadores = "- Se elegirán "+ $('#ganadores-text').val() +" ganadores\n";
      }
      
      ajax_ganadores = $('#ganadores-text').val();
    }else{
      demo.showNotificationError('top','center','Debes indicar la cantidad de Ganadores para el concurso');
    }
  /* Fin Ganadores */
	mensaje_final= $("#encabezado-publi").val()+"\n"+ var_seguirnos+ var_like+var_hastag+var_seguir_otros+var_cant_etiqueta+var_amigos_like_otros+var_amigos_seguirme+var_amigos_seguir_otros +$("#pie-publi").val();
  
  mensaje_final_html =$("#encabezado-publi").val()+"<br>"+ var_seguirnos+ "<br>"+ var_like+"<br>"+ var_hastag+"<br>"+ var_seguir_otros+"<br>"+ var_cant_etiqueta+"<br>"+ var_amigos_like_otros+"<br>"+ var_amigos_seguirme+"<br>"+ var_amigos_seguir_otros +"<br>"+  $("#pie-publi").val();
  $("#comentario-final").html(mensaje_final_html);

	

	
});