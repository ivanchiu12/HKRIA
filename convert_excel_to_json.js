const XLSX = require('xlsx');
const fs = require('fs');

// Read the Excel file
const workbook = XLSX.readFile('geomap_restaurant.xlsx');
const sheet_name_list = workbook.SheetNames;
const jsonData = XLSX.utils.sheet_to_json(workbook.Sheets[sheet_name_list[0]]);

// Write to a JSON file
fs.writeFileSync('restaurants.json', JSON.stringify(jsonData, null, 2), 'utf8');

console.log('Excel file converted to JSON successfully.');
