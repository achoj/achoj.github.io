var Fontmin = require("fontmin");
var fs = require("fs");
var path = require("path");

// 指定目录
var directoryPath = "./articles";
// 存储所有文件内容的变量
var allContent = "";

// 递归读取目录下的文件
function readFilesInDirectory(directoryPath) {
  fs.readdir(directoryPath, function(err, files) {
    if (err) {
      console.error("Error reading directory:", err);
      return;
    }
    files.forEach(function(file) {
      var filePath = path.join(directoryPath, file);
      fs.stat(filePath, function(err, stat) {
        if (err) {
          console.error("Error reading file:", err);
          return;
        }
        if (stat.isDirectory()) {
          // 如果是目录，则递归读取目录下的文件
          readFilesInDirectory(filePath);
        } else {
          // 如果是文件，则读取文件内容并追加到 allContent 变量中
          fs.readFile(filePath, "utf8", function(err, data) {
            if (err) {
              console.error("Error reading file:", err);
              return;
            }
            allContent += data; // 追加文件内容
          });
        }
      });
    });
  });
}

// 在所有文件读取完成后执行 Fontmin 处理
function processAllContent() {
  console.log(allContent)
  var fontmin = new Fontmin()
    .src("./fonts/SiYuan.ttf")
    .dest("./fontmins/")
    .use(Fontmin.glyph({ text: allContent }));

  fontmin.run(function(err, files) {
    if (err) {
      console.error("Error processing content:", err);
      return;
    }
    console.log("Fontmin processed", files.length, "files successfully.");
  });
}

// 从指定目录开始递归读取文件
readFilesInDirectory(directoryPath);

// 当所有文件读取完成后，执行 Fontmin 处理
setTimeout(processAllContent, 1000); // 适当增加延迟以确保所有文件都被读取完毕
