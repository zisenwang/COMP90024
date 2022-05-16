"""
define search_content in create_dynamic_view of CouchDbHandler
type: customized ———— define customized content in the following argument
      word_cloud ———— search the result in the form of word cloud (word - amount)
      emotion    ———— search the result of positive and negative emotion (positive - amount, negative - amount)
      default    ———— search the amount of tweets (null - amount)
"""


def search_content(type, content=None):
    if type == 'customized':
        return content
    if type == 'word_cloud':
        return "{ doc.text.toLowerCase().split(' ').forEach(function (word) { if (word != '' && /[" \
                      "a-zA-Z]+/.test(word)){ res = word.replace(/^[^a-zA-Z]+|[^a-zA-Z]+$/gm,''); emit(res,1);}}); } "
    if type == 'default':
        return "emit(null,1);"
    if type == 'emotion':
        return "{ if (doc.label) emit(doc.label,1); } "
    if type == 'line':
        return '''{
        if (doc.created_time){
            date = new Date(doc.created_time);
            actual = new Date(date.toLocaleString('en-US',{timeZone:'Australia/Melbourne'}));
            if (actual.getHours() % 2 == 1){
                actual.setHours(actual.getHours() - 1);
            }
            var s = (actual.getMonth() + 1) + '/' + actual.getDate() + ' ' + actual.getHours();
            emit(s,1);
        }
    }'''