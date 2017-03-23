/**
 * Created by skroo_000 on 2017-03-22.
 */


function getStorages() {
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            if (json.success) {

                document.getElementById('storages').innerHTML = json.data;
            }
        }
    };
    sendGETrequest(xmlhttp, "/print");
}

function sendGETrequest(xmlhttp, route){
    xmlhttp.open("GET", route, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send();
}

