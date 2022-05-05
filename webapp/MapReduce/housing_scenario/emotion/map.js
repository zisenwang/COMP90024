function (doc) {
    if (doc.text && (doc.text.indexOf('house') != -1 || doc.text.indexOf('housing') != -1 ||
        doc.text.indexOf('rent') != -1 || doc.text.indexOf('income') != -1 || doc.text.indexOf('incoming') != -1 )){
        if (doc.label){
            emit(doc.label,1);
        }
    }
}
