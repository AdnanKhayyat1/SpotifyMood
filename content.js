const BASE_URL = 'http://localhost:8080/pl/'
async function fetchData(url){
    const urlPath = url.split('/')[4];
    const playlistID = urlPath.indexOf('?') == -1 ? urlPath : urlPath.substr(0, urlPath.indexOf('?'));
    fetchURL = BASE_URL+playlistID
    let res = await fetch(fetchURL).then(response => {
        return response.json();     
    });

    let moods = res[Object.keys(res)[0]]; 

    return moods;
    
}
async function getData(request, sr){
    const moods = await fetchData(request);
    sr({"data": moods});
};
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
        getData(request,sendResponse)
        return true;
});