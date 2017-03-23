/**
 * Created by skroo_000 on 2017-03-22.
 */

function populate_stock_table(storage_name) {
    window.alert(storage_name);
    var data = get_stock_by_storage_name(storage_name);

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
                    '<a onclick="populate_stock_table(this.text)" href="javascript:void(0);">' + storage_name + '</a>';
                })

                //'<a href=' + "get_stock_by_storage_name/" +item+ '>' +item+ '</a>';
                //document.getElementById('storages').innerHTML = json.data
            }
        }
    };
    sendGETrequest(xmlhttp, "/get_storages");
}

function get_stock_by_storage_name(storage_name) {
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            if (json.success) {
                return json.data;
            }
        }
    };
    sendGETrequest(xmlhttp, "/get_stock_by_storage_name/" + storage_name);
}


function sendGETrequest(xmlhttp, route){
    xmlhttp.open("GET", route, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send();
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
}