<script language="JavaScript">
	$("#ddSubGenres").on("change", function(){
	  var selectedValue = $(this).text();
	  
	  $.ajax({
	    url : "subGenreSelectHandler/",
	    type : "POST",
	    data : {"subGenre" : selectedValue},
	    dataType : "json",
	    success : function(){
	    }
	  });
	});
</script>