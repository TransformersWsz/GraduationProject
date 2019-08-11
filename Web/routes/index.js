var express = require("express");
var router = express.Router();

const db = require("../config/db.config");
const commonController = require("../controllers/common.controller");

/* GET home/en page. */
router.get("/", function (req, res, next) {
	res.render("index");
});

/* GET home/zh_cn page. */
router.get("/zh_cn", function (req, res, next) {
	res.render("index_zhcn");
});

/* GET personal  homepage. */
router.get("/homepage", (req, res, next) => {
	commonController.getUserInfo(db, req, res, next).then((userInfo) => {
		if (req.query.lan == "en") {
			res.render("info", userInfo);
		}
		else {
			res.render("info_zhcn", userInfo);
		}
	}).catch((error) => {
		res.json(error);
	});
});

/* 接收研究人员的信息，返回研究人员的user_id. */
router.post("/info", (req, res, next) => {
	commonController.getUserId(db, req, res, next);
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

// 获取某个学者的前10名相似学者
router.get("/similarity", (req, res, next) => {
	commonController.getSimilarity(db, req, res, next);
});


// 导出excel
router.get("/excel", (req, res, next) => {
	commonController.exportExcel(db, req, res, next);
});

// 导出某学者的前10名相似学者
router.get("/similarityexcel", (req, res, next) => {
	commonController.exportSimilarityExcel(db, req, res, next);
});



module.exports = router;