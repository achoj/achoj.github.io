var Fontmin = require("fontmin")

var fontmin = new Fontmin()
  .src("./fonts/SiYuan.ttf")
  .dest("./fontmins/")
  .use(
    Fontmin.glyph({
      text: "从而自定义自己博客园markdown样式.当然本文也可以当markdown语法学习之用.  "
    })
  )

fontmin.run(function(err, files) {
  if (err) {
    throw err
  }
})
