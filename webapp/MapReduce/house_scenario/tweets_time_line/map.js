function (doc) {
    if (doc.text && (doc.text.indexOf('house') != -1 || doc.text.indexOf('housing') != -1 ||
        doc.text.indexOf('rent') != -1 || doc.text.indexOf('income') != -1 || doc.text.indexOf('incoming') != -1 )){
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
