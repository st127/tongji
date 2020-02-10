var xmlhttp = false;
function createRequest(url) {
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
        if(xmlhttp.overrideMimeType){
            xmlhttp.overrideMimeType("text/xml");
        }
    } else if(window.ActiveXObject) {
        try{
            xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
        }catch (e) {
            try {
                xmlhttp = new ActiveXObject("Microsoft.XMLHTTP")
            }catch (e) {}
        }
    }
    if(!xmlhttp){
        alert("不能创建xmlhttp实例，请不要使用兼容模式或更换浏览器！")
        return false;
    }
    xmlhttp.onreadystatechange = alertContents;
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
}
function alertContents() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        document.getElementById("shuoming_by_ajax").innerHTML = xmlhttp.responseText;
    }
}
function query_by_statistics(str) {
    if(str=="0"){
        window.alert("请在 选择项目 中选择您要进行提交的项目");
        return false;
    }
    else{
        createRequest("{% url 'xxtj:ajax' %}?statistics=" + str + "&do=query_description_by_statistics");
    }
}
function validateForm()
{
    var sta=document.forms["main"]["statistics"].value;
    var name=document.forms["main"]["name"].value;
    if (sta=="0"){
        alert("项目必须选择");
        return false;
    }
    if (name=="0"){
        alert("姓名必须选择");
        return false;
    }
}