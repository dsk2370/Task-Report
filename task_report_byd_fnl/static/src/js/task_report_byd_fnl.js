$(function() {
	$(document).on('click', "#refresh", function () {
		  location.reload();
	  });
    
    //   onclick of the image this is called and data is fetched by json call and rendered
    $(document).on('click', ".clickbl1", function () {
      
      $("#myModal").modal("show");
      $.getJSON('/get/'+this.id+'/user_data', {}, function(result) {
        $('#qres').DataTable( {
                    
          data: result,
         pagination: "bootstrap",
         filter:true, 
         destroy: true,
         lengthMenu:[5,10,25],
         pageLength: 10,
         "columns":[  
                     {     "data"     :     "project"     },
                     {     "data"     :     "open_count"},  
                     {     "data"     :     "delay_count"},
                     {     "data"     :     "month_count"     },
                     {     "data"     :     "week_count"     },
                ],
                
       } );		
      });
  });
    
    //   onclick of the report action(Kanban View) this is called and data is fetched by json call and rendered
    //   We are using datatables library here for better view of report.
  $.getJSON('/get/tasks', {}, function(result) {
		$('.oe_kanban_groups').css( "width", "100%" );
    $('.oe_kanban_record').css( "width", "100%" );
            $('#task_report').DataTable( {
                    
                    data: result,
                    
                    "columnDefs": [
                   {targets: 0,
                    className: "clickbl1",
                    "createdCell": function(td, data, rowData, row, col) {
                        $(td).attr('id', data[2]);
                      },
                    "render": function (data, type, meta) {
                        return '<img class="img-circle" width="25" height="25" src="'+data[0]+'">'+' '+'<span>'+data[1]+'</span>';
                    }},
                    { "searchable": true, "targets": 1},
                                
                ],
                   pagination: "bootstrap",
                   filter:true,
                   destroy: true,
                   lengthMenu:[5,10,25],
                   pageLength: 10,
                   "columns":[  
                               {     "data"     :     "img_link"     },
                               {     "data"     :     "name"},  
                               {     "data"     :     "date_deadline"},
                               {     "data"     :     "project"     },
                               {     "data"     :     "status"     },
                          ],
                          
                 } );		
	});
});