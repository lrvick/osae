queries = [':)',':(']

emoticons = [':-L', ':L', '<3', '8)', '8-)', '8-}', '8]', '8-]', '8-|', '8(', '8-(','8-[', '8-{', '-.-', 'xx', '</3>3', ':-{', ': )', ': (', ';]', ':{', '={',':-}', ':}', '=}', ':)', ';)', ':/', '=/', ';/', 'x(', 'x)', ':D', 'T_T', 'O.o', 'o.o', 'o_O', 'o.-', 'O.-', '-.o', '-.O', 'X_X', 'x_x', 'XD', 'DX',':-$', ':|', '-_-', 'D:', ':-)', '^_^', '=)', '=]', '=|', '=[', '=(', ':(',':-(', ':, (', ':\'(', ':-]', ':-[', ':]', ':[', '>.>', '<.<']

$(document).ready(function() {
    var query = queries[Math.floor(Math.random()*queries.length)]
    $.getJSON('http://search.twitter.com/search.json?q=' + query + '&lang=en&rpp=1&callback=?',function(data) {
        $.each(data.results, function() {
            text = this.text
        });
        $.each(emoticons, function() {
            text = text.replace(this,'');
        });
        $('textarea[name=sample]').val(text)
    });
})
