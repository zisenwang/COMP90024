function (doc) {
    if (doc.text && (doc.text.indexOf('house') != -1 || doc.text.indexOf('housing') != -1 ||
        doc.text.indexOf('rent') != -1 || doc.text.indexOf('income') != -1 || doc.text.indexOf('incoming') != -1 )){
        if (doc.senti){
            var polarity = '';
            if (doc.senti.polarity > 0){
                polarity = 'Positive';
            }
            if (doc.senti.polarity == 0){
                polarity = 'Neutral';
            }
            if (doc.senti.polarity < 0){
                polarity = 'Negative';
            }
            var sub = '';
            if (doc.senti.subjectivity >= 0.5){
                sub = 'Subjective';
            }
            if (doc.senti.subjectivity < 0.5){
                sub = 'Objective';
            }
            emit(polarity + ' ' + sub, 1);
        }
    }
}
