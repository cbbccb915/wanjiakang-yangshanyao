(function () {
  try {
    var page = (document.body && document.body.getAttribute('data-page')) || 'home';
    var day = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Asia/Shanghai',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }).format(new Date()).replace(/-/g, '');
    var path = 'wjk2-' + page + '-' + day;
    var img = new Image();
    img.width = 1;
    img.height = 1;
    img.alt = '';
    img.style.cssText = 'position:absolute;left:-9999px;top:-9999px;width:1px;height:1px;opacity:0;pointer-events:none';
    img.src = 'https://api.visitorbadge.io/api/visitors?path=' + encodeURIComponent(path) +
      '&label=visits&countColor=%230b7a4b&t=' + Date.now();
    document.body.appendChild(img);
  } catch (e) {
    // 统计失败不影响页面
  }
})();
