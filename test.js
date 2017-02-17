var page = require('webpage').create();
page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
page.viewportSize = {
  width: 1366,
  height: 768
};
page.open('https://scholar.google.com/scholar?start=20&q=oxygen&hl=en&as_sdt=0,5', function() {
    page.render('output.png');
    console.log("captured");
    var result = page.evaluate(function(){
        var resultList = document.getElementsByClassName('gs_r');
        var items = [];        
        for(var i=0; i<resultList.length; i++){
            var articleTitle = resultList[i].getElementByClassName('gs_rt');
            items[i] = 'test';
        }
        return {'items' : items, 'count' : resultList.length};
    });
    for(var i=0; i<result.count; i++)
        console.log(result.items[i]);
    phantom.exit();
});