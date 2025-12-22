var red=0;
var green=0;
var blue=0;
var colorname="";

function printMessage(msg){
    $("#message").html(msg).show(1000).hide(1000);
}

function colorChangeEventHandler(event){
    loadColor();
    event.preventDefault();
    return false;
}

function colorEditEventHandler(event){
    editColor();
    event.preventDefault();
    return false;
}

$(document).ready(function(){
    colorname="black";
    loadColor()
    $("#colorname").keydown((event)=>{if(event.keyCode == 13){colorChangeEventHandler(event)}});
    $("#colorname").on("change", (event) => {colorChangeEventHandler(event)})
    $("#red").on("change", (event) => {colorEditEventHandler(event)})
    $("#green").on("change", (event) => {colorEditEventHandler(event)})
    $("#blue").on("change", (event) => {colorEditEventHandler(event)})
    printMessage("page loaded")
});

function updatePage(){
    //console.log("updatePage: ("+red+", "+green+", "+blue+")")
    $("#colorbox").css("background-color", "rgb("+red+","+green+", "+blue+")")
    $("#colordescription").html(colorname + ": #"+red.toString(16).padStart(2, '0')+green.toString(16).padStart(2, '0')+blue.toString(16).padStart(2, '0'))
    $("#colorname").val(colorname)
    $("#red").val(red)
    $("#green").val(green)
    $("#blue").val(blue)
}

function loadColor(){
    if ($("#colorname").val()!="") {
        colorname=$("#colorname").val();
    }
    $.ajax({
        method: "GET",
        url: "/api/v1/colors/"+colorname,
        statusCode: {
            200: (data)=>{
                red=parseInt(data["red"]);
                green=parseInt(data["green"]);
                blue=parseInt(data["blue"]);
                updatePage();    
            },
            404: ()=>{console.log("creating color"); createColor();}
        }
    });
}

function editColor(){
    red=parseInt($("#red").val());
    green=parseInt($("#green").val());
    blue=parseInt($("#blue").val());
    console.log("editColor: ("+red+", "+green+", "+blue+")");
    updatePage();
    $.ajax({
        method: "PUT",
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        url: "/api/v1/colors/"+colorname,
        data: JSON.stringify({"red": red, "green": green, "blue": blue})
    }).done(()=>{printMessage("color updated")});
}

function createColor(){
    colorname=$("#colorname").val();
    console.log("createColor: ("+colorname+")");
    updatePage();
    $.ajax({
        method: "POST",
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        url: "/api/v1/colors/"+colorname,
        data: JSON.stringify({"red": red, "green": green, "blue": blue})
    }).done(()=>{printMessage("colorCreated")});
}
