# 万家康羊山窑店门店页

静态门店页，用于地图/微信/抖音等渠道的统一落地页。

- 门店：内蒙古万家康医药连锁有限公司羊山窑店
- 地址：包头市青山区兴胜镇羊山窑子村西区4排107号
- 电话：13664076072
- 页面：`index.html`
- 二维码：`assets/qr.png`（指向 GitHub Pages 地址）
- SEO：`robots.txt`、`sitemap.xml`、JSON-LD（Pharmacy + FAQ）

## 本地预览

直接用浏览器打开 `index.html`。

## 部署

```bash
gh repo create cbbccb915/wanjiakang-yangshanyao --public --source . --remote origin --push
gh api -X POST repos/cbbccb915/wanjiakang-yangshanyao/pages -f 'source[branch]=main' -f 'source[path]=/'
```

部署后地址：<https://cbbccb915.github.io/wanjiakang-yangshanyao/>

> 页面中的服务项目、营业时间、医保政策均标注“以门店现场为准”，避免与实际不一致。
