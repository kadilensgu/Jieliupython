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
		document.querySelectorAll('input[type="date"]').forEach(input => {
			input.valueAsDate = new Date()
		})
	}, 100)
})

function getContrastColors() {
	// 生成随机颜色
	const color = Math.floor(Math.random() * 16777215)
	const hexColor = '#' + color.toString(16).padStart(6, '0')

	// 计算反色（对比色）
	const r = (color >> 16) & 255
	const g = (color >> 8) & 255
	const b = color & 255

	// 计算亮度，决定用黑还是白
	const brightness = (r * 299 + g * 587 + b * 114) / 1000
	const contrastColor = brightness > 128 ? '#000000' : '#FFFFFF'

	return [hexColor, contrastColor]
}

// 随机生成数据叠加
document.getElementById('randomBtn').addEventListener('click', async () => {
	var rangeinput = document.getElementById('rangeinput').value
	var [bgColor, textColor] = getContrastColors()

	//
	var inputObjs = document.querySelectorAll('form input')
	for (let inputNode of inputObjs) {
		if (inputNode.getAttribute('step') !== '0.001' && inputNode.type !== 'date') {
			let currentValue = parseFloat(inputNode.value) || 0
			//
			inputNode.value = parseInt(currentValue * rangeinput)
			//
			inputNode.style.backgroundColor = bgColor
			inputNode.style.color = textColor
			await new Promise(resolve => setTimeout(resolve, 20))
		}
	}
})
