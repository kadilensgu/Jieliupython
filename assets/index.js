// 获取表单数据，发送数据
document.getElementById('submitBtn').addEventListener('click', async () => {
	var obj = {
		usData: {},
		glData: {},
	}

	// 获取美国区域表单数据
	var usForm = document.getElementById('usForm')
	if (usForm) {
		var usFormData = new FormData(usForm)
		for (let [key, value] of usFormData.entries()) {
			obj.usData[key] = value
		}
	}

	// 获取全球区域表形数据
	var glForm = document.getElementById('glForm')
	if (glForm) {
		var glFormData = new FormData(glForm)
		for (let [key, value] of glFormData.entries()) {
			obj.glData[key] = value
		}
	}
	const res = await window.pywebview.api.submit_data(obj)
})
