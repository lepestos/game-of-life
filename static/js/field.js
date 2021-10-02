$(document).ready(function () {
    var board = $('.container');
    var nextgen = $('#nextgen');
    var color;
    makeGrid(n, m);

    function makeGrid(n, m){
        board.html('');
        board.css("width", m * 30+2);
        for (var i = 0; i < n; i++) {
            for (var j = 0; j < m; j++){
                color = chooseColor(i, j);
                makeSquare(color);
            }
        }

    }

    function makeSquare(color) {
        board.append('<div class="square ' + color + '"></div>');
    }

    function chooseColor(i, j) {
        var k = i * m + j;
        if ((1 << k) & state){
            return 'black'
        }
        return 'white'
    }

    nextgen.click(function(){
        $.getJSON($SCRIPT_ROOT + '/_next_state',{state: state, n: n, m: m},
            function(data){
                state = data.state;
                makeGrid(n, m);
            })
    })

})