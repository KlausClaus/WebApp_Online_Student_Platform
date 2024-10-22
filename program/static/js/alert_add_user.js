function alert_message(){
        var url = document.location.toString();

        if(url.indexOf("?") != -1){
            var para = url.split("?")[1].split("=");
            if(para[0] == "add")
            {
                url = url.split("?")[0];
                window.location.replace(url);
                if(para[1] == "True")
                {
                    alert("Add user successfully!");
                }
                else if(para[1] == "False")
                {
                    alert("Add failed.\nPlease check twice");
                }
            }
        }
}
alert_message()