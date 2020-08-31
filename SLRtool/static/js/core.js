function start() {
    $.ajax({
        type: "GET",
        url: "/start",
        success: function(){
            getArticle("/next");},
        failure: function(errMsg) {
            console.log("start error")
        }
    });  
}


function getArticle(endpoint, eid=null) {
        if(endpoint=="/history") {
            console.log("endpoint" + endpoint)
            $.ajax({
                type: "POST",
                url: endpoint,
                data: JSON.stringify({'requested_eid': eid}),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data){
                    loadedData = data;
                    loadArticle(data)},
                failure: function(errMsg) {
                    console.log("get error")
                }
            });  
        } else {
            $.ajax({
                type: "GET",
                url: endpoint,
                success: function(data){
                    loadedData = data;
                    loadArticle(data)},
                failure: function(errMsg) {
                    console.log("get error")
                }
            });  
        }
}

function loadArticle(data){
    $("#articleURL").attr("href", data.paperurl);
    $("#title").text(data.title);
    $("#abstract").text(data.abstract);
    $("#keywords").text(data.keywords);

    // check if the article was already accessed (e.g. because back previous article button was triggered)
    // and change background color accordingly to indicate existing accessment to user
    //console.log(typeof  data.decision)
    console.log("data decision:" + data.decision);
    switch (data.decision) {
        case '1':
            console.log('the decision is already set to 1')
            $("div.content").css("background-color", "#00cc44");
            //also display current status
            $("#articleStatusDisplay").text("included")
            break;

        case '0':
            $("div.content").css("background-color", "#ffcc00");
            //also display current status
            $("#articleStatusDisplay").text("unsure")
            break;
        
        case '-1':
            $("div.content").css("background-color", "#ff5050");
            //also display current status
            $("#articleStatusDisplay").text("excluded")
            break;

        case null:
            $("div.content").css("background-color", "white");
            //also display current status
            $("#articleStatusDisplay").text("not yet rated")
            break;
    }
}

function decision(decision) {
    $.ajax({
        type: "POST",
        url: "/decision",
        // the key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify({'decision': decision}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(){
            getArticle('/next');
            // append article to article-overview table in the right-box
            // 1. get number of rows inside of table for incrementor
            var numItems = $('td').length;
            // set table class (color setting) based on decision
            var tableClass;
            switch (decision) {
                case '1':
                    tableClass = "table-success"
                    break;
        
                case '0':
                    tableClass = "table-warning"
                    break;
                
                case '-1':
                    tableClass = "table-danger"
                    break;
            }
           
            $("#table-body").prepend(
                `<tr class=${tableClass}>
                        <th scope="row"><a class="" href="#" onclick="getArticle('/history', '${loadedData.eid}')">${numItems + 1}</a></th>
                        <td maxlength="20"><a href="#" onclick="getArticle('/history', '${loadedData.eid}')">${loadedData.title}</a></td>
                </tr>`);
            },
        failure: function() {
            console.log("decision post error");
        }
    });
}

function setReviewerName() {
    currentReviewer = $("#reviewerUserInput").val();
    console.log("Reviewer: " + currentReviewer)
    $("#reviewer").text(currentReviewer);
    $.ajax({
        type: "POST",
        url: "/reviewer",
        data: JSON.stringify(currentReviewer),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){},
        failure: function(errMsg) {
            console.log("get error")
        }
    });  


}


