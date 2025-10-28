---
Title: 在线生成二维码
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: 工具
keywords: 在线生成二维码
summary: 在线生成二维码
lang: zh
status: published
Slug: qrcode_create
url: qrcode_create
---

<div>
  <h3>二维码生成工具</h3>
  <div class="qrcode-tool">
    <div class="input-group">
      <label for="qrcode-text">输入内容：</label>
      <textarea id="qrcode-text" placeholder="输入文本、URL或其他内容生成二维码" rows="4"></textarea>
    </div>

    <div class="options-group">
      <div class="option-item">
        <label for="qrcode-size">二维码尺寸：</label>
        <select id="qrcode-size">
          <option value="128">128x128</option>
          <option value="200" selected>200x200</option>
          <option value="256">256x256</option>
          <option value="300">300x300</option>
        </select>
      </div>

      <div class="option-item">
        <label for="qrcode-color">前景色：</label>
        <div class="color-picker">
          <input type="color" id="qrcode-color" value="#000000">
          <span id="color-preview" class="color-preview" style="background-color: #000000"></span>
          <span id="color-value">#000000</span>
        </div>
      </div>

      <div class="option-item">
        <label for="qrcode-bgcolor">背景色：</label>
        <div class="color-picker">
          <input type="color" id="qrcode-bgcolor" value="#ffffff">
          <span id="bgcolor-preview" class="color-preview" style="background-color: #ffffff"></span>
          <span id="bgcolor-value">#ffffff</span>
        </div>
      </div>
    </div>

    <div class="button-group">
      <button id="generate-btn">生成二维码</button>
      <button id="clear-btn">清空</button>
    </div>

    <div class="result-group">
      <h4>二维码预览：</h4>
      <div id="qrcode-container">
        <!-- 这里会插入二维码（img / canvas / table） -->
      </div>
      <div id="qrcode-error" style="color: red; display: none;"></div>
    </div>

    <div class="download-group">
      <button id="download-btn" disabled>下载二维码</button>
      <select id="download-format">
        <option value="png">PNG</option>
        <option value="jpeg">JPEG</option>
      </select>
    </div>
  </div>

  <style>
    .qrcode-tool {
      max-width: 600px;
      margin: 20px 0;
    }
    .input-group, .options-group, .result-group, .download-group {
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
      width: 90%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 3px;
      resize: vertical;
      font-size: 14px;
    }
    .options-group {
      display: flex;
      flex-direction: column;
      gap: 15px;
    }
    .option-item {
      display: flex;
      align-items: center;
      gap: 15px;
    }
    .option-item label {
      font-weight: bold;
      width: 100px;
      margin: 0;
    }
    .color-picker {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .color-preview {
      width: 30px;
      height: 30px;
      border: 1px solid #ccc;
      border-radius: 3px;
      display: inline-block;
    }
    #color-value, #bgcolor-value {
      font-family: monospace;
      font-size: 14px;
      min-width: 70px;
    }
    .button-group, .download-group {
      display: flex;
      gap: 10px;
      align-items: center;
    }
    button {
      background-color: #007cba;
      color: white;
      padding: 8px 15px;
      border: none;
      border-radius: 3px;
      cursor: pointer;
      font-size: 14px;
    }
    button:hover {
      background-color: #005a87;
    }
    button:disabled {
      background-color: #cccccc;
      cursor: not-allowed;
    }
    #qrcode-container {
      text-align: center;
      margin: 20px 0;
      padding: 20px;
      background-color: #f8f9fa;
      border-radius: 5px;
      min-height: 220px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    #qrcode img, #qrcode canvas, #qrcode table {
      max-width: 100%;
      height: auto;
      border: 1px solid #ddd;
      background: white;
    }
  </style>

  <!-- 正确的 QRCode 库（davidshimjs 的 qrcodejs），会导出全局 QRCode 构造函数 -->
  <script src="https://cdn.jsdelivr.net/gh/davidshimjs/qrcodejs/qrcode.min.js"></script>

  <script>
    // 全局变量保存二维码实例与配置
    let qrcodeInstance = null;

    document.addEventListener('DOMContentLoaded', function () {
      // 初始化颜色显示
      updateColorDisplay('qrcode-color', 'color-preview', 'color-value');
      updateColorDisplay('qrcode-bgcolor', 'bgcolor-preview', 'bgcolor-value');

      document.getElementById('qrcode-color').addEventListener('input', function () {
        updateColorDisplay('qrcode-color', 'color-preview', 'color-value');
      });
      document.getElementById('qrcode-bgcolor').addEventListener('input', function () {
        updateColorDisplay('qrcode-bgcolor', 'bgcolor-preview', 'bgcolor-value');
      });

      document.getElementById('generate-btn').addEventListener('click', generateQRCode);
      document.getElementById('clear-btn').addEventListener('click', clearQRCode);
      document.getElementById('download-btn').addEventListener('click', downloadQRCode);

      // 初始化显示提示
      initQRCodePlaceholder();
    });

    function updateColorDisplay(colorInputId, previewId, valueId) {
      const colorInput = document.getElementById(colorInputId);
      const preview = document.getElementById(previewId);
      const value = document.getElementById(valueId);
      preview.style.backgroundColor = colorInput.value;
      value.textContent = colorInput.value;
    }

    function initQRCodePlaceholder() {
      const container = document.getElementById('qrcode-container');
      container.innerHTML = '<div id="qrcode" style="width:200px;height:200px;display:flex;align-items:center;justify-content:center;"></div>';
      const el = document.createElement('div');
      el.style.textAlign = 'center';
      el.style.color = '#666';
      el.style.fontSize = '14px';
      el.textContent = '请输入内容生成二维码';
      document.getElementById('qrcode').appendChild(el);
      document.getElementById('download-btn').disabled = true;
    }

    function generateQRCode() {
      const text = document.getElementById('qrcode-text').value.trim();
      const size = parseInt(document.getElementById('qrcode-size').value, 10);
      const color = document.getElementById('qrcode-color').value;
      const bgColor = document.getElementById('qrcode-bgcolor').value;
      const errorDiv = document.getElementById('qrcode-error');
      const downloadBtn = document.getElementById('download-btn');

      if (!text) {
        errorDiv.textContent = '请输入要生成二维码的内容';
        errorDiv.style.display = 'block';
        downloadBtn.disabled = true;
        return;
      }
      errorDiv.style.display = 'none';

      // 确保全局 QRCode 可用
      if (typeof QRCode !== 'function') {
        errorDiv.textContent = '二维码库未加载或不兼容，请检查网络或换用支持的 CDN。';
        errorDiv.style.display = 'block';
        return;
      }

      // 清空容器并创建目标容器
      const container = document.getElementById('qrcode-container');
      container.innerHTML = '<div id="qrcode"></div>';

      // 如果之前有实例，清除（qrcodejs 没有 destroy API，所以直接清空容器）
      try {
        qrcodeInstance = new QRCode(document.getElementById("qrcode"), {
          text: text,
          width: size,
          height: size,
          colorDark: color,
          colorLight: bgColor,
          correctLevel: QRCode.CorrectLevel.H
        });
      } catch (e) {
        errorDiv.textContent = '生成二维码失败：' + (e && e.message ? e.message : e);
        errorDiv.style.display = 'block';
        downloadBtn.disabled = true;
        return;
      }

      // qrcodejs 可能会以 <img> 或 <table> 形式插入，等 DOM 稳定后启用下载
      setTimeout(() => {
        downloadBtn.disabled = false;
      }, 200);
    }

    function clearQRCode() {
      document.getElementById('qrcode-text').value = '';
      document.getElementById('qrcode-error').style.display = 'none';
      document.getElementById('download-btn').disabled = true;
      initQRCodePlaceholder();
    }

    function downloadQRCode() {
      const format = document.getElementById('download-format').value;
      const rawText = document.getElementById('qrcode-text').value.trim().substring(0, 20) || 'qrcode';
      const downloadName = `qrcode-${rawText}.${format}`;

      const qrContainer = document.getElementById('qrcode');
      if (!qrContainer) return;

      // qrcodejs 输出可能是 <img>（data URL）或 <table>（用表格绘制），有些实现会生成 canvas
      const imgEl = qrContainer.querySelector('img');
      const canvasEl = qrContainer.querySelector('canvas');
      const tableEl = qrContainer.querySelector('table');

      if (imgEl && imgEl.src) {
        // img 的 src 通常是 data URL，可以直接下载
        triggerDownload(imgEl.src, downloadName);
        return;
      }

      if (canvasEl) {
        // 将 canvas 导出为指定格式
        const mime = format === 'jpeg' ? 'image/jpeg' : 'image/png';
        const dataUrl = canvasEl.toDataURL(mime);
        triggerDownload(dataUrl, downloadName);
        return;
      }

      if (tableEl) {
        // 将 table 绘制到 canvas，然后导出（通用方式）
        const size = parseInt(document.getElementById('qrcode-size').value, 10);
        const canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');

        // 背景色
        ctx.fillStyle = document.getElementById('qrcode-bgcolor').value;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // table->pixels：每个 table cell 对应一个小块，遍历并绘制
        // 注意：qrcodejs 生成 table 时，table 的宽高会包含边距，这里用简单方法按子元素绘制
        const cells = Array.from(tableEl.querySelectorAll('td'));
        if (cells.length === 0) {
          alert('无法读取二维码数据用于下载（table 无单元格）。');
          return;
        }
        // 计算格子数（行数）
        const rows = tableEl.querySelectorAll('tr').length;
        const cols = tableEl.querySelectorAll('tr')[0].children.length;
        const cellSize = Math.min(canvas.width / cols, canvas.height / rows);

        const trs = tableEl.querySelectorAll('tr');
        for (let r = 0; r < trs.length; r++) {
          const tds = trs[r].children;
          for (let c = 0; c < tds.length; c++) {
            const td = tds[c];
            const bg = window.getComputedStyle(td).backgroundColor;
            // 如果是黑色点则绘制深色块
            if (!bg || bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') continue;
            ctx.fillStyle = bg;
            ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
          }
        }
        const mime = format === 'jpeg' ? 'image/jpeg' : 'image/png';
        const dataUrl = canvas.toDataURL(mime);
        triggerDownload(dataUrl, downloadName);
        return;
      }

      alert('未找到可下载的二维码元素（img / canvas / table）。');
    }

    function triggerDownload(dataUrl, filename) {
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
  </script>
</div>
