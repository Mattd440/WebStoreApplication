
   $(document).ready(()=> {

       //Contact Form Handler
       var contactForm = $('.contact-form')
       var  formMethod = contactForm.attr('method')
       var formEndpoint = contactForm.attr('action')


       function displaySubmitting(submitBtn,defaultTxt, doSubmit){
           if (doSubmit) {
               submitBtn.addClass('disabled')
               submitBtn.html('<i class="fa fa-spin fa-spinner"></i>Sending...')
           }else{
               submitBtn.removeClass('disabled')
               submitBtn.html(defaultTxt)
           }

       }

       contactForm.submit(function(event){
           event.preventDefault();

            var formSubmitBtn = searchForm.find('[type="submit"]')
            var formSubmitBtnTxt = formSubmitBtn.text()

           var formData = contactForm.serialize()
           var thisForm = $(this)
           displaySubmitting(formSubmitBtn, "", true)

           $.ajax({
               method:formMethod,
               url: formEndpoint,
               data:formData,
               success: function(data){
                contactForm[0].reset()
                   $.alert({
                       title:'Success!',
                       content:data.message,
                       theme: 'modern'
                   })
                   setTimeout(function(){
                       displaySubmitting(formSubmitBtn, "", false)
                   }, 500)
               },
               error: function(err){
                   var jsonData = error.responseJSON
                   var msg = '' ;
                   $.each(jsonData, function(key,value){
                       msg += key + ': ' + value[0].message + '<br/>'
                   });

                   $.alert({
                       title:'Oops!',
                       content: "An Error Occured",
                        theme:'modern'
                   })

                   setTimeout(function(){
                       displaySubmitting(formSubmitBtn, formSubmitBtnTxt, false)
                   }, 500)
               }
           })

       });



       // Search Form Handler
       var searchForm = $('.search-form')
       var searchInput = searchForm.find("[name='q']")
       var timer ;
       var typeInterval = 500;
       var searchBtn = searchForm.find('[type="submit"]')
       searchInput.keydown(function(event){
            clearTimeout(timer)
       })

       searchInput.keyup(function(event){
           clearTimeout(timer)
           timer = setTimeout(doSearch, typeInterval)
       })
       function setBtnHTML(){
           searchBtn.addClass('disabled')
           searchBtn.html('<i class="fa fa-spin fa-spinner"></i> Searching...')
       }
       function doSearch(){
           setBtnHTML()
           var query = searchInput.val()
           console.log(query)
           setTimeout(function(){
               windown.location.href='/search/?q='+query
           }, 1000)

       }


       // Cart Handler
       var productAddForm = $(".product-add-form")
       productAddForm.submit(function (event) {
           event.preventDefault()
           let form = $(this)
           let endPoint = form.attr("data-endpoint")
           let method = form.attr("method")
           let formData = form.serialize()

           $.ajax({
               url: endPoint,
               method:method,
               data:formData,

               success: function(data){
                   console.log('success')
                   console.log(data)
                   var submitSpan = form.find('.submit-span')
                   if (data.added){
                       submitSpan.html("In Cart <button type='submit' class=\"btn btn-danger\">Remove?</button>")
                   }else{
                       submitSpan.html("<button type='submit' class=\"btn btn-success\">Add To Cart</button>")
                   }
                   var count = $('.navbar-cart-count')
                   count.text(data.count)

                   var path = window.location.href

                   if(path.indexOf('cart') != -1){
                       updateCart()
                   }
               },
               error:function(err){
                   $.alert({
                       title:'Oops!',
                       content:"An Error Occurred",
                       theme:'modern'
                   })
                   console.log("error")
                   console.log(err)
               }
           })

       })

       function updateCart(){
            var cartTable =$(".cart-table")
            var cartBody = cartTable.find(".cart-body")
            var productRow = cartBody.find('.cart-products')
            var currentLocation = window.location.href

            $.ajax({
                url:'/api/cart/',
                method: 'GET',
                data: {},
                success: function(data){
                    console.log(data)
                    var hiddenRemoveForm = $(".cartitem-remove-form")
                    if (data.products.length > 0){
                        productRow.html('')
                        i =data.products.length
                        $.each(data.products, function(index, value){
                            var newCartItemRemove =hiddenRemoveForm.clone()
                            newCartItemRemove.css('display', 'block')
                            newCartItemRemove.find('.cart-item-product-id').val(value.id)
                            cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" +value.url + "'>"+ value.name +
                            "</a>"+ newCartItemRemove.html()+"</td><td>" + value.price + "</td></tr>")
                            i--
                        })

                        cartBody.find('.cart-subtotal').text(data.subtotal)
                        cartBody.find('.cart-total').text(data.total)
                    }
                    else{
                        $.alert({
                       title:'Oops!',
                       content:"An Error Occurred",
                       theme:'modern'
                   })
                        window.location.href = currentLocation
                    }
                },
                error: function(err){

                }

            })

       }



   })
