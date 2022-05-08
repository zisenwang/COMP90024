function (doc) {
    if (doc.label && doc.suburb){
        emit(doc.suburb + ';' + doc.label, 1);
    }
}
