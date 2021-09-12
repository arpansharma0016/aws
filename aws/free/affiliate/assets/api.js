user = document.currentScript.getAttribute('user')
product = document.currentScript.getAttribute('product')
url = `http://127.0.0.1:8000/api-${user}-${product}/`
$.get(url, function(data, status){
    if (data.status == 'No Such Product'){
        document.getElementById(`${user}-${product}`).innerHTML = 
        `<h1>There's no such product!</h1>`
    } else if (data.status == 'success') {
        document.getElementById(`${user}-${product}`).innerHTML = `
        <div class="col-md-4 ftco-animate">
            <div class="blog-entry" style="text-align: center"><br>
                ${data.product_image}
                <div class="text p-4 d-block">
                <div class="meta mb-3">
                    <a href="${data.product_text_link}" target="_blank" style="color:black"><strong>${data.product_name.substring(0, 100)}</strong></a>
                    
                </div>
                <h4><a href="{{product.product_text_link}}" target="_blank" style="color:black">${data.currency} ${numberWithCommas(data.product_price)}</a></h4>
                <a href="http://127.0.0.1:8000/${data.username}/${data.username}-${data.id}/${convertToSlug(data.product_name)}"><button type="button" class="btn btn-primary">
                        View Description
                </button></a>
                </div>
            </div>
        </div>
        `
    }
})

function convertToSlug(Text)
{
    return Text
        .toLowerCase()
        .replace(/[^\w ]+/g,'')
        .replace(/ +/g,'-')
        ;
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

{/* <div class="col-md-4 ftco-animate">
    <div class="blog-entry" style="text-align: center"><br>
        {{ product.product_image |safe}}
        <div class="text p-4 d-block">
        <div class="meta mb-3">
            <a href="{{product.product_text_link}}" target="_blank" style="color:black"><strong>{{product.product_name|truncatechars:100}}</strong></a>
            
        </div>
        <h4><a href="{{product.product_text_link}}" target="_blank" style="color:black">{{user_info.currency}} {{product.product_price|intcomma}}</a></h4>
        <a href="{{product.username}}-{{product.id}}/{{product.product_name|slugify}}"><button type="button" class="btn btn-primary" data-toggle="modal">
                View Description
        </button></a>
        </div>
    </div>
</div> */}