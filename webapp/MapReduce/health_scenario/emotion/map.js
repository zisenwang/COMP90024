function (doc) {
    if (doc.text && (doc.text.indexOf('covid') != -1 || doc.text.indexOf('lockdown') != -1 ||
        doc.text.indexOf('virus') != -1 || doc.text.indexOf('corona') != -1 || doc.text.indexOf('vaccine') != -1 )){
        if (doc.label){
            emit(doc.label,1);
        }
    }
}
