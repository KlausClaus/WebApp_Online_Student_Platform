function alert_login(){
    var url = document.location.toString();
    if(url.indexOf("?") != -1){
        var para = url.split("?")[1].split("=");
        if(para[1] == "False")
        {
            url = url.split("?")[0];
            window.location.replace(url);
            if(para[0] == "cate")
            {
                alert("Please select a category");
            }
            else if(para[0] == "content")
            {
                alert("Content cannot be empty");
            }
        }
    }
}
alert_login()