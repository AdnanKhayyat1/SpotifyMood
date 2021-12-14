

document.addEventListener('DOMContentLoaded', function () {
    var chx = document.getElementById("mood_chart");

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var t = tabs[0];
        let URL = t.url
        if(!URL.includes('/playlist/')){
            $('#loading').html('<h2>Oops! Something went wrong. Please refresh or try another page. </h2>');
        } else {
            chrome.tabs.sendMessage(t.id,URL, function(response) {
                fourMoods = response.data;
                $('#loading').empty();
                var mChart = new Chart(chx, {
                    type: 'polarArea',
                    data: {
                        labels: [ 'Happy', 'Sad', 'Energetic', 'Chill'],
                            datasets: [{
                            backgroundColor: [
                                "#1db954",
                                "#3b6148",
                                '#44c973',
                                '#6be897'
                            ],
                            data: fourMoods,
                        }]
                    },
                    // options.plugins.legend.title
                    options: {
                        legend: {
                            labels: {
                                fontColor: "#FFFFFF",
                            }
                        },
                        borderWidth: 0,
                    }
                });
                //$('#hs').html('<p>Happy: ' + fourMoods[0] + ' Sad:'+ fourMoods[1]);
                //$('#ce').html('<p>Chill: ' + fourMoods[3] + ' Energetic:'+ fourMoods[2]);
                
                
                
            });
        }
        
        // use `url` here inside the callback because it's asynchronous!
        //getData(url)
    });
});
