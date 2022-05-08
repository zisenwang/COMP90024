function (doc) {
    if (doc.suburb){
        emit(doc.suburb, 1);
    }
}
