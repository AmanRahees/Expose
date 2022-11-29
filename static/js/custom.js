$(document).ready(function(){

    $(".choose-memory").hide();
    $(".product-price").hide();
    $(".choose-memory").first().addClass("selected")

    //show memory according to selected color

    $(".choose-color").on('click',function(){
        $(".choose-memory").removeClass('selected');
        $(".choose-memory").removeClass('active');
		$(".choose-color").removeClass('focused');
		$(this).addClass('focused');


        var _color=$(this).attr('data-color');

        $(".choose-memory").hide();
        $(".color"+_color).show();
        $(".color"+_color).first().addClass('active selected');

    });
    //end
    
    //show the price according to selected memory
    $(".choose-memory").on('click',function(){
        $(".choose-memory").removeClass('selected');
        $(".choose-memory").removeClass('active');
        $(this).addClass('active');
        _pid = $(this).data('ramid')
        //console.log(_pid);

        var _price=$(this).data('price');
        //console.log(_price)
        $(".product-price").text(_price);
        $(this).addClass('selected');
    });

    //show the default
    $(".choose-color").first().addClass('focused')
    var _color=$(".choose-color").first().attr('data-color');
    var _price=$(".choose-memory").first().attr('data-price');

    $(".color"+_color).show();
    $(".color"+_color).first().addClass('active');
    $(".product-price").text(_price);


    $("#addToCartBtn").on('click',function(){
        var _vm=$(this); 
        var _qty=$("#productQty").val();
        var _pId=$('.selected').data('ramid')
        var _productImage=$(".product-image").val();
        var _productTitle=$(".product-title").val();
        var _productPrice=$(".product-price").text();
        var _color=$(".choose-color").attr('color');
        var _memory=$(".choose-memory").attr('ram');
        //console.log(_pId);
        //Ajax
        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':_pId,
                'image':_productImage,
                'qty':_qty,
                'title':_productTitle,
                'price':_productPrice,
                'color':_color,
                'memory':_memory,
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
            }
        });
        //End
    });
    //Delete Cart Item
    $(document).on('click','.delete-item',function(){
        var _pId=$(this).attr('data-item');
        var _vm=$(this);
        //Ajax for delete
        $.ajax({
            url:'/delete-from-cart',
            data:{
                'id':_pId
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
                $("#cartList").html(res.data);
            }
        });
    });

    //Update Cart
    $(document).on('click','.update-item',function(){
        var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
        //Ajax for delete
        $.ajax({
            url:'/cart_update',
            data:{
				'id':_pId,
				'qty':_pQty
			},
            dataType:'json',
            beforeSend:function(){
				_vm.attr('disabled',true);
			},
            success:function(res){
                // $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
                $("#cartList").html(res.data);
            }
        });
    });

});

$(document).on('click','.update-item',function(){
    
    $.ajax({
        type: "method",
        url: "url",
        data: "data",
        dataType: "dataType",
        success: function (response) {
            
        }
    });
});