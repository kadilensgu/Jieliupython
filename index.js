// 获取表单数据，发送数据
document.getElementById('submitBtn').addEventListener('click', async () => {
	const form = document.getElementById('dataForm')
	const data = {}
	for (let i = 0; i < form.length; i++) {
		let element = form[i]
		if (element.name) {
			data[element.name] = element.value || 0
		}
	}
	out.textContent = '正在提交...'
	const res = await window.pywebview.api.submit_data(data)
	out.textContent = '修改成功！' + JSON.stringify(res)
})
