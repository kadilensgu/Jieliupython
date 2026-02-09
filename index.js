// 获取表单数据，发送数据
document.getElementById('submitBtn').addEventListener('click', async () => {
	const form = document.getElementById('dataForm')
	const obj = {}
	const formData = new FormData(form)
	for (let [key, value] of formData.entries()) {
		obj[key] = value
	}
	out.textContent = '正在提交...'
	const res = await window.pywebview.api.submit_data(obj)
	out.textContent = '修改成功！' + JSON.stringify(res)
})
