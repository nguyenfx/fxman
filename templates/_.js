var symbols = ["BTCUSD", "ETHUSD", "XAUUSD",
                "EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDCHF", "USDJPY", "USDCAD",
				"EURJPY", "GBPJPY", "AUDJPY", "NZDJPY", "CHFJPY", "CADJPY",
				"EURGBP", "EURAUD", "EURNZD", "EURCHF", "EURCAD",
				"GBPAUD", "GBPNZD", "GBPCHF", "GBPCAD",
                "AUDNZD", "AUDCHF", "AUDCAD",
                "NZDCHF", "NZDCAD",
                "CADCHF"];

function load_sentiments() {
		var sen_image = document.getElementById("sen_image");
        sen_image.src = "sentiments.png?" + timestamp();
        var tbody = document.getElementById("sentiments").getElementsByTagName('tbody')[0];
        while (tbody.firstChild) {
            tbody.firstChild.remove();
        }
        for (i = symbols.length - 1; i >= 0 ; i--) {
             var row = tbody.insertRow(0);
             var row1 = tbody.insertRow(1);
             var cell = row1.insertCell(0);
             cell.innerHTML = '<img src="sen' + symbols[i] + '.png?' + timestamp() + '">';
        }
}

function load_signals() {
    var xhr  = new XMLHttpRequest()
    xhr.open('GET', "signals.json?" + timestamp(), true)
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == "200") {
            var data = JSON.parse(xhr.responseText);
            var tbody = document.getElementById("signals").getElementsByTagName('tbody')[0];
            while (tbody.firstChild) {
                tbody.firstChild.remove();
            }
            for (i = 2; i >= 0 ; i--) {
	            var row = tbody.insertRow(0);
	            row.classList.add('active-row');
	            var cell1 = row.insertCell(0);
	            cell1.innerHTML = data[i][1];
	            var cell2 = row.insertCell(1);
	            if(data[i][2] > 0) {
	                cell2.classList.add('positive');
	                cell2.innerHTML = "Buy";
	            } else {
	                cell2.classList.add('negative');
	                cell2.innerHTML = "Sell";
	            }
	            var cell3 = row.insertCell(2);
	            var now = Math.floor((new Date()).getTime() / 1000);
	            var time = Math.floor(Date.parse(data[i][6] + " GMT") / 1000)
	            var diff = Math.floor((now - time) / 60 / 60);
	            cell3.innerHTML = data[i][6] + " GMT<br>" + diff + " hours ago";
	            var cell4 = row.insertCell(3);
	            cell4.innerHTML = data[i][4] + "<br>" + data[i][5];
	            var change = data[i][5] - data[i][4];
	            var changep = (data[i][5] - data[i][4]) / data[i][4] * 100;
	            var max_up = data[i][8] - data[i][4];
                var max_down = data[i][9] - data[i][4];
                var cell5 = row.insertCell(4);
                cell5.innerHTML = changep.toFixed(2) + "%<br>" + topips(data[i][1], data[i][2], change) + " pips";
                var cell6 = row.insertCell(5);
                if(data[i][2] > 0){
                    if(change >= 0){
	                    cell5.classList.add('positive');
	                } else {
	                    cell5.classList.add('negative');
	                }
	                cell6.innerHTML = topips(data[i][1], data[i][2], max_up) + " pips<br>" + topips(data[i][1], data[i][2], max_down) + " pips";
                } else {
                    if(change <= 0){
	                    cell5.classList.add('positive');
	                } else {
	                    cell5.classList.add('negative');
	                }
	                cell6.innerHTML = topips(data[i][1], data[i][2], max_down * -1) + " pips<br>" + topips(data[i][1], data[i][2], max_up * -1) + " pips";
                }
	            var row1 = tbody.insertRow(1);
	            row1.innerHTML = '<td colspan="6"><div id="tradingview_' + data[i][1] + '"></div></td>'
	            tradingview(data[i][1]);
	        }
            var tbody1 = document.getElementById("signals1").getElementsByTagName('tbody')[0];
            var tbody2 = document.getElementById("signals2").getElementsByTagName('tbody')[0];
            while (tbody1.firstChild) {
                tbody1.firstChild.remove();
            }
            while (tbody2.firstChild) {
                tbody2.firstChild.remove();
            }
            for (i = data.length - 1; i > 2 ; i--) {
                var tbody;
                if(data[i][2] > 0) {
                    tbody = tbody1;
                } else {
                    tbody = tbody2;
                }
                var row = tbody.insertRow(0);
                var cell1 = row.insertCell(0);
                cell1.innerHTML = data[i][1];
                var cell2 = row.insertCell(1);
                if(data[i][2] > 0) {
                    cell2.classList.add('positive');
                    cell2.innerHTML = "Buy";
                } else {
                    cell2.classList.add('negative');
                    cell2.innerHTML = "Sell";
                }
                var cell3 = row.insertCell(2);
                var now = Math.floor((new Date()).getTime() / 1000);
                var time = Math.floor(Date.parse(data[i][6] + " GMT") / 1000)
	            var diff = Math.floor((now - time) / 60 / 60);
	            cell3.innerHTML = data[i][6].substring(0, data[i][6].length - 3); + "<br>" + diff + " hours ago";
	            var cell4 = row.insertCell(3);
                cell4.innerHTML = data[i][4] + "<br>" + data[i][5];
                var change = data[i][5] - data[i][4];
                var changep = (data[i][5] - data[i][4]) / data[i][4] * 100;
                var max_up = data[i][8] - data[i][4];
                var max_down = data[i][9] - data[i][4];
                var cell5 = row.insertCell(4);
                cell5.innerHTML = changep.toFixed(2) + "%<br>" + topips(data[i][1], data[i][2], change) + " pips";
                var cell6 = row.insertCell(5);
                if(data[i][2] > 0){
                    if(change >= 0){
	                    cell5.classList.add('positive');
	                } else {
	                    cell5.classList.add('negative');
	                }
	                cell6.innerHTML = topips(data[i][1], data[i][2], max_up) + " pips<br>" + topips(data[i][1], data[i][2], max_down) + " pips";
                } else {
                    if(change <= 0){
	                    cell5.classList.add('positive');
	                } else {
	                    cell5.classList.add('negative');
	                }
	                cell6.innerHTML = topips(data[i][1], data[i][2], max_down * -1) + " pips<br>" + topips(data[i][1], data[i][2], max_up * -1) + " pips";
                }
            }
        } else {
            console.error(users);
        }
    }
    xhr.send(null);
}

function tradingview(symbol) {
	  new TradingView.widget({
		  "width": 800,
		  "height": 400,
		  "symbol": "OANDA:" + symbol,
		  "interval": "60",
		  "timezone": "Etc/UTC",
		  "theme": "light",
		  "style": "1",
		  "locale": "en",
		  "toolbar_bg": "#f1f3f6",
		  "enable_publishing": false,
		  "enable_publishing": false,
		  "save_image": false,
		  "show_popup_button": true,
		  "popup_width": "980",
		  "popup_height": "610",
		    "studies": [
			    "MAExp@tv-basicstudies",
			    "MACD@tv-basicstudies",
			    "RSI@tv-basicstudies",
			  ],
		  "container_id": "tradingview_" + symbol
		}
	  );
}

function topips(symbol, type, change) {
    var pips = 0;
    var digits = 0.0001;
    if(symbol.search("JPY") > 0) {
        digits = 0.01;
    }
    if(symbol.search("BTC") > 0 || symbol.search("ETH") > 0) {
        digits = 1;
    }
    if(type == 1) {
        pips = change / digits;
    }
    if(type == -1) {
        pips = change / digits;
    }
    return(pips.toFixed(0));
}

function timestamp() {
	return(Math.floor((new Date()).getTime() / 100000));
}

function clock() {
	var local_time = document.getElementById("local_time");
	var gmt_time = document.getElementById("gmt_time");
	var date = new Date();
	local_time.innerHTML = date.toString('en-US').substring(0, date.toString('en-US').indexOf('('));
	gmt_time.innerHTML = date.toUTCString('en-US');
}

setInterval(clock, 1000);

function loads() {
  load_sentiments();
  load_signals();
}

function reload() {
	location.reload()
}

loads();
setInterval(loads, 1 * 60 * 1000);
setInterval(reload, 30 * 60 * 1000);

