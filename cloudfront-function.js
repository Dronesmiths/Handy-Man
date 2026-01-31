function handler(event) {
    var request = event.request;
    var uri = request.uri;

    // Check if the URI is a directory (ends with /)
    if (uri.endsWith('/')) {
        request.uri += 'index.html';
    }
    // Check if the URI doesn't have a file extension
    else if (!uri.includes('.')) {
        request.uri += '/index.html';
    }

    return request;
}
