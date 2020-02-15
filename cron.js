const schedule = require('node-schedule')

var path = require('path')

const child_process = require('child_process')

const fs = require("fs");

const file = path.join(__dirname, './log/cron.log')

const date = new Date()

const day = date.getDate()

const hour = date.getHours()

const minute = date.getMinutes()

const second = date.getSeconds()

const time = hour + ':' + minute + ':' + second

let log = (error) => {

	fs.writeFile(file, time + ':' + error + '\n', { flag: 'a' },(err)=>{
		
		if (err) {

				console.log(err)

			}
		}
	)
}

let addChat = schedule.scheduleJob('10 */12 * * * *', async () => {
	
	const cmd_add = 'python3 addChat.py'

	const child_addChat = child_process.exec(cmd_add,{timeout:100000},function (error, stdout, stderr) {
		
		if (error) {

			log('child_error:' + JSON.stringify(error))
		}

		if(stdout){
			
			log('child_stdout: ' + stdout)
		}
	})

	child_addChat.on('exit', (code, signal) => {

		log(`exit code ${code} child process exited with signal ${signal}`)
	})
})

let childnum = 0

let clear = schedule.scheduleJob('*/10 * * * * *', async () => {

	if (childnum<2) {

		childnum = childnum + 1

		console.log(childnum,'开始执行')

		const cmd_clear = 'python3 clearJob.py'

		// timeout:15000

		const child_clear = child_process.exec(cmd_clear,{},function (error, stdout, stderr) {
		
			if (error) {

				log('child_error:' + JSON.stringify(error),childnum)
			}

			if(stdout){

				log('child_stdout: ' + stdout,childnum)
			}
		})

		child_clear.on('exit', (code, signal) => {

			console.log(childnum,'结束执行')

			childnum = childnum - 1

			log(`exit code ${code} child process exited with signal ${signal}`)
		})	
	}
})