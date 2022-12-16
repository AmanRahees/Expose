$(document).ready(function(){

    $('.codbutton').click(function (e) { 
        e.preventDefault();
        var name = $("[name='name']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var address_2 = $("[name='address_2']").val();
        var state = $("[name='state']").val();
        var district = $("[name='district']").val();
        var city = $("[name='city']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if(name=="" || email=="" ||  phone=="" || address=="" || address_2=="" || state=="" || district=="" || city=="" || pincode=="" )
        {
            swal("Alert!", "Select an Address before proceeding!", "error");
            return false;
        } 
        else
        {
            data = {
                "name":name,
                "email":email,
                "phone":phone,
                "address":address,
                "address_2":address_2,
                "state":state,
                "district":district,
                "city":city,
                "pincode":pincode,
                "payment_mode":"Cash on Delivery",
                "payment_id":"-",
                csrfmiddlewaretoken: token
            }
            $.ajax({
                method: "POST",
                url: "/placeorder",
                data: data, 
                success: function(responsec) {
                    console.log(responsec.status);
                    redirect_url = '/ordersuccess'
                    window.location.href = redirect_url + '?order_number=' + responsec.tracking_no
                }
            });
        }
    });

})


$(document).ready(function(){

    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();
        var name = $("[name='name']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var address_2 = $("[name='address_2']").val();
        var state = $("[name='state']").val();
        var district = $("[name='district']").val();
        var city = $("[name='city']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        // urltest = "{% url 'placeorder' %}"
        
        if(name=="" || email=="" ||  phone=="" || address=="" || address_2=="" || state=="" || district=="" || city=="" || pincode=="" )
        {
            swal("Alert!", "Select an Address before proceeding!", "error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    // console.log(response)
                    var options = {
                        "key": "rzp_test_u2afvxYxg4Tr0j", // Enter the Key ID generated from the Dashboard
                        "amount":1*100, //response.grand_total * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Expose Mobiles & Laptops",
                        "description": "Thank you for buying from Us.",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        // "callback_url": "/orderconfirmed",
                        "handler":function(responseb){
                            console.log("first test");
                            // alert(responseb.razorpay_payment_id);
                            data = {
                                "name":name,
                                "email":email,
                                "phone":phone,
                                "address":address,
                                "address_2":address_2,
                                "state":state,
                                "district":district,
                                "city":city,
                                "pincode":pincode,
                                "payment_mode":"Paid by Razorpay",
                                "payment_id":responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            }
                            $.ajax({
                                method: "POST",
                                url: "/placeorder",
                                data: data,
                                success: function(responsec) {
                                    console.log(responsec.status);
                                    redirect_url = '/ordersuccess'
                                    window.location.href = redirect_url + '?order_number=' + responsec.tracking_no
                                }
                            });
                        },
                        "prefill": {
                            "name": name,
                            "email": email,
                            "contact": phone
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
            
        }
    });

    $('#couponbutton').click(function (e) {
        e.preventDefault;
        var coupon = $("[name ='coupon']").val();
        var token = $("[name = 'csrfmiddlewaretoken']").val()
        data = {
            "code": coupon,
            csrfmiddlewaretoken: token
        }
        $.ajax({
            method: "POST",
            url: "/checkout/",
            data: data,
            success: function (response7) {
                console.log(response7.Status);
                if (response7.Status == "Coupon Activated") {
                    window.location.reload();
                } else if (response7.Status == "Coupon changed") {
                    window.location.reload();
                } else {
                    $('#msg').empty()
                    $('#msg').html(response7.Status).fadeIn('fast').addClass('cart-styling').css('background-image', 'linear-gradient(to right, rgb(255, 0, 0), rgb(255, 255, 255)');

                    $('#msg').delay(2500).fadeOut('slow');
                }
            }
        })
    })

});
