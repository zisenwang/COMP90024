function (doc) {
    if (doc.text && (doc.text.indexOf('cancer') != -1 || doc.text.indexOf('air quality') != -1 ||
        doc.text.indexOf('traffic') != -1 || doc.text.indexOf('pet') != -1 )){
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
