
$(document).ready(function(){

    
    console.log("Init");

    // this dynamically fixes rightside & bottomside squares to anchor differently
    // for tooltips

    var tooltips = document.querySelectorAll('.tooltip-div')
    for (i = 0; i < tooltips.length; i++) {
        
        var tt = tooltips[i];
        tt_idx = parseInt($(tt).attr("idx"));
        // console.log(tt_idx);
        // console.log(tt_idx_bottom_right)
        if ([13, 14, 18,19,22,23,24].indexOf(tt_idx) > -1) {
            // console.log("BR "+ tt_idx);
            $(tt).css(
                {'bottom' : '0', 
                'right' : '0'

                });
        }
        else if ([15,16,20,21].indexOf(tt_idx) > -1) {
            // console.log("BL "+ tt_idx);
            $(tt).css(
                {'bottom' : '0', 
                'left' : '0'
                });
        }
        else if ([3,4, 8, 9].indexOf(tt_idx) > -1) {
            // console.log("TR "+ tt_idx);
            $(tt).css(
                {'top' : '0', 
                'right' : '0'
                });
        }
        else {
            // console.log("TL "+ tt_idx);
            $(tt).css(
                {'top' : '0', 
                'left' : '0'
                });
        };            
            
            
        }
    
   
    
    $('.bingo-card-item').on({
    'mouseover': function () {
        // console.log($(this).children(".tooltip-div"));
        $(this).delay(1100).queue(function () { $(this).children(".tooltip-div").css("display","block").css("clear","both"); $(this).dequeue(); } );

        // console.log("Block");
            
        
    },
    'mouseout' : function () {

        // console.log("None");
        $(this).dequeue();
        $(this).children( ".tooltip-div" ).css("display","none").css("clear","both");
    }
});
    




    $(".bingo-card-item").on('click', function() {
      // console.log("Click")
      var bg = $(this).css("background-color")
      if (bg.indexOf("96") >= 0)
      {
          $(this).css("background-color","#39485c");
      }
      else if (bg.indexOf("57") >= 0) {
          $(this).css("background-color","#32a86d");
          // $(this).toggleClass('after');
      }
      else if (bg.indexOf("168") >= 0) {
          $(this).css("background-color","#520008");
          // $(this).toggleClass('after');
      }
      
      else {
          $(this).css("background-color","#606060");
          // $(this).toggleClass('after');
      }
      
    });



    $('.clear-button').on('click', function(){
        $('.bingo-card-item').css("background-color","#606060");

    });
    
    
    const rcd = [[],
                ["COL 1",0,5,10,15,20],
                ["COL 2",1,6,11,16,21],
                ["COL 3",2,7,12,17,22],
                ["COL 4",3,8,13,18,23],
                ["COL 5",4,9,14,19,24],
                
                ["ROW 1",0,1,2,3,4],
                ["ROW 2",5,6,7,8,9],
                ["ROW 3",10,11,12,13,14],
                ["ROW 4",15,16,17,18,19],
                ["ROW 5",20,21,22,23,24],
                
                ["TL-BR",0,6,12,18,24],
                ["BL-TR",4,8,12,16,20],
                
                ["BOARD",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
          
                
                ];
    
    $('.bingo-card__borders').on('click', function(){
        
        // console.log(this);
        var data_num = parseInt($(this).attr("title"));
        temp_rcd = rcd[data_num];
        
        var tags = document.querySelectorAll('.bingo-card-item');
        // console.log(tags[0]);

        var return_data = [temp_rcd[0]]
        for (i = 0; i < temp_rcd.length; i++) {
            var idx = temp_rcd[i];
            if (i > 0) {
                // console.log(idx);
                match_div = tags[idx]
                // console.log(match_div)
                return_data.push($(match_div).attr("data"));
            };
        }
        
        var settings = document.querySelectorAll('.title')[0];
        var settings_str = $(settings).text();
        return_data.push(settings_str);
        
        if (temp_rcd[0] == "BOARD") {
            width_set = 800;
            height_set = 800;
        }
        else {
            width_set = 300;
            height_set = 650;            
            
        };
        window.open(`bingo-popout?data=${return_data}`, '_blank', `width=${width_set}, height=${height_set}, toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no`);
        
        // silent thank you to OOT bingo devs for this code :bless:
        
        //   window.open(`${prefix}/board-popout.html?seed=${bingoOpts.seed}&mode=${bingoOpts.mode}&version=${bingoOpts.version}${langParamBoard}`, '_blank', `width=${width}, height=${height}, toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no`);
        
        console.log(return_data)
    });
    		


// var pageX, pageY;

// $(document).mousemove(
    // function(e){
        // pageX = e.pageX;
        // pageY = e.pageY;
    // });

// $('#bingo-card-item').hover(
    // function(){
        // var tip = $('<div />')
            // .addClass('bingo-card__tooltipindicator')
            // .text($(this).attr('title'))
            // .css({
                // 'position' : 'absolute',
                // 'top' : pageY,
                // 'left' : pageX
            // });
        // $(tip).appendTo($(this));
        // $(this).mousemove(
            // function(){
                // $('.bingo-card__tooltipindicator').css(
                    // {
                        // 'top' : pageY,
                        // 'left' : pageX
                    // });
            // });
    // },
    // function(){
        // $('.bingo-card__tooltipindicator').remove();
    // });
    
    
var min = 8;
var max = 18;

function changeFontSize(delta) {
  console.log("Font change")
  var tags = document.querySelectorAll('.bingo-card-item');
  for (i = 0; i < tags.length; i++) {
    if (tags[i].style.fontSize) {
      var s = parseInt(tags[i].style.fontSize.replace("px", ""));
    } else {
      var s = 14;
    } s += delta;
    tags[i].style.fontSize = s + "px"
  }
}

function increaseFontSize() {
  changeFontSize(1);
}

function decreaseFontSize() {
  changeFontSize(-1);
}

document.getElementById('increase-font-size').onclick = increaseFontSize;
document.getElementById('decrease-font-size').onclick = decreaseFontSize;

function toggleGames() {
  var tags = document.querySelectorAll('.bingo-card__footer');
  for (i = 0; i < tags.length; i++) {
      if (tags[i].style.display === "none") {
        tags[i].style.display = "flex";
      } else {
        tags[i].style.display = "none";
      }
  }
  
  

}

document.getElementById('toggle-games').onclick = toggleGames;



});