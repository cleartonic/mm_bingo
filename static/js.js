

$(document).ready(function(){

    console.log("Init")

    $(".bingo-card__item1").on('click', function() {
      console.log("Click")
      var bg = $(this).css("background-color")
      if (bg.indexOf("96") >= 0)
      {
          $(this).css("background-color","#32a86d");
      }
      else {
          $(this).css("background-color","#606060");
          // $(this).toggleClass('after');
      }
      
    });


    
    $(".bingo-card__item2").on('click', function() {
      console.log("Click")
      var bg = $(this).css("background-color")
      if (bg.indexOf("96") >= 0)
      {
          $(this).css("background-color","#32a86d");
      }
      else {
          $(this).css("background-color","#606060");
          // $(this).toggleClass('after');
      }
      
    });


    $(".bingo-card__item3").on('click', function() {
      console.log("Click")
      var bg = $(this).css("background-color")
      if (bg.indexOf("96") >= 0)
      {
          $(this).css("background-color","#32a86d");
      }
      else {
          $(this).css("background-color","#606060");
          // $(this).toggleClass('after');
      }
      
    });

    $('.clear-button').on('click', function(){
        $('.bingo-card__item1').css("background-color","#606060");
        $('.bingo-card__item2').css("background-color","#606060");
        $('.bingo-card__item3').css("background-color","#606060");
    });
    
});
		


var pageX, pageY;

$(document).mousemove(
    function(e){
        pageX = e.pageX;
        pageY = e.pageY;
    });

$('#bingo-card__item]').hover(
    function(){
        var tip = $('<div />')
            .addClass('tooltiptext')
            .text($(this).attr('title'))
            .css({
                'position' : 'absolute',
                'top' : pageY,
                'left' : pageX
            });
        $(tip).appendTo($(this));
        $(this).mousemove(
            function(){
                $('.tooltiptext').css(
                    {
                        'top' : pageY,
                        'left' : pageX
                    });
            });
    },
    function(){
        $('.tooltiptext').remove();
    });