/**
 * Created by skroo_000 on 2017-03-22.
 */


function getStorages() {
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            if (json.success) {
                var userdata = json.data;
                var result = '';
                for (var i = 0; i < userdata.length; i++) {
                    result += userdata[i];
                }
                document.getElementById('storages').innerHTML = result;
                //document.getElementById("storages").innerHTML = '<p type="text">' + json.data + "</p>";
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
