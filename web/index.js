// Usage Example:
const hakatomi_api = new APIAdapter('hakatomi');

function refresh() {
    hakatomi_api.get('/v1/logs/tail', {  }, { size: 10 })
        .then(data => {
            entries = data.toString().split(',');
            table = ""
            for (let i = 0; i < entries.length; i++ )
            {
                table += `<tr><td>${entries[i]}</td></tr>`
            }
            document.getElementById('table-logs').innerHTML = table;
        })
        .catch(err => console.error(`Error occurred: ${err}`));

    hakatomi_api.get('/v1/measure/signin/success', {  }, {  })
        .then(data => {
            rate = data.rate;
            data = data.locked;
            document.getElementById('count-3').style = `width: 0%`;
            user_count = 0;
            for (let i = 0; i < data.count.length; i++) {
                user_count += data.count[i]
            }
            for (let i = 0; i < data.attempts.length; i++)
            {
                if (data.attempts[i] == 3) {
                    document.getElementById('count-3').style = `width: ${(data.count[i] * 100) / user_count}%`;
                    document.getElementById('count-3').innerText = `${(data.count[i] * 100) / user_count}%`;
                }
            }
        })
        .catch(err => console.error(`Error occurred: ${err}`));
}



setInterval(refresh, 5 * 1000);