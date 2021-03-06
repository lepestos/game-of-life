$(document).ready(function () {
    var board = $('#board');
    var iboard = $('#iboard');
    var nextgen = $('#nextgen');
    var new_state = $('#new_state')
    var dims = $('#dims')
    var play = $('#play')
    var stop = $('#stop')
    var slowdown = $('#slowdown')
    var speedup = $('#speedup')
    var color;
    var updateInterval = 1000;

    makeGrid(n, m, state);
    makeInteractiveGrid(n, m, state);

    function makeGrid(n, m, state){
        board.html('');
        board.css("width", m * 30+2);
        for (var i = 0; i < n; i++) {
            for (var j = 0; j < m; j++){
                color = chooseColor(i, j, state);
                makeSquare(board, color);
            }
        }
    }

    function makeInteractiveGrid(n, m){
        iboard.html('');
        iboard.css("width", m * 30+2);
        for (var i = 0; i < n; i++) {
            for (var j = 0; j < m; j++){
                color = chooseColor(i, j, state);
                makeSquare(iboard, color, i*m + j);
                $("#sq" + (i*m + j)).click(function(event){
                    $('#' + (event.target.id)).toggleClass('white black');
                });
            }
        }
    }

    function makeSquare(element, color, id=null) {
        if (id === null) {
            element.append('<div class="square ' + color + '"></div>');
        }
        else {
            element.append('<div class="square ' + color + '" id="sq' + id +'"></div>');
        }
    }

    function chooseColor(i, j, state) {
        var k = i * m + j;
        if (1n << BigInt(k) & state){
            return 'black'
        }
        return 'white'
    }

    function nextGen(){
        $.getJSON($SCRIPT_ROOT + '/_next_state',{state: state, n: n, m: m, nxt: 1},
            function(data){
                var next_state = BigInt(data.state);
                makeGrid(n, m, next_state);
                state = next_state;
            })
    }

    nextgen.click(nextGen);

    new_state.click(function(){
        var new_state = 0n;
        var i = 0n;
        var val;
        iboard.children().each(function(){
            val = ($(this).attr("class").split(/\s+/)[1]==='black') ? 1n : 0n;
            new_state += (val << i);
            i += 1n;
        })
        $.getJSON($SCRIPT_ROOT + '/_next_state',{state: new_state, n: n, m: m, nxt: 0},
            function(data){
                new_state = BigInt(data.state);
                state = new_state;
                makeGrid(n, m, new_state);
        })
    });

    dims.click(function(){
        n = $('#n').val();
        m = $('#m').val();
        state = 0n;
        makeInteractiveGrid(n, m);
        makeGrid(n, m, state)
    });

    play.click(function(){
        var intervalId = setInterval(nextGen, updateInterval);
        play.css("display", "none");
        stop.css("display","inline-block");
        slowdown.css("display","inline-block");
        speedup.css("display","inline-block");

        stop.click(function(){
            clearInterval(intervalId);
            stop.css("display", "none");
            slowdown.css("display", "none");
            speedup.css("display", "none");
            play.css("display","inline-block");
        });

        slowdown.click(function () {
            if (updateInterval < 10000) {
                updateInterval *= 2;
                clearInterval(intervalId);
                intervalId = setInterval(nextGen, updateInterval);
            }
        });

        speedup.click(function () {
            if (updateInterval > 600) {
                updateInterval /= 2;
                clearInterval(intervalId);
                intervalId = setInterval(nextGen, updateInterval);
            }
        })
    });



})