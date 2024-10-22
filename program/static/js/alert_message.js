function alert_message(){
        var url = document.location.toString();
        if(url.indexOf("?") != -1){
            var para = url.split("?")[1].split("=")[1];
            if(para == "True")
            {
                alert("Add user successfully!");
            }
            else
            {
                alert("Add failed.\nPlease check twice");
            }
            url = url.split("?")[0];
            window.location.replace(url);
        }
}
alert_message()