Title: 时间戳在线转换
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: 工具
keywords: 在线转换时间戳、时间戳转换
summary: 在线转换时间戳
lang: zh
status: published
Slug: format_timestamp
url: format_timestamp

---

<div>
			<h3>时间戳转换工具</h3>
			<div class="timestamp-tool">
				<div class="input-group">
					<label for="timestamp-input">时间戳：</label>
					<input type="text" id="timestamp-input" placeholder="输入时间戳（秒或毫秒）">
					<button onclick="convertTimestamp()">转换为日期</button>
				</div>
				<div class="input-group">
					<label for="date-input">日期时间：</label>
					<input type="datetime-local" id="date-input">
					<button onclick="convertToTimestamp()">转换为时间戳</button>
				</div>
				<div class="result-group">
					<h4>转换结果：</h4>
					<div id="result"></div>
				</div>
				<div class="current-time">
					<h4>当前时间：</h4>
					<div id="current-time"></div>
					<button onclick="updateCurrentTime()">刷新</button>
				</div>
			</div>
			<style>
				.timestamp-tool {
					max-width: 600px;
					margin: 20px 0;
				}
				.input-group {
					margin: 15px 0;
					padding: 10px;
					border: 1px solid #ddd;
					border-radius: 5px;
				}
				.input-group label {
					display: block;
					margin-bottom: 5px;
					font-weight: bold;
                    margin-left: 10px;
                    width: auto;
				}
				.input-group input {
                    width: 300px;
                    padding: 8px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    display: block;
                    margin-left: 5px;
                    vertical-align: middle;
                }
                .input-group button {
                    background-color: #007cba;
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 3px;
                    cursor: pointer;
                    vertical-align: middle;
                    margin-left: 10px;
                }
				.input-group button:hover {
					background-color: #005a87;
				}
				.result-group, .current-time {
					margin: 15px 0;
					padding: 15px;
					background-color: #f8f9fa;
					border-radius: 5px;
				}
				#result {
					padding: 10px;
					background-color: white;
					border: 1px solid #ddd;
					border-radius: 3px;
					min-height: 40px;
				}
			</style>
			<script>
				function convertTimestamp() {
					const timestampInput = document.getElementById('timestamp-input').value.trim();
					const resultDiv = document.getElementById('result');
					if (!timestampInput) {
						resultDiv.innerHTML = '<span style="color: red;">请输入时间戳</span>';
						return;
					}
					let timestamp = parseInt(timestampInput);
					// 判断是秒还是毫秒
					if (timestampInput.length === 10) {
						// 10位时间戳（秒）
						timestamp *= 1000;
					} else if (timestampInput.length !== 13) {
						resultDiv.innerHTML = '<span style="color: red;">请输入10位（秒）或13位（毫秒）时间戳</span>';
						return;
					}
					const date = new Date(timestamp);
					if (isNaN(date.getTime())) {
						resultDiv.innerHTML = '<span style="color: red;">无效的时间戳</span>';
						return;
					}
					const localTime = date.toLocaleString();
					const utcTime = date.toUTCString();
					resultDiv.innerHTML = `
						<p><strong>本地时间：</strong>${localTime}</p>
						<p><strong>UTC时间：</strong>${utcTime}</p>
						<p><strong>时间戳（毫秒）：</strong>${timestamp}</p>
						<p><strong>时间戳（秒）：</strong>${Math.floor(timestamp / 1000)}</p>
					`;
				}
				function convertToTimestamp() {
					const dateInput = document.getElementById('date-input').value;
					const resultDiv = document.getElementById('result');
					if (!dateInput) {
						resultDiv.innerHTML = '<span style="color: red;">请选择日期时间</span>';
						return;
					}
					const date = new Date(dateInput);
					const timestampMs = date.getTime();
					const timestampS = Math.floor(timestampMs / 1000);
					resultDiv.innerHTML = `
						<p><strong>时间戳（毫秒）：</strong>${timestampMs}</p>
						<p><strong>时间戳（秒）：</strong>${timestampS}</p>
						<p><strong>对应时间：</strong>${date.toLocaleString()}</p>
					`;
				}
				function updateCurrentTime() {
					const now = new Date();
					const currentTimeDiv = document.getElementById('current-time');
					currentTimeDiv.innerHTML = `
						<p><strong>本地时间：</strong>${now.toLocaleString()}</p>
						<p><strong>UTC时间：</strong>${now.toUTCString()}</p>
						<p><strong>当前时间戳（毫秒）：</strong>${now.getTime()}</p>
						<p><strong>当前时间戳（秒）：</strong>${Math.floor(now.getTime() / 1000)}</p>
					`;
				}
				// 初始化显示当前时间
				updateCurrentTime();
			</script>
		</div>