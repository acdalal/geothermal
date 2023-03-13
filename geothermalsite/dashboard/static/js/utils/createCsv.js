function downloadData(fileName) {
    var csv = "";
    var keys = Object.keys(queryData[0]);
    var keyArray = [];
    keys.forEach((key) => {
        keyArray.push(key);
    });
    let keyRow = keyArray.join(",");
    csv += keyRow + "\n";

    queryData.forEach((row) => {
        let rowElements = [];
        keyArray.forEach((key) => {
            rowElements.push(row[key]);
        });
        let csvRow = rowElements.join(",");
        csv += csvRow;
        csv += "\n";
    });

    var newElement = document.createElement("a");
    newElement.href = "data:text/csv;charset=utf-8," + encodeURI(csv);

    //provide the name for the CSV file to be downloaded
    newElement.download = fileName + ".csv";
    newElement.click();
}
