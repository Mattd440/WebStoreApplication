// $(document).ready(function(){
//
// var stripeForm = $(".stripe-payment-form")
// var stripeToken = stripeForm.attr('data-token')
// var stripeBtnTitle = stripeForm.attr('data-btn-title') || "Add To Cart"
// var stripeNextUrl = stripeForm.attr('data-next-url')
// var stripeTemplate =   $.templates("#stripeTemplate")
// var stripeContext = {
//     publish_key: stripeToken,
//     next_url: stripeNextUrl,
//     btnTitle: stripeBtnTitle
// }
//
// var stripeTemplateHtml = stripeTemplate.render(stripeContext)
// stripeForm.html(stripeTemplateHtml)
//
// var payment_form =$('.payment-form')
// if(payment_form.length > 1){
//     alert('Only One payment form per page')
//     payment_form.css('display', 'none')
// }
// else if(payment_form.length == 1) {
//     // Create a Stripe client.
//     var pKey = payment_form.attr('data-token')
//     var nextUrl = payment_form.attr('data-next-url')
//     var stripe = Stripe(pKey);
//
// // Create an instance of Elements.
//     var elements = stripe.elements();
//
// // Custom styling can be passed to options when creating an Element.
// // (Note that this demo uses a wider set of styles than the guide below.)
//     var style = {
//         base: {
//             color: '#32325d',
//             lineHeight: '18px',
//             fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
//             fontSmoothing: 'antialiased',
//             fontSize: '16px',
//             '::placeholder': {
//                 color: '#aab7c4'
//             }
//         },
//         invalid: {
//             color: '#fa755a',
//             iconColor: '#fa755a'
//         }
//     };
//
// // Create an instance of the card Element.
//     var card = elements.create('card', {style: style});
//
// // Add an instance of the card Element into the `card-element` <div>.
//     card.mount('#card-element');
//
// // Handle real-time validation errors from the card Element.
//     card.addEventListener('change', function (event) {
//         var displayError = document.getElementById('card-errors');
//         if (event.error) {
//             displayError.textContent = event.error.message;
//         } else {
//             displayError.textContent = '';
//         }
//     });
//
// // Handle form submission.
//     var form = document.getElementById('payment-form');
//     form.addEventListener('submit', function (event) {
//         event.preventDefault();
//
//         stripe.createToken(card).then(function (result) {
//             if (result.error) {
//                 // Inform the user if there was an error.
//                 var errorElement = document.getElementById('card-errors');
//                 errorElement.textContent = result.error.message;
//             } else {
//                 // Send the token to your server.
//                 stripeTokenHandler(result.token);
//             }
//         });
//     });
//
//
//     function redirectToNext(nextPath, timeoffset){
//          if(nextPath) {
//              setTimeout(function () {
//                  window.location.href = nextUrl
//              }, timeoffset)
//          }
//     }
//
//     function stripeTokenHandler(token) {
//         console.log(token.id)
//         var payment_endpoint = '/billing/payment-method/create/'
//         var data = {
//             'token': token.id
//         }
//         $.ajax({
//             data:data,
//             url: payment_endpoint,
//             method: 'POST',
//             success: function(data){
//                 var msg = data.message || 'Success! Your card was added.'
//                 card.clear()
//                 if(nextUrl){
//                     msg = msg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting... "
//                 }
//
//                 if($.alert){
//                     $.alert(msg)
//                 }
//                 else {
//                     alert(msg)
//                 }
//                 redirectToNext(nextUrl, 1500)
//
//             },
//             error: function(err){
//                 console.log(err)
//             }
//         })
//     }
//
// }
//   })

$(document).ready(function(){

var stripeForm = $(".stripe-payment-form")
var stripeToken = stripeForm.attr('data-token')
var stripeBtnTitle = stripeForm.attr('data-btn-title') || "Add To Cart"
var stripeNextUrl = stripeForm.attr('data-next-url')
var stripeTemplate =   $.templates("#stripeTemplate")
var stripeContext = {
    publish_key: stripeToken,
    next_url: stripeNextUrl,
    btnTitle: stripeBtnTitle
}

var stripeTemplateHtml = stripeTemplate.render(stripeContext)
stripeForm.html(stripeTemplateHtml)






// https secure site when live

var paymentForm =$('.payment-form')
if (paymentForm.length > 1){
    alert("Only one payment form is allowed per page")
    paymentForm.css('display', 'none')
}
else if (paymentForm.length == 1) {

var pKey = paymentForm.attr('data-token')
var nextUrl = paymentForm.attr('data-next-url')
var stripe = Stripe(pKey);

// Create an instance of Elements
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    lineHeight: '24px',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission
var form = $('#payment-form');
var loadBtn = form.find('.btn-load')
var loadBtnHtml = loadBtn.html()
var loadBtnClasses = loadBtn.attr('class')

form.on('submit', function(event){
    event.preventDefault();
    var $this = $(this)

    loadBtn.blur()
    var timeLoad = 1500
    var currentTimeout;
    var errHtml = "<i class='fa fa-warning'></i> An error occured"
    var loadingHtml = "<i class=' fa fa-spin fa-spinner'></i> Loading..."

    var errorBtnClass = "btn btn-danger disabled my-3"
    var loadingBtnClass = "btn btn-success disabled my-3"

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error
      var errorElement = $('#card-errors');
      errorElement.textContent = result.error.message;
      currentTimeout = statusBtnShow(loadBtn, errHtml, errorBtnClass, 1000, currentTimeout)
    } else {
      // Send the token to your server
      currentTimeout = statusBtnShow(loadBtn, loadingHtml, loadingBtnClass, 2000, currentTimeout)
      stripeTokenHandler(nextUrl, result.token);
    }
  });
});

function statusBtnShow(element, Html, Classes, timeLoad, timeout){

    if(!timeLoad){
        timeLoad = 1500
    }
    var defaultHtml = element.html()
    var defaultClass = element.attr('class')
    element.html(Html)
    element.removeClass(defaultClass)
    element.addClass(Classes)
    return setTimeout(function(){
        element.html(Html)
        element.addClass(defaultHtml)
        element.removeClass(Classes)
    }, timeLoad)
}

function redirectToNext(nextPath, timeoffset) {
    // body...
    if (nextPath){
    setTimeout(function(){
                window.location.href = nextPath
            }, timeoffset)
    }
}

function stripeTokenHandler(nextUrl, token){
    // console.log(token.id)
    var paymentMethodEndpoint = '/billing/payment-method/create/'
    var data = {
        'token': token.id
    }
    $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: "POST",
        success: function(data){
            var succesMsg = data.message || "Success! Your card was added."
            card.clear()
            if (nextUrl){
                succesMsg = succesMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
            }
            if ($.alert){
                $.alert(succesMsg)
            } else {
                alert(succesMsg)
            }

            loadBtn.html(loadBtnHtml)
            loadBtn.attr('class', loadBtnClasses)
            redirectToNext(nextUrl, 1500)

        },
        error: function(error){
            $.alert({title: "An error occured", content: "Please try adding your card again"})
            loadBtn.html(loadBtnHtml)
            loadBtn.attr('class', loadBtnClasses)
        }
    })
}
}})

