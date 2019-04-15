const fs = require('fs');
const newman = require('newman');

// logging into a file
function writeToDisk(fileName, content) {
	fs.writeFile(fileName, content, function(error) {
		if (error) {
			console.error(error);
		}
	});
}

// logged results
const results_response_statuses = [];
const results_failed_assertions = [];
// file names
const response_statuses_file_name = 'newman/response_statuses.txt';
const failed_assertions_file_name = 'newman/failed_assertions.txt';

newman.run({
    collection: require('./Skills.postman_collection.json'),
	environment: require('./Skills_API - localhost.postman_environment.json'),
	bail: true,
	reporters: ['cli', 'junit', 'html', 'htmlextra']
}).on('request', function (err, args) {
    results_response_statuses.push(args.item.name + ': ' + args.response.code + ' ' + args.response.status);
}).on('assertion', function (err, args) {
	if (args.error) {
		results_failed_assertions.push(args.item.name + ' - ' + args.assertion + '\n' + args.error.name + ' - ' + args.error.message + ' - ' + 'expected: ' + args.error + 'actual: ' + args.error + 'stack: ' + args.error.stack);
	}
}).on('done', function (err, args) {
	writeToDisk(response_statuses_file_name, results_response_statuses.join('\n'));
	if(results_failed_assertions.length !== 0) {
        console.log(`\nThere are ${results_failed_assertions.length} test failure(s)!\n`);		
		writeToDisk(failed_assertions_file_name, results_failed_assertions.join('\n'));
    }
});