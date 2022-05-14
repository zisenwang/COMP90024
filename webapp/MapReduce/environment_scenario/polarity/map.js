function (doc) {
    if (doc.text && (doc.text.indexOf('cancer') != -1 || doc.text.indexOf('air quality') != -1 ||
        doc.text.indexOf('traffic') != -1 || doc.text.indexOf('pet') != -1 ) && doc.text.indexOf('peter') == -1){
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
