


function tableFilter() {
  var filter_category, filter_view_count, filter_start_date, filter_end_date, filter_creator,  filter, table, tr, td, i, txtValue;
  filter_view_count = document.getElementById("filter_view_count");
  filter_category = document.getElementById("filter_category");
  filter_start_date = document.getElementById("filter_start_date");
  filter_end_date = document.getElementById("filter_end_date");
  filter_creator = document.getElementById("filter_creator");
  console.log(`PARAMS Views: ${filter_view_count.value} Category: ${filter_category.value} Start: ${filter_start_date.value} End: ${filter_end_date.value} Creator: ${filter_creator.value}`)
  table = document.getElementById("clips_table");
  tr = table.getElementsByTagName("tr");
  
  tableReset()
  
  // filter category selection
  for (i = 0; i < tr.length; i++) {
    if (filter_category.value != "All Categories") {  
        
        filter = filter_category.value.toUpperCase();
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
          // console.log(td)
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) <= -1) {
            tr[i].style.display = "none";
          }
        }       
      }
      
    if (filter_start_date.value) {  
        
        td = tr[i].getElementsByTagName("td")[3];
        if (td) {
          // console.log(td)
          row_date = moment(td.innerText,"YYYY-MM-DD").toDate();
          filter_date = moment(filter_start_date.value,"YYYY-MM-DD").toDate();
          // console.log(row_date, filter_date)
          if (row_date < filter_date) {
            tr[i].style.display = "none";
          }
        }       
      }
    if (filter_end_date.value) {  
        
        td = tr[i].getElementsByTagName("td")[3];
        if (td) {
          // console.log(td)
          row_date = moment(td.innerText,"YYYY-MM-DD").toDate();
          filter_date = moment(filter_end_date.value,"YYYY-MM-DD").toDate();
          // console.log(row_date, filter_end_date.value, filter_date)
          if (row_date > filter_date) {
            tr[i].style.display = "none";
          }
        }       
      }
    
    if (filter_creator.value != "All") {  
        
        filter = filter_creator.value.toUpperCase();
        td = tr[i].getElementsByTagName("td")[4];
        if (td) {
          // console.log(td)
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) <= -1) {
            tr[i].style.display = "none";
          }
        }       
      }
      
    if (filter_view_count.value) {
        td = tr[i].getElementsByTagName("td")[5];
        if (td) {
          // console.log(td.innerText)
          if (parseInt(td.innerText) < parseInt(filter_view_count.value)) {
            tr[i].style.display = "none";
          }
        }       
      }
    }
}
function tableReset() {
      var table, tr, td, i;
      table = document.getElementById("clips_table");
      tr = table.getElementsByTagName("tr");
      
          for (i = 0; i < tr.length; i++) {
                tr[i].style.display = "";
              }
          
            }


// $(document).ready(function(){
// var hidden_output = 1


// $(document).off().on('click','.resulttree',function() {
    // console.log('Click');
    // var query = $(this).children('.output');
    // var isVisible = query.is(':visible');
    // if (isVisible === true) {
       // query.hide();
    // } else {
       // query.show();
    // }
// });



// $(document).on('click','.hideoutput',function() {
    // console.log('Hide/show all');
    // if (hidden_output == 0){
        // console.log('Call hide');
        // $('.resulttree').children('.output').hide() 
        // hidden_output = 1
    // }
    // else  {
        // console.log('Call show');
        // $('.resulttree').children('.output').show()
        // hidden_output = 0
    // }
// });

// $('.resulttree').children('.output').hide();
// })
