// 表单数据处理工具函数
const formDataHandler = {
	// 获取表单数据
	getFormData: formId => {
		const form = document.getElementById(formId)
		if (!form) return {}
		const formData = new FormData(form)
		const data = {}
		for (let [key, value] of formData.entries()) {
			data[key] = value
		}
		return data
	},

	// 填充表单数据
	fillFormData: (formId, data) => {
		const form = document.getElementById(formId)
		if (!form || !data) return
		form.querySelectorAll('input').forEach(input => {
			const key = input.name
			if (key && data[key] !== undefined) {
				input.value = data[key]
			}
		})
	},
}

// 提交数据
document.getElementById('submitBtn').addEventListener('click', async () => {
	const obj = {
		usData: formDataHandler.getFormData('usForm'),
		glData: formDataHandler.getFormData('glForm'),
	}
	await window.pywebview.api.submit_data(obj) // 调用 Python 后端接口提交数据
})

// 页面加载时填充数据
window.addEventListener('load', async () => {
	setTimeout(async () => {
		const savedData = await window.pywebview.api.default_data() // 获取默认数据
		formDataHandler.fillFormData('usForm', savedData.usData)
		formDataHandler.fillFormData('glForm', savedData.glData)
	}, 100)
})
