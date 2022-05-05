function (doc) {
    if (doc.text && (doc.text.indexOf('cancer') != -1 || doc.text.indexOf('air quality') != -1 ||
        doc.text.indexOf('traffic') != -1 || doc.text.indexOf('pet') != -1 )){
        if (doc.label){
            emit(doc.label,1);
        }
    }
}
