function (doc) {
    if (doc.suburb && (doc.text.indexOf('disabled') != -1 || doc.text.indexOf('welfare') != -1
        || doc.text.indexOf('hospital') != -1|| doc.text.indexOf('aid') != -1|| doc.text.indexOf('assistance') != -1||
        doc.text.indexOf('charity') != -1 )){
        emit(doc.suburb, 1);
    }
}
