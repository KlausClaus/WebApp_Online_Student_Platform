function alert_mute(){
    var url = document.location.toString();

    if(url.indexOf("?") != -1){
        var para = url.split("?")[1].split("=");
        if(para[0] == "mute")
        {
            url = url.split("?")[0];
            window.location.replace(url);
            if(para[1] == "True")
            {
                alert("You cannot post or comment.\nYou are muted by an administrator.");
            }
        }
    }
}
alert_mute()