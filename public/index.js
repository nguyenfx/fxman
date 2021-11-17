function load_sentiments() {
		var sen_image = document.getElementById("sen_image");
        sen_image.src = "sentiments.png?" + timestamp();
}

function load_signals() {
    var xhr  = new XMLHttpRequest()
    xhr.open('GET', "signals.json?" + timestamp(), true)
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == "200") {
            var data = JSON.parse(xhr.responseText);
            var tbody1 = document.getElementById("signals1").getElementsByTagName('tbody')[0];
            var tbody2 = document.getElementById("signals2").getElementsByTagName('tbody')[0];
            while (tbody1.firstChild) {
                tbody1.firstChild.remove();
            }
            while (tbody2.firstChild) {
                tbody2.firstChild.remove();
            }
            for (i = data.length - 1; i >= 0 ; i--) {
                var tbody;
                if(i % 2 == 0) {
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
	            var diff = Math.floor((now - time) / 60);
	            cell3.innerHTML = data[i][6] + " GMT<br>" + diff + " minutes ago";
	            var cell4 = row.insertCell(3);
                cell4.innerHTML = data[i][4] + "<br>" + data[i][5];
                var change = (data[i][5] - data[i][4]) / data[i][4] * 100;
                var cell5 = row.insertCell(4);
                if((data[i][2] > 0 && change >= 0) || (data[i][2] < 0 && change <= 0)){
                    cell5.classList.add('positive');
                } else {
                    cell5.classList.add('negative');
                }
                cell5.innerHTML = change.toFixed(2) + "%";
	            var row1 = tbody.insertRow(1);
	            row1.innerHTML = '<td colspan="5"><div id="tradingview_' + data[i][1] + '"></div></td>'
	            tradingview(data[i][1])
            }
        } else {
            console.error(users);
        }
    }
    xhr.send(null);
}

function tradingview(symbol) {
	  new TradingView.widget({
		  "width": 400,
		  "height": 250,
		  "symbol": "OANDA:" + symbol,
		  "interval": "240",
		  "timezone": "Etc/UTC",
		  "theme": "light",
		  "style": "1",
		  "locale": "en",
		  "toolbar_bg": "#f1f3f6",
		  "enable_publishing": false,
		  "hide_top_toolbar": true,
		  "hide_legend": true,
		  "save_image": false,
		  "show_popup_button": true,
		  "popup_width": "980",
		  "popup_height": "610",
		  "studies": [
			    "MAExp@tv-basicstudies",
                "MACD@tv-basicstudies",
                "RSI@tv-basicstudies"
		  ],
		  "container_id": "tradingview_" + symbol
		}
	  );
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
setInterval(loads, 5 * 60 * 1000);
setInterval(reload, 30 * 60 * 1000);
