function (doc) {
    if (doc.text && (doc.text.indexOf('covid') != -1 || doc.text.indexOf('lockdown') != -1 ||
        doc.text.indexOf('virus') != -1 || doc.text.indexOf('corona') != -1 || doc.text.indexOf('vaccine') != -1 )){
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
