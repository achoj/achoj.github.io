var Fontmin = require("fontmin");


// 在所有文件读取完成后执行 Fontmin 处理
function processAllContent() {
  var fontmin = new Fontmin()
    .src("./fonts/Kalam-Regular.ttf")
    .dest("./font-min/")
    .use(Fontmin.glyph({ text: "Achoj's Web Page"}));

  fontmin.run(function(err, files) {
    if (err) {
      console.error("Error processing content:", err);
      return;
    }
    console.log("Fontmin processed", files.length, "files successfully.");
  });
}

processAllContent()