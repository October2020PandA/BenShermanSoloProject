$(document).ready(function(){

    /*  CHECKOUT PAGE */

    //shipping selects
    var taxRate = (Math.random() * (0.08)).toFixed(2);
    var tax = (parseInt($("#preTaxTotal").attr('data-subtotal')) * taxRate).toFixed(2);
    $("#sameDayShipping").click(function(){
        var subtotal = (parseInt($("#preTaxTotal").attr('data-subtotal')) + 2.99);
        $("#sameDayShippingPrice").show();
        $("#nextDayShippingPrice").hide();
        $("#standardShippingPrice").hide();
        $("#preTaxTotal").html("$" + subtotal);
        $("#totalPrice").html("$" + (parseInt($("#preTaxTotal").attr('data-subtotal')) + (parseFloat(tax)) + 2.99));
    });
    $("#nextDayShipping").click(function(){
        var subtotal = (parseInt($("#preTaxTotal").attr('data-subtotal')) + 1.99);
        $("#sameDayShippingPrice").hide();
        $("#nextDayShippingPrice").show();
        $("#standardShippingPrice").hide();
        $("#preTaxTotal").html("$" + subtotal);
        $("#totalPrice").html("$" + (parseInt($("#preTaxTotal").attr('data-subtotal')) + (parseFloat(tax)) + 1.99));
    });
    $("#standardShipping").click(function(){
        var subtotal = (parseInt($("#preTaxTotal").attr('data-subtotal')));
        $("#sameDayShippingPrice").hide();
        $("#nextDayShippingPrice").hide();
        $("#standardShippingPrice").show();
        $("#preTaxTotal").html("$" + subtotal.toFixed(2));
        $("#totalPrice").html("$" + (parseInt($("#preTaxTotal").attr('data-subtotal')) + (parseFloat(tax))));
    });
    $("#shippingStateSelect").change(function(){
        $("#tax").html("$" + tax);
    });

    /*  RECORDS PAGE */

    //enabling filter by genre

    //left nav
    $('#left_nav_items li a').click(function(){

        var genre = $(this).attr('data-genre');
        
        if(genre === 'all'){
            $("#card_holder").children('div').show();
        }
        else{
            $('#card_holder').children('div:not([data-genre=' + genre + '])').hide();
            $('#card_holder').children('div[data-genre=' + genre + ']').show();
        }
    });
    //lower nav
    $('#lowerNavbar li a').click(function(){

        var genre = $(this).attr('data-genre');

        if(genre === 'all'){
            $("#card_holder").children('div').show();
        }
        else{
            $('#card_holder').children('div:not([data-genre=' + genre + '])').hide();
            $('#card_holder').children('div[data-genre=' + genre + ']').show();
        }
    });
    return false;
});