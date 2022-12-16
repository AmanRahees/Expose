$(document).ready(function(){

    $(".choose-memory").hide();
    $(".product-price").hide();
    $(".off-per").hide();
    $(".p-off").hide();
    $(".p-stock").hide();
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

        var _price=$(".color"+_color).first().data('price');
        $(".product-price").text("₹"+_price)

        x = "₹" + Math.round(_price - _price * _poff / 100)
        $(".p-off").text(x)
        
        var _pstock = $(".color"+_color).first().data('stock')
        if (_pstock > 0){
            $(".p-stock").removeClass("text-danger")
            $(".p-stock").addClass("text-success")
            $(".p-stock").text(_pstock+" left");
        }
        else{
            $(".p-stock").addClass("text-danger")
            $(".p-stock").text("Out of Stock");
        }

    });
    //end
    
    //show the price according to selected memory
    $(".choose-memory").on('click',function(){
        $(".choose-memory").removeClass('selected');
        $(".choose-memory").removeClass('active');
        $(this).addClass('active');
        _pid = $(this).data('ramid')
        _poff = $(this).data('off')
        

        var _price=$(this).data('price');
        var _peroff=$(this).data('off');
        var _pstock = $(this).data('stock')

        $(".product-price").text("₹"+_price);
        $(".off-per").text(_peroff+"% off");
        if (_pstock > 0){
            $(".p-stock").removeClass("text-danger")
            $(".p-stock").addClass("text-success")
            $(".p-stock").text(_pstock+" left");
        }
        else{
            $(".p-stock").addClass("text-danger")
            $(".p-stock").text("Out of Stock");
        }
        $(this).addClass('selected');

         x = "₹" + Math.round(_price - _price * _poff / 100)
         $(".p-off").text(x);
    });

    //show the default
    $(".choose-color").first().addClass('focused')
    var _color=$(".choose-color").first().attr('data-color');
    var _price=$(".choose-memory").first().attr('data-price');
    var _poff=$(".choose-memory").first().attr('data-off');
    var _peroff=$(".choose-memory").first().attr('data-off');
    var _pstock=$(".choose-memory").first().attr('data-stock');

    $(".color"+_color).show();
    $(".color"+_color).first().addClass('active');
    $(".product-price").text("₹"+_price);
    $(".off-per").text(_peroff+"% off");
    if (_pstock > 0){
        $(".p-stock").addClass("text-success")
        $(".p-stock").text(_pstock+" left");
    }
    else{
        $(".p-stock").addClass("text-danger")
        $(".p-stock").text("Out of Stock");
    }
    x = "₹" + Math.round(_price - _price * _poff / 100)
    $(".p-off").text(x);


    $("#addToCartBtn").on('click',function(){
        var _vm=$(this);
        var _qty=$("#productQty").val();
        var _pId=$('.selected').data('ramid')
        var _productImage=$(".product-image").val();
        var _productTitle=$(".product-title").val();
        var _productPrice=$(".p-off").text();
        var _color=$(".choose-color").attr('color');
        var _memory=$(".choose-memory").attr('ram');
        var _gtstock=$(".p-stock").text();

        if (_gtstock == "Out of Stock"){
            swal("Sorry!", "Out of stock!", "error");
            return false;
        }
        else{
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
                    swal("Success!","Added to Cart Successfully!","success").then(function () {
                        return true;
                        }
                    );
                }
            });
        //End
        }
        
    });

    $('#addtoWishlist').click(function (e) { 
        e.preventDefault();
        var _pId=$('.selected').data('ramid')

        $.ajax({
            url:'/add-to-wishlist',
            data: {
                'id':_pId,
            },
            success: function (response) {
                if(response.status == 'Not'){
                    swal("Sorry!", "Product Already in wishlist!", "error");
                }
                else{
                    swal("Success!","Added to wishlist!","success")
                }
            }
        });

    });

});

$(document).ready(function(){

    $('#AddfwtoC').click(function (e) { 
        e.preventDefault();
        $(".wish-item").addClass("selected")
        var _vm=$(this);
        var _wId =$('.selected').data('id')
        var _qty= 1
        console.log(_wId);

        $.ajax({
            url:'/add-to-cart',
                data:{
                    'id':_wId,
                    'qty':_qty,
                },
                dataType:'json',
                beforeSend:function(){
                    _vm.attr('disabled',true);
                },
                success:function(res){
                    $(".cart-list").text(res.totalitems);
                    _vm.attr('disabled',false);
                    swal("Success!","Added to Cart Successfully!","success").then(function () {
                        return true;
                        }
                    );
                }
        });
        
    });

});