$("document").ready(function(){

    console.log("Init")

    $(".bingo-card__item").on('click', function() {
      console.log("Click")
      var bg = $(this).css("background")
      if (bg.indexOf("96") >= 0)
      {
          $(this).css("background","#32a86d");
      }
      else {
          $(this).css("background","#606060");
          // $(this).toggleClass('after');
      }
      
    });

    $('.clear-button').on('click', function(){
        $('.bingo-card__item').css("background","#606060");
    });
    
});
		
