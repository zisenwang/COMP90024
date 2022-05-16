function (doc) {
    if (doc.text && (doc.text.indexOf('covid') != -1 || doc.text.indexOf('lockdown') != -1 ||
        doc.text.indexOf('virus') != -1 || doc.text.indexOf('corona') != -1 || doc.text.indexOf('vaccine') != -1 )){
        doc.text.toLowerCase().split(' ').forEach(function (word) {
            if (word != '' && /[a-zA-Z]+/.test(word)){
                res = word.replace(/^[^a-zA-Z]+|[^a-zA-Z]+$/gm,'');
                emit(res,1);
            }
        });
    }
}
