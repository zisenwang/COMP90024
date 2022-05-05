function (doc) {
    if (doc.text && (doc.text.indexOf('cancer') != -1 || doc.text.indexOf('air quality') != -1 ||
        doc.text.indexOf('traffic') != -1 || doc.text.indexOf('pet') != -1 )){
        doc.text.toLowerCase().split(' ').forEach(function (word) {
            if (word != '' && /[a-zA-Z]+/.test(word)){
                res = word.replace(/^[^a-zA-Z]+|[^a-zA-Z]+$/gm,'');
                emit(res,1);
            }
        });
    }
}
