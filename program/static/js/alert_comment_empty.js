function alert_comment(){
    var url = document.location.toString();

    if(url.indexOf("?") != -1){
        var para = url.split("?")[1].split("&")[1].split("=");
        if(para[0] == "comment")
        {
            url = url.split("&")[0];
            window.location.replace(url);
            if(para[1] == "False")
            {
                alert("Comment cannot be empty.");
            }
        }
    }
}
alert_comment()
