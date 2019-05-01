var express = require("express");
var router = express.Router();

const db = require("../config/db.config");
const commonController = require("../controllers/common.controller");

/* GET home/en page. */
router.get("/", function (req, res, next) {
	res.render("index");
});

/* GET home/zh_cn page. */
router.get("/zh-cn", function (req, res, next) {
	res.render("index_zhcn");
});

/* GET info page. */
router.get("/info", function (req, res, next) {
	const info = commonController.getInfo(db, req, res, next);
	res.render("info", {info: info});
});


// 获取研究人数占前10的领域
router.get("/person", (req, res, next) => {
	commonController.getPerson(db, req, res, next);
});

// 获取研究比重占前10的领域
router.get("/weight", (req, res, next) => {
	commonController.getWeight(db, req, res, next);
});

// 分页获取根据hindex排序的user信息
router.get("/hindex", (req, res, next) => {
	commonController.getHindex(db, req, res, next);
});

router.get("/excel", (req, res, next) => {
	commonController.exportExcel(db, req, res, next);
});


module.exports = router;