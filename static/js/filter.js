$(document).ready(function(){
    $(".filter-data").on('click',function(){
        var _filterobj={};
        $(".filter-data").each(function(index,ele){
            var _filterVal=$(this).val();
            var _filterKey=$(this).data('filter');
            _filterobj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:active')).map(function(){
               return el.value; 
            });
        });
    });
});