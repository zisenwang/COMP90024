function (doc) {
    if (doc.text && (doc.text.indexOf('covid') != -1 || doc.text.indexOf('lockdown') != -1 ||
        doc.text.indexOf('virus') != -1 || doc.text.indexOf('corona') != -1 || doc.text.indexOf('vaccine') != -1 )){
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
