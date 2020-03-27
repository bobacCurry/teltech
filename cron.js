const schedule = require('node-schedule')

var path = require('path')

const child_process = require('child_process')

const fs = require("fs");

const env = require('./env.js')

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

let addChat = schedule.scheduleJob('0 */10 * * * *', async () => {
	
	const cmd_add_chat = 'python3 addChat.py'

	const child_addChat = child_process.exec(cmd_add_chat,function (error, stdout, stderr) {})

	child_addChat.on('exit', (code, signal) => {

		log(`exit code ${code} child process exited with signal ${signal} -- addChat`)

	})
})

let clearChat = schedule.scheduleJob('10 * * * * *', async () => {
	
	const cmd_clear_chat = 'python3 clearChat.py'

	const child_clearChat = child_process.exec(cmd_clear_chat,function (error, stdout, stderr) {})

	child_clearChat.on('exit', (code, signal) => {

		log(`exit code ${code} child process exited with signal ${signal} -- clearChat`)

	})
})

let addJob = schedule.scheduleJob('0 * * * * *', async () => {

	const cmd_add_job = 'python3 addJob.py'

	const child_addJob = child_process.exec(cmd_add_job,{},function (error, stdout, stderr) {})

	child_addJob.on('exit', (code, signal) => {

		log(`exit code ${code} child process exited with signal ${signal} -- addJob`)
	})
})

let childnum = 0

let clearJob = schedule.scheduleJob('*/10 * * * * *', async () => {

	let maxnum = env.maxnum

	if (childnum<maxnum) {

		childnum = childnum + 1

		console.log(childnum,'开始执行')

		const cmd_clear_job = 'python3 clearJob.py'

		// {timeout:60000},

		const child_clearJob = child_process.exec(cmd_clear_job,function (error, stdout, stderr) {
		
			if (error) {

				log('child_error:' + JSON.stringify(error),childnum)

				console.log('child_error:' + JSON.stringify(error),childnum)

			}

			if(stdout){

				log('child_stdout: ' + stdout,childnum)
			}
		})

		child_clearJob.on('exit', (code, signal) => {

			console.log(childnum,'结束执行')

			childnum = childnum - 1

			log(`exit code ${code} child process exited with signal ${signal} -- clearJob`)
		})	
	}
})

let clearAdd = schedule.scheduleJob('0 */10 * * * *', async () => {

	const cmd_clear_add = 'python3 addMember.py'

	const child_clearAdd = child_process.exec(cmd_clear_add,function (error, stdout, stderr) {
	
		if (error) {

			log('child_error:' + JSON.stringify(error))

		}

		if(stdout){

			log('child_stdout: ' + stdout)
		}
	})

	child_clearAdd.on('exit', (code, signal) => {

		log(`exit code ${code} child process exited with signal ${signal} -- clearJob`)
	})	
})

let resetAdd = schedule.scheduleJob('0 0 0 * * *', async () => {

	const cmd_reset_add = 'python3 resetMember.py'

	const child_resetAdd = child_process.exec(cmd_reset_add,function (error, stdout, stderr) {
	
		if (error) {

			log('child_error:' + JSON.stringify(error))

		}

		if(stdout){

			log('child_stdout: ' + stdout)
		}
	})

	child_resetAdd.on('exit', (code, signal) => {

		log(`exit code ${code} child process exited with signal ${signal} -- clearJob`)
	})

})