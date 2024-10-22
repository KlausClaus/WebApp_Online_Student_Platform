function alert_message(){
    var url = document.location.toString();

    if(url.indexOf("?") != -1){
        var para = url.split("?")[1].split("=");
        if(para[0] == "delete")
        {
            url = url.split("?")[0];
            window.location.replace(url);
            if(para[1] == "False")
            {
                alert("You cannot delete yourself or super administrator.");
            }
        }
    }
}
alert_message()