function (doc) {
    if (doc.text && (doc.text.indexOf('house') != -1 || doc.text.indexOf('housing') != -1 ||
        doc.text.indexOf('rent') != -1 || doc.text.indexOf('income') != -1 || doc.text.indexOf('incoming') != -1 )){
        doc.text.toLowerCase().split(' ').forEach(function (word) {
            if (word != '' && /[a-zA-Z]+/.test(word)){
                res = word.replace(/^[^a-zA-Z]+|[^a-zA-Z]+$/gm,'');
                emit(res,1);
            }
        });
    }
}
