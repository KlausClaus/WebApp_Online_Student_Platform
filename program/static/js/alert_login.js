function alert_login(){
    var url = document.location.toString();
    if(url.indexOf("?") != -1){
        var para = url.split("?")[1].split("=")[1];
        if(para == "False")
        {
            alert("Wrong username or password!\nPlease check your entry.");
            url = url.split("?")[0];
            window.location.replace(url);
        }
    }
}
alert_login()