function (doc) {
  doc.text.toLowerCase().split(/\W+/).forEach(function (word) {
    if (word.length > 1) {
      emit([word, doc.senti], 1);
    }
  });
}
