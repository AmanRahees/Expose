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
        if (_pstock <= 10 && _pstock > 0){
            $(".p-stock").addClass("text-danger")
            $(".p-stock").text("Only "+_pstock+" left");
        }
        else if (_pstock > 10){
            $(".p-stock").text(" ");
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
        if (_pstock <= 10 && _pstock > 0){
            $(".p-stock").addClass("text-danger")
            $(".p-stock").text("Only "+_pstock+" left");
        }
        else if (_pstock > 10){
            $(".p-stock").text(" ");
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
    if (_pstock <= 10 && _pstock > 0){
        $(".p-stock").addClass("text-danger")
        $(".p-stock").text("Only "+_pstock+" left");
    }
    else if (_pstock > 10){
        $(".p-stock").text(" ");
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
                    if (res.status != "Don't Add"){
                        swal("Success!","Added to Cart Successfully!","success").then(function () {
                            location.reload();
                            }
                        );
                    }
                    else{
                        swal("Sorry!", "Already added in Cart!", "error");
                    }
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
                    swal("Sorry!", "Already added in wishlist!", "error");
                }
                else{
                    swal("Success!","Added to wishlist!","success").then(function(){
                        location.reload();
                    })
                }
            }
        });

    });

});

$(document).ready(function(){

    $(".cartButton").on('click', function(e){
        e.preventDefault();
        var tid = $(this).data('id')
        console.log(tid)
        $(".wish-item"+tid).addClass("selected")
        var _vm=$(this);
        var _qty= 1

        $.ajax({
            url:'/add-to-cart',
                data:{
                    'id':tid,
                    'qty':_qty,
                },
                dataType:'json',
                beforeSend:function(){
                    _vm.attr('disabled',true);
                },
                success:function(res){
                    $(".cart-list").text(res.totalitems);
                    _vm.attr('disabled',false);
                    if (res.single_product == "success"){
                        console.log('add');
                        swal("Success!","Added to Cart Successfully!","success").then(function () {
                            location.reload();
                            }
                        );
                    }
                    else if (res.status == "Out of stock"){
                        swal("Sorry!", "Out of stock!", "error");
                    }
                    else if (res.status == "Don't Add"){
                        swal("Sorry!", "Already added in Cart!", "error");
                    }
                }
        });
    });

});