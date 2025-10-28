Title: Base64在线转换工具
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: 工具
keywords: 在线Base64编码/解码工具
summary: 在线Base64编码/解码工具
lang: zh
status: published
Slug: base64_converter
url: base64_converter

---
<div>
    <h3>Base64编码/解码工具</h3>
        <div class="base64-tool">
            <div class="input-group">
                <label for="text-input">文本输入：</label>
                <textarea id="text-input" placeholder="输入要编码的文本或要解码的Base64字符串" rows="5"></textarea>
                <div class="button-group">
                    <button onclick="encodeBase64()">Base64编码</button>
                    <button onclick="decodeBase64()">Base64解码</button>
                    <button onclick="clearText()">清空</button>
                </div>
            </div>
            <div class="result-group">
                <h4>转换结果：</h4>
                <textarea id="result" placeholder="转换结果将显示在这里" rows="5" readonly></textarea>
            </div>
            <div class="file-group">
                <h4>文件转换：</h4>
                <input type="file" id="file-input" onchange="handleFileSelect()">
                <div id="file-result"></div>
            </div>
        </div>
        <style>
            .base64-tool {
                max-width: 600px;
                margin: 20px 0;
            }
            .input-group, .result-group, .file-group {
                margin: 15px 0;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .input-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-family: monospace;
                resize: vertical;
            }
            .button-group {
                margin-top: 10px;
            }
            .button-group button {
                background-color: #007cba;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 3px;
                cursor: pointer;
                margin-right: 10px;
            }
            .button-group button:hover {
                background-color: #005a87;
            }
            .file-group input {
                margin: 10px 0;
            }
            #file-result {
                margin-top: 10px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 3px;
            }
        </style>
        <script>
            function encodeBase64() {
                const textInput = document.getElementById('text-input').value;
                const resultTextarea = document.getElementById('result');
                if (!textInput.trim()) {
                    resultTextarea.value = '请输入要编码的文本';
                    return;
                }
                try {
                    const encoded = btoa(unescape(encodeURIComponent(textInput)));
                    resultTextarea.value = encoded;
                } catch (e) {
                    resultTextarea.value = '编码失败：' + e.message;
                }
            }
            function decodeBase64() {
                const textInput = document.getElementById('text-input').value.trim();
                const resultTextarea = document.getElementById('result');
                if (!textInput) {
                    resultTextarea.value = '请输入要解码的Base64字符串';
                    return;
                }
                try {
                    // 移除可能的data URL前缀
                    let base64String = textInput;
                    if (base64String.includes(',')) {
                        base64String = base64String.split(',')[1];
                    }
                    const decoded = decodeURIComponent(escape(atob(base64String)));
                    resultTextarea.value = decoded;
                } catch (e) {
                    resultTextarea.value = '解码失败：请检查输入的Base64格式是否正确';
                }
            }
            function clearText() {
                document.getElementById('text-input').value = '';
                document.getElementById('result').value = '';
                document.getElementById('file-result').innerHTML = '';
            }
            function handleFileSelect() {
                const fileInput = document.getElementById('file-input');
                const fileResult = document.getElementById('file-result');
                const file = fileInput.files[0];
                if (!file) {
                    return;
                }
                const reader = new FileReader();
                reader.onload = function(e) {
                    const base64 = e.target.result;
                    fileResult.innerHTML = `
                        <p><strong>文件名：</strong>${file.name}</p>
                        <p><strong>文件大小：</strong>${(file.size / 1024).toFixed(2)} KB</p>
                        <p><strong>Base64编码：</strong></p>
                        <textarea style="width:100%; height:100px; font-size:12px;" readonly>${base64}</textarea>
                        <button onclick="copyToClipboard('${base64.replace(/'/g, "\\'")}')">复制Base64</button>
                        <button onclick="downloadBase64File('${base64.replace(/'/g, "\\'")}', '${file.name}')">下载文件</button>
                    `;
                };
                reader.onerror = function() {
                    fileResult.innerHTML = '<span style="color:red;">文件读取失败</span>';
                };
                reader.readAsDataURL(file);
            }
            function copyToClipboard(text) {
                const textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert('已复制到剪贴板');
            }
            function downloadBase64File(base64Data, filename) {
                const link = document.createElement('a');
                link.href = base64Data;
                link.download = filename;
                link.click();
            }
        </script>
    </div>