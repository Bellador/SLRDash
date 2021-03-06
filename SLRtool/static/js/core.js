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
                    // set global loadedData
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

    // check the previous decision on the paper given the current reviewer
    let decision;
    console.log("reviewer: " + currentReviewerId);
    switch (currentReviewerId) {
        case '1':
            decision = data.decision_r_1
            $("#reviewerRemark").val(data.remark_r_1);
            break;
        case '2':
            decision = data.decision_r_2
            $("#reviewerRemark").val(data.remark_r_2);
            break;
        case '3':
            decision = data.decision_r_3
            $("#reviewerRemark").val(data.remark_r_3);
            break;
    }
    console.log("data decision: " + decision);
    switch (decision) {
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

        case 'not reviewed':
            $("div.content").css("background-color", "white");
            //also display current status
            $("#articleStatusDisplay").text("not yet rated")
            break;
    }
}

function decision(decision) {
    let remark = $("#reviewerRemark").val();
    // clear remark text field for next article
    $("#reviewerRemark").val("");
    $.ajax({
        type: "POST",
        url: "/decision",
        // the key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify({
                    "decision": decision,
                    "remark": remark    
                }),
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

function setSettings() {
    psw = $("#inputPassword").val()
    console.log("psw: " + inputPassword)
    currentReviewerId = $("#selectReviewer").val();
    currentReviewerName = $(`#selectReviewer option[value="${currentReviewerId}"]`).text();
    // set text in html visible to user
    $("#reviewer").text(currentReviewerName);
    //console.log("Current reviewer " + currentReviewer)
    // get article filter settings for session
    let articleFilterList = [];
    $(".custom-control-input").each(function() {
        let articleFilter = $(this).attr('id')
        // chech if checkbox is checked lol
        if($(this).prop('checked')){
            articleFilterList.push(articleFilter);
        }
    });
    var payload = {
                    "password": psw,
                    "reviewer": currentReviewerId,
                    "article_filter_list": articleFilterList}
    $.ajax({
        type: "POST",
        url: "/settings",
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){start()},
        failure: function(errMsg) {
            console.log("get error")
        }
    });  
}


