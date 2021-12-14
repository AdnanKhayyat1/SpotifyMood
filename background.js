const BASE_URL = 'http://localhost:8080/pl'
function getData(url){
    const urlParams = new URLSearchParams(url);
    console.log(urlParams)
    //const url = BASE_URL + 
    //fetch('http://www.example.com?par=0').then(r => r.text()).then(result => {
    // Result now contains the response text, do what you want...
    //})
}
var activeTabId;

chrome.tabs.query({active: true, currentWindow: true}, tabs => {
    let url = tabs[0].url;
    console.log(window.location)
    // use `url` here inside the callback because it's asynchronous!
    getData(url)
});
