const nodeExcel = require("excel-export");

// 获取学者的个人信息
const getInfo = (db, req, res, next) => {
    const info = "";
    const sql = "select name, paper, citation, h_index, g_index, sociability, diversity, activity from user where user_id = ?";
    db.sequelize.query(sql, {
        replacements: [parseInt(req.query.offset)],
        type: db.sequelize.QueryTypes.SELECT
    }).then((selectInfoRes) => {
        info = selectInfoRes[0];
    });
    return info;
};

// 获取各研究领域的人数
const getPerson = (db, req, res, next) => {
    let sql = "select name, person from interest_person_top10";
    if (req.query.lan == "zh_cn") {
        sql = "select en_zhcn.zhcn as name, interest_person_top10.person from interest_person_top10 join en_zhcn on en_zhcn.en = interest_person_top10.name;"
    }

    db.sequelize.query(sql, {
        type: db.sequelize.QueryTypes.SELECT
    }).then((selectPersonRes) => {
        const xData = [];
        const yData = [];
        selectPersonRes.map((item) => {
            xData.push(item.name);
            yData.push(item.person);
        });
        res.json([xData, yData]);
    });
};

// 获取各研究领域所占的比重
const getWeight = (db, req, res, next) => {
    let sql = "select w as value, name from interest_w_top10"
    if (req.query.lan == "zh_cn") {
        sql = "select w as value, en_zhcn.zhcn as name from interest_w_top10 join en_zhcn on interest_w_top10.name = en_zhcn.en";
    }
    db.sequelize.query(sql, {
        type: db.sequelize.QueryTypes.SELECT
    }).then((selectWRes) => {
        const legend = [];
        selectWRes.map((item) => {
            legend.push(item.name);
        });
        res.json([legend, selectWRes]);
    });
};

// 获取按照h_index高低排序的所有学者信息
const getHindex = (db, req, res, next) => {
    if (req.query.search == null || req.query.search == "") {
        db.sequelize.query("select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id limit ?, ?", {
            replacements: [parseInt(req.query.offset), parseInt(req.query.limit)],
            type: db.sequelize.QueryTypes.SELECT
        }).then((selectUH) => {
            db.sequelize.query("select count(user_id) as nums from user", {
                type: db.sequelize.QueryTypes.SELECT
            }).then((selectUserRes) => {
                res.json({
                    total: selectUserRes[0].nums,
                    rows: selectUH
                });
            });
        });
    }
    else {
        const search = req.query.search;
        const offset = req.query.offset;
        const limit = req.query.limit;

        db.sequelize.query("select count(user_id) as nums from user;", {
            type: db.sequelize.QueryTypes.SELECT
        }).then((selectUserNums) => {
            
            // selectUserNums[0].nums: 总学者数量
            db.sequelize.query("select incre_id from user_h_index limit 0, 2;", {
                type: db.sequelize.QueryTypes.SELECT
            }).then((selectFirstId) => {
                // selectFirstId[0].incre_id: user_h_index 的 incre_id

                batchSize = Math.ceil(selectUserNums[0].nums / 4);
                
                const promises = [];

                let firstIncreId = selectFirstId[0].incre_id;
                
                for (let i = 0; i < 4; i++) {
                    let lowIncreId = firstIncreId + i*batchSize;
                    let highIncreId = lowIncreId + batchSize - 1;
                    if (highIncreId > lowIncreId + selectUserNums[0].nums - 1) {
                        highIncreId = firstIncreId + selectUserNums[0].nums - 1;
                    }
                    let rowSql = `select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id where user_h_index.incre_id >= ${lowIncreId} and user_h_index.incre_id <= ${highIncreId} and (name like '%${search}%' or paper like '%${search}%' or citation like '%${search}%' or user.h_index like '%${search}%' or g_index like '%${search}%' or sociability like '%${search}%' or diversity like '%${search}%' or activity like '%${search}%');`;

                    let sqlPromise = db.sequelize.query(rowSql, {
                        type: db.sequelize.QueryTypes.SELECT
                    });
                    promises.push(sqlPromise);
                }

                Promise.all(promises).then((allResults) => {
                    const result = [];
                    allResults.map((item) => {
                        result.push(...item);
                    });
                    const split = result.slice(offset, offset+limit);
                    res.json({
                        total: result.length,
                        rows: split
                    });
                });
            });
        });

        // let rowSql = `select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id where name like '%${search}%' or paper like '%${search}%' or citation like '%${search}%' or user.h_index like '%${search}%' or g_index like '%${search}%' or sociability like '%${search}%' or diversity like '%${search}%' or activity like '%${search}%' limit ${offset}, ${limit};`;

        // let totalSql = `select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id where name like '%${search}%' or paper like '%${search}%' or citation like '%${search}%' or user.h_index like '%${search}%' or g_index like '%${search}%' or sociability like '%${search}%' or diversity like '%${search}%' or activity like '%${search}%';`;
        // db.sequelize.query(rowSql, {
        //     type: db.sequelize.QueryTypes.SELECT
        // }).then((selectUH) => {
        //     db.sequelize.query(totalSql, {
        //         type: db.sequelize.QueryTypes.SELECT
        //     }).then((selectTotalUserRes) => {
        //         res.json({
        //             total: selectTotalUserRes.length,
        //             rows: selectUH
        //         });
        //     });
        // });
    }
    
};

const formatResult = (selectRes) => {
    const result = [];
    selectRes.map((item) => {
        const row = [];
        row.push(item.name);
        row.push(item.h_index);
        row.push(item.paper);
        row.push(item.citation);
        row.push(item.g_index);
        row.push(item.sociability);
        row.push(item.diversity);
        row.push(item.activity);
        result.push(row);
    });
    return result;
};

// 导出excel
const exportExcel = (db, req, res, next) => {
    let name = "aminers";
    let cols = [
        {
            caption: "name",
            type: "string",
            width: 30
        }, 
        {
            caption:"h_index",
            type:"number"				
        }, 
        {
            caption:"paper",
            type:"number"				
        }, 
        {
            caption:"citation",
            type:"number"				
        },
        {
            caption:"g_index",
            type:"number"				
        },
        {
            caption:"sociability",
            type:"number"				
        },
        {
            caption:"diversity",
            type:"number"				
        },
        {
            caption:"activity",
            type:"number"				
        }
    ];
    let filename = "export_aminer.xlsx";

    if (req.query.lan == "zh_cn") {
        // name = "学者名单";
        cols = [
            {
                caption: "姓名",
                type: "string",
                width: 30
            }, 
            {
                caption: "h指数",
                type: "number"				
            }, 
            {
                caption: "论文数",
                type: "number"				
            }, 
            {
                caption: "引用次数",
                type: "number"				
            },
            {
                caption: "g指数",
                type: "number"				
            },
            {
                caption: "群集度",
                type: "number"				
            },
            {
                caption: "多样性",
                type: "number"				
            },
            {
                caption: "活跃度",
                type: "number"				
            }
        ];
        filename = encodeURI("导出学者.xlsx");
    }

    db.sequelize.query("select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id", {
        type: db.sequelize.QueryTypes.SELECT
    }).then((result) => {
        var conf = {};
        conf.name = name;
        conf.cols = cols;
        conf.rows = formatResult(result);
        var excelFile = nodeExcel.execute(conf);
        res.setHeader('Content-Type', 'application/vnd.openxmlformats;charset=utf-8');
        res.setHeader("Content-Disposition", `attachment; filename=${filename}`);
        res.end(excelFile, "binary");
    });
};

const commonController = {};
commonController.getInfo = getInfo;
commonController.getPerson = getPerson;
commonController.getWeight = getWeight;
commonController.getHindex = getHindex;
commonController.exportExcel = exportExcel;

module.exports = commonController;