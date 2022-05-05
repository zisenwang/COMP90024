function (doc) {
    if (doc.text && (doc.text.indexOf('house') != -1 || doc.text.indexOf('housing') != -1 ||
        doc.text.indexOf('rent') != -1 || doc.text.indexOf('income') != -1 || doc.text.indexOf('incoming') != -1 )){
        if (doc.senti){
            var polarity = '';
            if (doc.senti.polarity > 0){
                polarity = 'positive';
            }
            if (doc.senti.polarity == 0){
                polarity = 'neutral';
            }
            if (doc.senti.polarity < 0){
                polarity = 'negative';
            }
            var sub = '';
            if (doc.senti.subjectivity >= 0.5){
                sub = 'subjective';
            }
            if (doc.senti.subjectivity < 0.5){
                sub = 'objective';
            }
            emit(polarity + ' ' + sub, 1);
        }
    }
}
