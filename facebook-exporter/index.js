var request = require('request');
var fs = require('fs');
var moment = require('moment');
var config = {
    googleSpreadsheet: 'https://script.googleusercontent.com/a/macros/9gag.com/echo?user_content_key=5rB_V-GfLXa_VleYhJ17wJFhHzV7acDoGNlscBb4syuXE3rCLBGjRr4GTzZylfoFZxy1evj789I8hkXEF2MovbOq8QdZwM4wOJmA1Yb3SEsKFZqtv3DaNYcMrmhZHmUMi80zadyHLKAt-QELwJMLee8rPozBcotHtMyUQ50rEcTzW_eLHFbxIysVmuTfZaYEmUf1nKd3HdDN-fqX8Tw_b4mIOSv_1lOby1QSCbpxgpH5ispxt-K_YnyPKHFW471ddrx5_-y6IJwMC8qrsYZYetKv-L8akWNg7RE4Wg6mM2v8PXHli4Hd-rVpARzRnnDp&lib=M0klXLQOsKcIM4m86X8_CevqWUX6-vu4W'
  , sheetName: 'od1'
  , storageFile: 'feederTmp.json'
  , accessToken: ''
}

fs.readFile(config.storageFile, function (err, data) {
  if (err) {
    throw err;
  }
  var usedMap = JSON.parse(data);
  // JSON output of the spreadsheet result
  request(config.googleSpreadsheet, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      obj = JSON.parse(body);
      
      arr = obj[config.sheetName];
      for (i = 0; i < arr.length ; i++) {
        el = arr[i];
        var key = el.Start_Date + el.Tag;
        if (!usedMap[key]) {
          var dayOfWeek = moment(el['Start_Date']).format('ddd');
          if (dayOfWeek.indexOf('Sat') === 0) {
             dayOfWeek = '星期六';
          } else if (dayOfWeek.indexOf('Wed') === 0) {
             dayOfWeek = '星期三';
          } else {
             dayOfWeek = '';
          }
          usedMap[key] = 1;
          var scheduleTime = moment(el['Start_Date']).unix() - 86400;
          // Call facebook API
          request.post('https://graph.facebook.com/v2.1/feed'
          , {
              form: {
                'access_token': config.accessToken
              , 'message': '賣旗機構：' + el['Headline'] + '\n日期：' + el['Start_Date'].substr(0, 10) + '\n範圍：' + el['Tag'] +'\n服務：'+ el['Text'] + '\n本訊息由 http://charity.winginno.com 自動發出。'
              , 'link': el['Media_Caption']
              , 'published': false
              , 'scheduled_publish_time': scheduleTime
              }
            }
          , function(err,httpResponse,body){
              //console.log(body);
            }
          );
        }
      }

      fs.writeFile(config.storageFile, JSON.stringify(usedMap), function (err) {
        if (err) {
          throw err;
        }
      });
    }
  })
});
