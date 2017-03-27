/**
 * Created by skroo_000 on 2017-03-22.
 */

//populates the stock table with data from the database
function populate_stock_table(stock_data) {

    $("#stock_table").tabulator({
        columns:[
            {title:"Produkt", field:"product", sortable:true, width:150},
            {title:"Lager", field:"storage", sortable:true, width:150},
            {title:"Lagersaldo", field:"balance", sortable:true, width:150}
        ]
    });

    $("#stock_table").tabulator("setData", stock_data);
}


//populates the io_table with io shipment data from the database
function populate_io_table(io_data) {
    $("#io_table").tabulator({
        columns:[
            {title:"Datum", field:"date", sortable:true, width:150},
            {title:"Produkt", field:"product", sortable:true, width:150},
            {title:"Till/från", field:"storage", sortable:true, width:150},
            {title:"Antal", field:"amount", sortable:true, width:150}
        ]
    });

    $("#io_table").tabulator("setData", io_data);
    add_io_table(io_data[0]["storage"]);

}


//creates table for new io shipment data
function add_io_table(storage_name) {
    $("#add_io_table").tabulator({
        columns:[
            {title:"Datum", field:"date", sortable:true, editable:true, editor:"input", width:150},
            {title:"Produkt", field:"product", sortable:true, editable:true, editor:"input", width:150},
            {title:"Till/från", field:"storage", sortable:true, width:150},
            {title:"Antal", field:"amount", sortable:true, editable:true, editor:"input", width:150}
        ]
    });
    var new_io_data = [{"date":"", "product":"", "storage":storage_name, "amount":""}];
    $("#add_io_table").tabulator("setData", new_io_data);
}


//adds data from editing table to io_table
function add_io_to_table() {
    var data = $("#add_io_table").tabulator("getData");
    var json = JSON.stringify(data);
    if(data[0]['date'] == '') {
        update_stock(data);
    }
    else {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var json = JSON.parse(this.responseText);
                if (json.success) {
                    get_io_by_storage_name(data[0]["storage"])
                }
            }
        };
        sendPOSTrequest(xmlhttp, "add_io/", json)
    }
}

//updates stock_table by adding/subtracting amount provided in editing table
function update_stock(data) {
    var json = JSON.stringify(data);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            if (json.success) {
                get_stock_by_storage_name(data[0]['storage']);
            }
        }
    };
    sendPOSTrequest(xmlhttp, "update_stock/", json);
}


//retrieves the storage names and injects them in drop-down menu
function get_storages() {
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            if (json.success) {

                json.data.forEach(function(storage_name) {

                    document.getElementById("myDropdown").innerHTML +=
                    '<a id="storage_name" onclick="get_stock_by_storage_name(this.text)" href="javascript:void(0);">' + storage_name + '</a>';
                })
            }
        }
    };
    sendGETrequest(xmlhttp, "/get_storages");
}


//retrieves the stock(s) holding specified storage name
function get_stock_by_storage_name(storage_name) {
    document.getElementById("storage_area").style.display = 'block';
    document.getElementById("io_area").style.display = 'block';
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            if (json.success) {
                populate_stock_table(json.data);

                get_io_by_storage_name(storage_name);
            }

        }
    };
    sendGETrequest(xmlhttp, "/get_stock_by_storage_name/" + storage_name);
}


//retrieves the io(s) holding specified storage name
function get_io_by_storage_name(storage_name) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            if(json.success) {
                populate_io_table(json.data);
            }
        }
    };
    sendGETrequest(xmlhttp, "/get_io_by_storage_name/" + storage_name);
}


//help function for construction of GET requests to the server
function sendGETrequest(xmlhttp, route){
    xmlhttp.open("GET", route, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send();
}


//help function for construction of POST request to the server
function sendPOSTrequest(xmlhttp, route, data){
    xmlhttp.open("POST", route, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(data);
}


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}


// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
};