function (doc) {
    if (doc.text && (doc.text.indexOf('cancer') != -1 || doc.text.indexOf('air quality') != -1 ||
        doc.text.indexOf('traffic') != -1 || doc.text.indexOf('pet') != -1 )){
        if (doc.created_time){
            date = new Date(doc.created_time);
            actual = new Date(date.toLocaleString('en-US',{timeZone:'Australia/Melbourne'}));
            if (actual.getHours() % 2 == 1){
                actual.setHours(actual.getHours() - 1);
            }
            var s = (actual.getMonth() + 1) + '/' + actual.getDate() + ' ' + actual.getHours();
            emit(s,1);
        }
    }
}
